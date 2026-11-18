# -*- coding: utf-8 -*-
"""
Több Adathalmazos Esésdetektáló Benchmark Kiértékelő és Tesztelő Program
Téma: Gráf alapú modellek és viselkedéselemzés - Esésdetektálás
Használat: Hivatalos URFD és független (külső) valós videók kiértékelése
Modellek: YOLOv8s-Pose (Small) és YOLOv8n-Pose (Nano) összehasonlító elemzés
Készítette: Szakdolgozó Hallgató (BSc Mérnökinformatikus)
"""

import os
import sys
import time
import math
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)

from simple_fall_detector import KinematicFallDetector

try:
    from ultralytics import YOLO
except ImportError:
    print("[HIBA] Az 'ultralytics' csomag nincs telepítve!")
    sys.exit(1)


MODELS = {
    "YOLOv8s-Pose (Small - 11.6M param, Nagy pontosság)": os.path.join(WORKSPACE_DIR, "yolov8s-pose.pt"),
    "YOLOv8n-Pose (Nano - 3.2M param, Beágyazott / RPi)": os.path.join(WORKSPACE_DIR, "yolov8n-pose.pt")
}

BENCHMARK_SETS = {
    # --- 1. CSOPORT: UR FALL DETECTION (URFD) AKADÉMIAI ADATHALMAZ ---
    "1. [URFD] Fall-01 (Valós Esés - Előre zuhanás)": {
        "type": "folder",
        "path": os.path.join(WORKSPACE_DIR, "data", "raw", "urfd", "fall-01", "fall-01-cam0-rgb"),
        "ground_truth": "FALL",
        "description": "URFD Benchmark: Belépés a szobába, majd hirtelen előre zuhanás a padlóra."
    },
    "2. [URFD] Fall-02 (Valós Esés - Hátra esés)": {
        "type": "folder",
        "path": os.path.join(WORKSPACE_DIR, "data", "raw", "urfd", "fall-02", "fall-02-cam0-rgb"),
        "ground_truth": "FALL",
        "description": "URFD Benchmark: Egyensúlyvesztés és hátrairányuló zuhanás."
    },
    "3. [URFD] ADL-01 (Normál Mozgás - Séta és leülés)": {
        "type": "folder",
        "path": os.path.join(WORKSPACE_DIR, "data", "raw", "urfd", "adl-01", "adl-01-cam0-rgb"),
        "ground_truth": "ADL",
        "description": "URFD Benchmark: Séta, székre leülés, majd felállás (Vaklárma-szűrés tesztje)."
    },
    "4. [URFD] ADL-02 (Normál Mozgás - Tárgy felvétele a padlóról)": {
        "type": "folder",
        "path": os.path.join(WORKSPACE_DIR, "data", "raw", "urfd", "adl-02", "adl-02-cam0-rgb"),
        "ground_truth": "ADL",
        "description": "URFD Benchmark: Lehajolás a földre tárgyért, felegyenesedés (Törzsdőlés teszt)."
    },

    # --- 2. CSOPORT: FÜGGETLEN (KÜLSŐ, NEM TANÍTOTT) BENCHMARK ADATHALMAZ ---
    "5. [Független] Fall-01 (Valós Esés - Hirtelen zuhanás)": {
        "type": "video",
        "path": os.path.join(WORKSPACE_DIR, "data", "raw", "independent_benchmark", "fall_independent_01.mp4"),
        "ground_truth": "FALL",
        "description": "Külső Független Benchmark: Valós beltéri esés (különböző kamera és környezet)."
    },
    "6. [Független] Fall-02 (Valós Esés - Padlón megcsúszás)": {
        "type": "video",
        "path": os.path.join(WORKSPACE_DIR, "data", "raw", "independent_benchmark", "fall_independent_02.mp4"),
        "ground_truth": "FALL",
        "description": "Külső Független Benchmark (OpenVINO): Hirtelen csúszás és lezuhanás."
    },
    "7. [Független] ADL-01 (Normál Mozgás - Folyamatos séta)": {
        "type": "video",
        "path": os.path.join(WORKSPACE_DIR, "data", "raw", "independent_benchmark", "adl_independent_01.mp4"),
        "ground_truth": "ADL",
        "description": "Külső Független Benchmark (Intel IoT): Folyamatos természetes járás (0 vaklárma elvárt)."
    }
}


class BenchmarkViewerApp:
    def __init__(self):
        print("\n" + "="*65)
        print("  Több Adathalmazos Esésdetektáló Benchmark Kiértékelő Rendszer")
        print("="*65)

        self.loaded_models = {}
        # Elsődleges modell: YOLOv8s-Pose (Small)
        default_model_key = list(MODELS.keys())[0]
        self.current_model_key = default_model_key
        print(f"[1/2] Elsődleges modell betöltése: {self.current_model_key}...")
        self.model = self.get_or_load_model(default_model_key)
        self.detector = KinematicFallDetector()

        self.stgcn_path = os.path.join(WORKSPACE_DIR, "models", "stgcn_fall.onnx")
        self.has_stgcn = os.path.exists(self.stgcn_path)
        if self.has_stgcn:
            print(f"[OK] ST-GCN ONNX modell megtalálva: {self.stgcn_path}")
        else:
            print("[INFO] ST-GCN ONNX nem található, teszt a robusztus Kinematikai V2 motorral fut.")

        print("[2/2] Grafikus felület inicializálása...")
        self.root = tk.Tk()
        self.root.title("Szakdolgozat: Több Adathalmazos Esésdetektáló Benchmark")
        self.root.geometry("1150x880")
        self.root.minsize(950, 720)
        self.root.configure(bg="#0F172A")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Felső fejléc és adathalmaz választó sáv
        top_frame = tk.Frame(self.root, bg="#1E293B", pady=8, padx=12)
        top_frame.pack(fill=tk.X)

        # Adathalmaz sor
        row1 = tk.Frame(top_frame, bg="#1E293B")
        row1.pack(fill=tk.X, pady=(0, 6))

        tk.Label(row1, text="Teszt Videó:", font=("Segoe UI", 10, "bold"),
                 bg="#1E293B", fg="#F8FAFC").pack(side=tk.LEFT, padx=(0, 6))

        self.dataset_combo = ttk.Combobox(
            row1,
            values=list(BENCHMARK_SETS.keys()),
            state="readonly",
            width=46,
            font=("Segoe UI", 9)
        )
        # Alapértelmezetten a független 1. videó, hogy azonnal ezt lássa a felhasználó
        self.dataset_combo.current(4)  # 5. [Független] Fall-01
        self.dataset_combo.pack(side=tk.LEFT, padx=4)
        self.dataset_combo.bind("<<ComboboxSelected>>", self.on_dataset_change)

        self.btn_restart = tk.Button(
            row1,
            text="▶️ Újraindítás",
            command=self.restart_video,
            font=("Segoe UI", 9, "bold"),
            bg="#0284C7",
            fg="white",
            padx=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.btn_restart.pack(side=tk.RIGHT, padx=4)

        # Modell választó sor
        row2 = tk.Frame(top_frame, bg="#1E293B")
        row2.pack(fill=tk.X)

        tk.Label(row2, text="Pózbecslő Modell:", font=("Segoe UI", 10, "bold"),
                 bg="#1E293B", fg="#38BDF8").pack(side=tk.LEFT, padx=(0, 6))

        self.model_combo = ttk.Combobox(
            row2,
            values=list(MODELS.keys()),
            state="readonly",
            width=46,
            font=("Segoe UI", 9)
        )
        self.model_combo.current(0)  # YOLOv8s-Pose
        self.model_combo.pack(side=tk.LEFT, padx=4)
        self.model_combo.bind("<<ComboboxSelected>>", self.on_model_change)

        self.lbl_model_info = tk.Label(row2, text="[Nagyobb kapacitás, fekvő testtartásra optimalizált]",
                                       font=("Segoe UI", 8, "italic"), bg="#1E293B", fg="#94A3B8")
        self.lbl_model_info.pack(side=tk.LEFT, padx=6)

        # Videó Megjelenítő Vászon
        self.lbl_video = tk.Label(self.root, bg="#000000")
        self.lbl_video.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        # Fő Állapotsáv (Zöld: BIZTONSÁGOS / Vörös: VÉSZRIASZTÁS)
        self.lbl_status = tk.Label(
            self.root,
            text="TESZT INDÍTÁSA...",
            font=("Segoe UI", 15, "bold"),
            bg="#15803D",
            fg="white",
            pady=8
        )
        self.lbl_status.pack(fill=tk.X)

        # Telemetria és diagnosztikai adatsor
        self.lbl_telemetry = tk.Label(
            self.root,
            text="Inicializálás...",
            font=("Consolas", 10),
            bg="#0F172A",
            fg="#38BDF8",
            pady=5
        )
        self.lbl_telemetry.pack(fill=tk.X)

        # Eredmény-összegző és Kiértékelő Sáv
        self.lbl_verdict = tk.Label(
            self.root,
            text="Várakozás a tesztfutásra...",
            font=("Segoe UI", 11, "bold"),
            bg="#1E293B",
            fg="#FCD34D",
            pady=8
        )
        self.lbl_verdict.pack(fill=tk.X)

        # Videó vezérlő állapotok
        self.current_type = None
        self.cap = None
        self.frames = []
        self.total_frames = 0
        self.fps = 30.0
        self.current_frame_idx = 0
        self.is_running = True
        self.fall_detected_at = None
        self.restarting = False

        self.load_current_dataset()
        self.update_loop()
        self.root.mainloop()

    def get_or_load_model(self, model_key):
        if model_key in self.loaded_models:
            return self.loaded_models[model_key]
        m_path = MODELS[model_key]
        if not os.path.exists(m_path):
            print(f"[FIGYELEM] {m_path} nem található, visszatérés yolov8n-re.")
            m_path = os.path.join(WORKSPACE_DIR, "yolov8n-pose.pt")
        m = YOLO(m_path)
        self.loaded_models[model_key] = m
        return m

    def on_model_change(self, event):
        new_key = self.model_combo.get()
        print(f"[INFO] Váltás modellre: {new_key}...")
        self.model = self.get_or_load_model(new_key)
        self.current_model_key = new_key
        if "Small" in new_key:
            self.lbl_model_info.config(text="[Nagyobb kapacitás, fekvő testtartásra optimalizált]")
        else:
            self.lbl_model_info.config(text="[Kisebb méret, beágyazott eszközökre / RPi optimalizált]")
        self.restart_video()

    def load_current_dataset(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        choice = self.dataset_combo.get()
        info = BENCHMARK_SETS[choice]
        target_path = info["path"]
        self.current_type = info["type"]

        self.detector.reset()
        self.fall_detected_at = None
        self.last_known_bbox = None
        self.current_frame_idx = 0
        self.frames = []
        self.restarting = False

        if not os.path.exists(target_path):
            print(f"[HIBA] Nem található: {target_path}")
            self.lbl_verdict.config(
                text=f"⚠️ Az adatkészlet még nem található a gépen: {os.path.basename(target_path)}",
                bg="#854D0E", fg="#FEF08A"
            )
            return

        if self.current_type == "folder":
            png_files = sorted([f for f in os.listdir(target_path) if f.lower().endswith((".png", ".jpg"))])
            self.frames = [os.path.join(target_path, f) for f in png_files]
            self.total_frames = len(self.frames)
            self.fps = 30.0
        else: # video
            self.cap = cv2.VideoCapture(target_path)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 25.0

        dur_sec = (self.total_frames / self.fps) if self.fps > 0 else 0
        print(f"[OK] Betöltve: {self.total_frames} frame (~{dur_sec:.1f} mp) -> {choice}")
        self.lbl_verdict.config(
            text=f"Lejátszás: {self.total_frames} képkocka (~{dur_sec:.1f} mp) | Elvárt: {info['ground_truth']} | {info['description']}",
            bg="#1E293B", fg="#FCD34D"
        )

    def on_dataset_change(self, event):
        self.load_current_dataset()

    def restart_video(self):
        self.detector.reset()
        self.fall_detected_at = None
        self.last_known_bbox = None
        self.current_frame_idx = 0
        self.restarting = False
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def update_loop(self):
        if not self.is_running:
            return

        if self.total_frames == 0:
            self.root.after(500, self.update_loop)
            return

        # 1. Képkocka beolvasása
        frame = None
        if self.current_type == "folder":
            if self.current_frame_idx < len(self.frames):
                frame = cv2.imread(self.frames[self.current_frame_idx])
            else:
                frame = None
        else:
            if self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    frame = None
            else:
                frame = None

        # Videó vége kiértékelés
        if frame is None or self.current_frame_idx >= self.total_frames:
            if not self.restarting:
                self.restarting = True
                choice = self.dataset_combo.get()
                info = BENCHMARK_SETS[choice]
                gt = info["ground_truth"]

                if gt == "FALL":
                    if self.fall_detected_at is not None:
                        v_text = f"✅ SIKERES TESZT! Valós esés detektálva {self.fall_detected_at:.2f} mp-nél (True Positive)!"
                        v_bg = "#15803D"
                    else:
                        v_text = "❌ HIBA: Az esés észrevétlen maradt (False Negative)!"
                        v_bg = "#B91C1C"
                else: # ADL
                    if self.fall_detected_at is None:
                        v_text = "✅ SIKERES TESZT! Normál mozgás mellett nulla téves riasztás (True Negative)!"
                        v_bg = "#15803D"
                    else:
                        v_text = f"⚠️ TÉVES RIASZTÁS! Normál mozgásra esést jelzett {self.fall_detected_at:.2f} mp-nél (False Positive)!"
                        v_bg = "#B45309"

                self.lbl_verdict.config(text=v_text, bg=v_bg, fg="white")
                self.root.after(2500, self.restart_video)

            self.root.after(100, self.update_loop)
            return

        timestamp_sec = self.current_frame_idx / (self.fps if self.fps > 0 else 30.0)

        # 2. Optimalizálás méretezéssel (ha túl nagy a felbontás)
        orig_h, orig_w = frame.shape[:2]
        if orig_w > 720:
            scale = 720.0 / orig_w
            frame = cv2.resize(frame, (720, int(orig_h * scale)))

        # 3. YOLOv8-pose inferencia (adaptívabb conf=0.25)
        t0 = time.time()
        results = self.model(frame, verbose=False, conf=0.25)
        dt_ms = (time.time() - t0) * 1000.0

        annotated_frame = results[0].plot()
        current_state = self.detector.state  # Alapértelmezetten megtartja az állapotgép állapotát!
        info_dict = {"torso_angle": 0.0, "aspect_ratio": 0.0, "drop_velocity": 0.0}

        if len(results[0].boxes) > 0 and results[0].keypoints is not None:
            # Több detekció esetén válasszuk a legmagasabb konfidenciájú személyt
            best_idx = int(np.argmax(results[0].boxes.conf.cpu().numpy()))
            bbox = results[0].boxes.xyxy[best_idx].cpu().numpy()
            kpts = results[0].keypoints.data[best_idx].cpu().numpy()
            self.last_known_bbox = bbox
            current_state, info_dict = self.detector.update(
                kpts, bbox, current_time=timestamp_sec, frame_w=frame.shape[1], frame_h=frame.shape[0]
            )

            if current_state == "FALLEN" and self.fall_detected_at is None:
                self.fall_detected_at = timestamp_sec

            if info_dict.get("torso_vector") is not None:
                hx, hy, sx, sy = info_dict["torso_vector"]
                if current_state == "FALLEN":
                    col = (0, 0, 255)
                elif current_state in ["WARNING", "DROP_DETECTED"]:
                    col = (0, 165, 255)
                else:
                    col = (0, 255, 0)
                cv2.line(annotated_frame, (hx, hy), (sx, sy), col, 4)
        else:
            # HA ELTŰNIK A SZELETON A PADLÓN (takarás, bútor, járókeret):
            current_state, reason = self.detector.handle_disappearance(current_time=timestamp_sec, frame_w=frame.shape[1])
            if current_state == "FALLEN" and self.fall_detected_at is None:
                self.fall_detected_at = timestamp_sec

            # Ha a padlón veszett el a skeleton, rajzoljuk ki az utolsó ismert pozíciót vörössel
            if current_state == "FALLEN" and hasattr(self, "last_known_bbox") and self.last_known_bbox is not None:
                bx1, by1, bx2, by2 = [int(v) for v in self.last_known_bbox]
                cv2.rectangle(annotated_frame, (bx1, by1), (bx2, by2), (0, 0, 255), 3)
                cv2.putText(annotated_frame, "EMBER A PADLON (TAKARASBAN)", (bx1, max(20, by1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # 4. GUI Frissítés
        h, w, _ = annotated_frame.shape
        if current_state == "FALLEN":
            time_on_f = f" | Földön: {self.detector.time_on_floor:.1f}s" if self.detector.time_on_floor > 0 else ""
            status_text = f"🚨 VÉSZHELYZET: ESÉS DETEKTÁLVA! ({timestamp_sec:.2f} mp-nél{time_on_f})"
            status_bg = "#B91C1C"
            cv2.rectangle(annotated_frame, (0, 0), (w, h), (0, 0, 255), 12)
        elif current_state == "DROP_DETECTED":
            status_text = f"🚨 GYORS ZUHANÁS ÉRZÉKELVE ({timestamp_sec:.2f} mp)"
            status_bg = "#EA580C"
            cv2.rectangle(annotated_frame, (0, 0), (w, h), (0, 100, 255), 8)
        elif current_state == "WARNING":
            status_text = f"⚠️ FIGYELEM: ESÉSVESZÉLY / EGYENSÚLYVESZTÉS! ({timestamp_sec:.2f} mp | Dőlés: {info_dict['torso_angle']:.1f}°)"
            status_bg = "#D97706"
            cv2.rectangle(annotated_frame, (0, 0), (w, h), (0, 190, 255), 6)
        else:
            status_text = f"✅ BIZTONSÁGOS: NORMÁL MOZGÁS ({timestamp_sec:.2f} mp)"
            status_bg = "#15803D"

        self.lbl_status.config(text=status_text, bg=status_bg)

        telemetry = (
            f"Frame: {self.current_frame_idx + 1}/{self.total_frames} ({timestamp_sec:.2f}s) | "
            f"Inferencia: {dt_ms:.1f} ms | Modell: {self.current_model_key.split()[0]} | "
            f"Törzsszög: {info_dict['torso_angle']:.1f}° | W/H: {info_dict['aspect_ratio']:.2f}"
        )
        self.lbl_telemetry.config(text=telemetry)

        # Dinamikus képméret-igazítás az ablakhoz:
        lbl_w = self.lbl_video.winfo_width()
        lbl_h = self.lbl_video.winfo_height()
        if lbl_w < 100 or lbl_h < 100:
            lbl_w, lbl_h = 920, 560

        fh, fw = annotated_frame.shape[:2]
        scale = min((lbl_w - 6) / fw, (lbl_h - 6) / fh)
        disp_w = max(10, int(fw * scale))
        disp_h = max(10, int(fh * scale))

        disp_frame = cv2.resize(annotated_frame, (disp_w, disp_h), interpolation=cv2.INTER_LINEAR)
        rgb = cv2.cvtColor(disp_frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        img_tk = ImageTk.PhotoImage(image=pil_img)
        self.lbl_video.img_tk = img_tk
        self.lbl_video.configure(image=img_tk)

        self.current_frame_idx += 1
        # Folyamatos lejátszás
        self.root.after(25, self.update_loop)

    def on_close(self):
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()
        print("[OK] Benchmark kiértékelő bezárva.")


if __name__ == "__main__":
    BenchmarkViewerApp()
