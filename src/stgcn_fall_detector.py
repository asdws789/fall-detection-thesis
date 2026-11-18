# -*- coding: utf-8 -*-
"""
Valós Idejű Gráfkonvolúciós Esésdetektáló Rendszer (YOLOv8-Pose + ST-GCN ONNX)
Téma: Gráf alapú modellek alkalmazása vizuális információ feldolgozására
Hardver: AMD Ryzen 5 CPU / Raspberry Pi 5 (100% Helyi Inferencia)
Készítette: Szakdolgozó Hallgató

Működési elv:
1. Webkamera képkocka beolvasása (OpenCV).
2. 17 Kulcspont kinyerése (YOLOv8n-pose).
3. Csípőközép és testhossz normalizálás, 32 képkockás csúszóablak tenzorképzés: (1, 3, 32, 17, 1).
4. Tér-Időbeli Gráfkonvolúció (ST-GCN ONNX modell futtatása ONNX Runtime-mal).
5. Háromfázisú hiszterézis állapotgép és földön töltött idő mérése.
"""

import os
import sys
import time
import math
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import onnxruntime as ort

try:
    from ultralytics import YOLO
except ImportError:
    print("[HIBA] Az 'ultralytics' nincs telepítve! Futtasd: pip install ultralytics")
    sys.exit(1)


class STGCNFallDetector:
    def __init__(self, onnx_model_path=None):
        self.onnx_path = onnx_model_path
        self.ort_session = None
        self.is_onnx_ready = False

        if self.onnx_path and os.path.exists(self.onnx_path):
            try:
                opts = ort.SessionOptions()
                opts.intra_op_num_threads = 4
                opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
                self.ort_session = ort.InferenceSession(self.onnx_path, opts)
                self.is_onnx_ready = True
                print(f"[OK] ST-GCN ONNX modell sikeresen betöltve: {self.onnx_path}")
            except Exception as e:
                print(f"[FIGYELEM] Nem sikerült betölteni az ONNX modellt ({e}), tartalék mód aktív.")

        # Csúszóablak puffer: legutóbbi T=32 normalizált váz
        self.window_size = 32
        self.skeleton_buffer = []  # list of (17, 3) arrays
        
        # Állapotgép változók
        self.state = "NORMAL"  # NORMAL, DROP_DETECTED, FALLEN
        self.fall_start_time = None
        self.time_on_floor = 0.0
        self.horizontal_start_time = None

    def reset(self):
        self.skeleton_buffer.clear()
        self.state = "NORMAL"
        self.fall_start_time = None
        self.time_on_floor = 0.0
        self.horizontal_start_time = None

    def normalize_skeleton(self, keypoints):
        """
        keypoints: (17, 3) [x, y, conf]
        Normalizálja a koordinátákat a csípőközép origóhoz és a törzshosszhoz képest.
        """
        kpts = keypoints.copy()
        l_hip, r_hip = kpts[11], kpts[12]
        l_sh, r_sh = kpts[5], kpts[6]

        hip_cx = (l_hip[0] + r_hip[0]) / 2.0
        hip_cy = (l_hip[1] + r_hip[1]) / 2.0
        sh_cx = (l_sh[0] + r_sh[0]) / 2.0
        sh_cy = (l_sh[1] + r_sh[1]) / 2.0

        torso_len = math.hypot(sh_cx - hip_cx, sh_cy - hip_cy)
        torso_len = max(torso_len, 30.0)

        # Eltolás és skálázás
        norm_kpts = np.zeros_like(kpts)
        norm_kpts[:, 0] = (kpts[:, 0] - hip_cx) / torso_len
        norm_kpts[:, 1] = (kpts[:, 1] - hip_cy) / torso_len
        norm_kpts[:, 2] = kpts[:, 2]  # Konfidencia megmarad

        return norm_kpts

    def update(self, raw_keypoints, bbox):
        """
        raw_keypoints: (17, 3)
        bbox: [x1, y1, x2, y2]
        Visszaad: (state, info_dict)
        """
        curr_time = time.time()
        x1, y1, x2, y2 = bbox
        box_w = max(1.0, float(x2 - x1))
        box_h = max(1.0, float(y2 - y1))
        aspect_ratio = box_w / box_h

        # 1. Kinematikai kiegészítő jellemzők
        l_sh, r_sh = raw_keypoints[5], raw_keypoints[6]
        l_hip, r_hip = raw_keypoints[11], raw_keypoints[12]

        sh_cx = (l_sh[0] + r_sh[0]) / 2.0
        sh_cy = (l_sh[1] + r_sh[1]) / 2.0
        hip_cx = (l_hip[0] + r_hip[0]) / 2.0
        hip_cy = (l_hip[1] + r_hip[1]) / 2.0

        dx = sh_cx - hip_cx
        dy = sh_cy - hip_cy
        torso_angle = math.degrees(math.atan2(abs(dx), abs(dy) + 1e-5))
        torso_vector = (int(hip_cx), int(hip_cy), int(sh_cx), int(sh_cy))

        # 2. Váz normalizálása és csúszóablak bővítése
        norm_kpts = self.normalize_skeleton(raw_keypoints)
        self.skeleton_buffer.append(norm_kpts)
        if len(self.skeleton_buffer) > self.window_size:
            self.skeleton_buffer.pop(0)

        # 3. ST-GCN Inferencia (ha a puffer tele van és az ONNX be van töltve)
        p_fall = 0.0
        p_adl = 1.0

        if self.is_onnx_ready and len(self.skeleton_buffer) == self.window_size:
            # Tenzor építése: (1, 3, 32, 17, 1) -> (Batch, Channels, Time, Vertices, Persons)
            tensor = np.zeros((1, 3, self.window_size, 17, 1), dtype=np.float32)
            for t_idx, skel in enumerate(self.skeleton_buffer):
                tensor[0, 0, t_idx, :, 0] = skel[:, 0]  # x
                tensor[0, 1, t_idx, :, 0] = skel[:, 1]  # y
                tensor[0, 2, t_idx, :, 0] = skel[:, 2]  # conf

            ort_inputs = {self.ort_session.get_inputs()[0].name: tensor}
            logits = self.ort_session.run(None, ort_inputs)[0][0]
            # Softmax valószínűség
            exp_l = np.exp(logits - np.max(logits))
            probs = exp_l / np.sum(exp_l)
            p_adl = float(probs[0])
            p_fall = float(probs[1])

        # 4. Háromfázisú hiszterézis döntési állapotgép
        is_horizontal = (torso_angle > 55.0) or (aspect_ratio > 1.15)
        is_upright = (torso_angle < 35.0) and (aspect_ratio < 0.85)

        # Esés trigger feltételek
        if self.is_onnx_ready:
            stgcn_trigger = (p_fall > 0.70)
        else:
            # Tartalék heurisztika, amíg nincs letöltve az ONNX fájl
            stgcn_trigger = is_horizontal and (aspect_ratio > 1.25)

        if is_horizontal:
            if self.horizontal_start_time is None:
                self.horizontal_start_time = curr_time
            time_horizontal = curr_time - self.horizontal_start_time

            if self.state == "NORMAL":
                if stgcn_trigger or time_horizontal >= 0.6:
                    self.state = "FALLEN"
                    self.fall_start_time = curr_time
            elif self.state == "FALLEN":
                if self.fall_start_time is not None:
                    self.time_on_floor = curr_time - self.fall_start_time
        else:
            self.horizontal_start_time = None
            if is_upright:
                self.state = "NORMAL"
                self.fall_start_time = None
                self.time_on_floor = 0.0

        info = {
            "p_fall": p_fall,
            "p_adl": p_adl,
            "torso_angle": torso_angle,
            "aspect_ratio": aspect_ratio,
            "time_on_floor": self.time_on_floor,
            "is_horizontal": is_horizontal,
            "is_upright": is_upright,
            "torso_vector": torso_vector,
            "is_onnx_active": self.is_onnx_ready,
            "buffer_fill": len(self.skeleton_buffer)
        }
        return self.state, info


# ----------------- FELHASZNÁLÓI FELÜLET (TKINTER) -----------------
class STGCNApp:
    def __init__(self):
        print("\n========================================================")
        print("  Szakdolgozat: ST-GCN Gráf Esésdetektáló Alkalmazás")
        print("  (YOLOv8-Pose + Tér-Időbeli Gráfkonvolúció ONNX)")
        print("========================================================")

        yolo_path = r"C:\uni_stuff\anti_thesis\yolov8n-pose.pt"
        onnx_path = r"C:\uni_stuff\anti_thesis\models\stgcn_fall.onnx"

        print("[1/3] YOLOv8n-pose modell betöltése...")
        self.model = YOLO(yolo_path)
        self.detector = STGCNFallDetector(onnx_path)

        print("[2/3] Webkamera felderítése...")
        self.cap = None
        for idx in [0, 1, 2]:
            c = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
            if not c.isOpened():
                c = cv2.VideoCapture(idx)
            if c.isOpened():
                for _ in range(5):
                    time.sleep(0.04)
                    ret, frame = c.read()
                    if ret and frame is not None and frame.size > 0:
                        self.cap = c
                        print(f"[OK] Működő webkamera rögzítve (Index: {idx})")
                        break
                if self.cap is not None:
                    break
                c.release()

        self.use_synthetic = (self.cap is None)
        if self.use_synthetic:
            print("[INFO] Élő webkamera hiányában szintetikus tesztmód fut.")

        print("[3/3] GUI Felület indítása...")
        self.root = tk.Tk()
        self.root.title("Szakdolgozat: Valós Idejű ST-GCN Gráf Esésdetektáló Rendszer")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.configure(bg="#0F172A")

        # Fő videó keret
        self.lbl_video = tk.Label(self.root, bg="#111111")
        self.lbl_video.pack(fill=tk.BOTH, expand=True)

        # Fő állapotsáv
        self.lbl_status = tk.Label(
            self.root,
            text="FIGYELÉS AKTÍV: NORMÁL ÁLLAPOT",
            font=("Segoe UI", 16, "bold"),
            bg="#15803D",
            fg="white",
            pady=12
        )
        self.lbl_status.pack(fill=tk.X)

        # Telemetria sáv
        self.lbl_telemetry = tk.Label(
            self.root,
            text="Telemetria inicializálás...",
            font=("Consolas", 11),
            bg="#0F172A",
            fg="#38BDF8",
            pady=8
        )
        self.lbl_telemetry.pack(fill=tk.X)

        # Vezérlősáv
        btn_frame = tk.Frame(self.root, bg="#1E293B", pady=6)
        btn_frame.pack(fill=tk.X)

        self.btn_reset = tk.Button(
            btn_frame,
            text="🔄 Állapot visszaállítása (Reset)",
            command=self.reset_detector,
            font=("Segoe UI", 10, "bold"),
            bg="#475569",
            fg="white",
            padx=12,
            pady=4,
            relief=tk.FLAT
        )
        self.btn_reset.pack(side=tk.LEFT, padx=15)

        self.lbl_mode_badge = tk.Label(
            btn_frame,
            text="Modell: ST-GCN ONNX" if self.detector.is_onnx_ready else "Modell: Tartalék Kinematika V2",
            font=("Segoe UI", 10, "bold"),
            bg="#0369A1" if self.detector.is_onnx_ready else "#854D0E",
            fg="#F8FAFC",
            padx=10,
            pady=4
        )
        self.lbl_mode_badge.pack(side=tk.RIGHT, padx=15)

        self.prev_time = time.time()
        self.fps_buffer = []
        self.running = True

        self.update_loop()
        self.root.mainloop()

    def reset_detector(self):
        self.detector.reset()
        print("[INFO] Detektor állapot törölve.")

    def update_loop(self):
        if not self.running:
            return

        if not self.use_synthetic and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Webkamera nem elerheto", (140, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # YOLOv8-Pose inferencia
        t0 = time.time()
        results = self.model(frame, verbose=False, conf=0.40)
        pose_ms = (time.time() - t0) * 1000.0

        # FPS
        curr_time = time.time()
        dt = curr_time - self.prev_time
        fps = 1.0 / dt if dt > 0 else 30.0
        self.prev_time = curr_time
        self.fps_buffer.append(fps)
        if len(self.fps_buffer) > 15:
            self.fps_buffer.pop(0)
        avg_fps = np.mean(self.fps_buffer)

        annotated_frame = results[0].plot()
        current_state = "NORMAL"
        info = {
            "p_fall": 0.0,
            "p_adl": 1.0,
            "torso_angle": 0.0,
            "aspect_ratio": 0.0,
            "time_on_floor": 0.0,
            "is_horizontal": False,
            "is_upright": True,
            "torso_vector": None,
            "is_onnx_active": self.detector.is_onnx_ready,
            "buffer_fill": 0
        }

        if len(results[0].boxes) > 0 and results[0].keypoints is not None:
            bbox = results[0].boxes.xyxy[0].cpu().numpy()
            kpts = results[0].keypoints.data[0].cpu().numpy()
            current_state, info = self.detector.update(kpts, bbox)

            # Gerincvektor kirajzolása
            if info["torso_vector"] is not None:
                hx, hy, sx, sy = info["torso_vector"]
                vec_color = (0, 0, 255) if info["torso_angle"] > 55.0 else (0, 255, 0)
                cv2.line(annotated_frame, (hx, hy), (sx, sy), vec_color, 4)

        # GUI Frissítés
        h, w, _ = annotated_frame.shape
        if current_state == "FALLEN":
            status_text = f"🚨 VÉSZHELYZET: ESÉS ÉSZLELVE! (Földön: {info['time_on_floor']:.1f} mp)"
            status_bg = "#B91C1C"
            cv2.rectangle(annotated_frame, (0, 0), (w, h), (0, 0, 255), 14)
            cv2.putText(annotated_frame, "ESES VESZHELYZET!", (30, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1.1, (0, 0, 255), 3)
        else:
            status_text = "✅ BIZTONSÁGOS: NORMÁL MOZGÁSFORMÁK"
            status_bg = "#15803D"

        self.lbl_status.config(text=status_text, bg=status_bg)

        # Telemetria
        onnx_str = f"P(Esés): {info['p_fall']*100:4.1f}% | Puffer: {info['buffer_fill']}/32" if info['is_onnx_active'] else "ST-GCN: Töltsd be az ONNX modellt!"
        telemetry_text = (
            f"FPS: {avg_fps:.1f} | Inferencia: {pose_ms:.1f} ms | "
            f"Dőlésszög: {info['torso_angle']:.1f}° | W/H arány: {info['aspect_ratio']:.2f} | "
            f"{onnx_str}"
        )
        self.lbl_telemetry.config(text=telemetry_text)

        # Kép megjelenítés
        rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        img_tk = ImageTk.PhotoImage(image=pil_img)
        self.lbl_video.img_tk = img_tk
        self.lbl_video.configure(image=img_tk)

        self.root.after(10, self.update_loop)

    def on_close(self):
        self.running = False
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()
        print("[OK] ST-GCN detektor bezárva.")


if __name__ == "__main__":
    STGCNApp()
