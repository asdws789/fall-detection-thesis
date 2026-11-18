# -*- coding: utf-8 -*-
"""
Valós Idejű Arckifejezés és Érzelemfelismerő Rendszer (YOLO + ONNX FERPlus)
Téma: Gráf alapú modellek és vizuális viselkedéselemzés
Hardver: AMD Ryzen 5 CPU optimalizációval (100% Helyi futás, 0 Ft költség)
Készítette: Szakdolgozó Hallgató

Működési elv:
1. Arcfelderítés: YOLOv8 fej-kulcspontok + OpenCV Haar Cascade hibrid detektor.
2. Érzelem-osztályozás: Helyi ONNX FERPlus mély konvolúciós modell (Microsoft Open Source).
3. Eredmény: 8 alapérzelem valószínűsége és domináns érzelem valós időben (30+ FPS).
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


# Érzelem kategóriák és Emojik (FERPlus 8 osztály)
EMOTION_LABELS = [
    ("Semleges", "😐", "#64748B"),       # 0: Neutral
    ("Boldog / Mosoly", "😃", "#16A34A"), # 1: Happiness
    ("Meglepett", "😲", "#D97706"),      # 2: Surprise
    ("Szomorú", "😢", "#2563EB"),        # 3: Sadness
    ("Dühös / Harag", "😡", "#DC2626"),  # 4: Anger
    ("Undor", "🤢", "#4D7C0F"),          # 5: Disgust
    ("Félelem", "😨", "#7C3AED"),        # 6: Fear
    ("Megvetés", "😏", "#9333EA")        # 7: Contempt
]


class FaceEmotionPipeline:
    def __init__(self, yolo_path, onnx_path):
        print("[1/2] YOLOv8n-pose modell betöltése...")
        self.yolo = YOLO(yolo_path)

        print("[2/2] ONNX FERPlus érzelemmodell inicializálása...")
        # ONNX Runtime CPU opciók
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 4
        opts.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.emotion_sess = ort.InferenceSession(onnx_path, opts)

        # OpenCV beépített arc-detektor (közeli portrékhoz)
        cascade_file = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        self.face_cascade = cv2.CascadeClassifier(cascade_file)

    def extract_face_crops(self, frame):
        """
        Kivágja az arcokat a képről YOLO fej-kulcspontok vagy Haar Cascade alapján.
        Visszaad: listája [(x1, y1, x2, y2), face_crop_bgr]
        """
        h_img, w_img, _ = frame.shape
        faces = []

        # 1. Stratégia: YOLOv8-pose kulcspontok (orr, szemek, fülek)
        results = self.yolo(frame, verbose=False, conf=0.40)
        if len(results[0].keypoints) > 0 and len(results[0].boxes) > 0:
            kpts_all = results[0].keypoints.data.cpu().numpy()
            for kpts in kpts_all:
                # 0: orr, 1: bal szem, 2: jobb szem, 3: bal fül, 4: jobb fül
                nose = kpts[0]
                l_eye = kpts[1]
                r_eye = kpts[2]

                # Ha a szem és az orr látható
                if nose[2] > 0.35 and l_eye[2] > 0.35 and r_eye[2] > 0.35:
                    eye_dx = r_eye[0] - l_eye[0]
                    eye_dy = r_eye[1] - l_eye[1]
                    eye_dist = math.hypot(eye_dx, eye_dy)
                    face_size = max(60, int(eye_dist * 2.8))

                    cx = int((l_eye[0] + r_eye[0]) / 2.0)
                    cy = int((l_eye[1] + r_eye[1]) / 2.0 + eye_dist * 0.3)

                    x1 = max(0, cx - face_size // 2)
                    y1 = max(0, cy - face_size // 2)
                    x2 = min(w_img, cx + face_size // 2)
                    y2 = min(h_img, cy + face_size // 2)

                    if (x2 - x1) > 40 and (y2 - y1) > 40:
                        faces.append(((x1, y1, x2, y2), frame[y1:y2, x1:x2]))

        # 2. Stratégia (Tartalék): Ha a YOLO nem talált teljes testet (pl. túl közel van a kamera)
        if len(faces) == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))
            for (x, y, w, h) in detected:
                # Kis ráhagyás a homlokra és állra
                x1 = max(0, x - int(w * 0.1))
                y1 = max(0, y - int(h * 0.15))
                x2 = min(w_img, x + w + int(w * 0.1))
                y2 = min(h_img, y + h + int(h * 0.15))
                faces.append(((x1, y1, x2, y2), frame[y1:y2, x1:x2]))

        return faces

    def classify_emotion(self, face_bgr):
        """
        Klasszifikálja a kivágott arcot a FERPlus modellel.
        Visszaad: (top_index, top_label, top_prob, all_probs)
        """
        gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (64, 64)).astype(np.float32)
        inp = resized.reshape(1, 1, 64, 64)

        logits = self.emotion_sess.run(None, {"Input3": inp})[0][0]
        # Stabil Softmax
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)

        top_idx = int(np.argmax(probs))
        top_name, top_emoji, top_color = EMOTION_LABELS[top_idx]
        top_prob = float(probs[top_idx])

        return top_idx, top_name, top_emoji, top_color, top_prob, probs


class EmotionApp:
    def __init__(self):
        print("\n========================================================")
        print("   Valós Idejű Arckifejezés- és Érzelemfelismerő Rendszer")
        print("   (100% Nyílt Forráskódú, Helyi AMD Ryzen 5 Inferencia)")
        print("========================================================")

        yolo_path = r"C:\uni_stuff\anti_thesis\yolov8n-pose.pt"
        onnx_path = r"C:\uni_stuff\anti_thesis\emotion-ferplus-8.onnx"

        self.pipeline = FaceEmotionPipeline(yolo_path, onnx_path)

        print("[Kamera keresése...]")
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
                        print(f"[OK] Webkamera sikeresen megnyitva (Index: {idx})!")
                        break
                if self.cap is not None:
                    break
                c.release()

        self.use_synthetic = (self.cap is None)
        if self.use_synthetic:
            print("[INFO] Élő kamera hiányában szintetikus tesztmód aktiválva.")

        # Felhasználói felület (Tkinter)
        self.root = tk.Tk()
        self.root.title("Arckifejezés és Érzelemfelismerő Modul (YOLOv8 + FERPlus ONNX)")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.configure(bg="#0F172A")

        # Felső fejléc
        lbl_head = tk.Label(
            self.root,
            text="🎭 ARCKIFEJEZÉS- ÉS ÉRZELEMELEMZŐ (100% HELYI ÉS INGYENES)",
            font=("Segoe UI", 13, "bold"),
            bg="#1E293B",
            fg="#38BDF8",
            pady=8
        )
        lbl_head.pack(fill=tk.X)

        # Fő konténer: Balra a videó, jobbra az érzelem-statisztika sávok
        main_frame = tk.Frame(self.root, bg="#0F172A")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Videó keret
        self.lbl_video = tk.Label(main_frame, bg="#000000")
        self.lbl_video.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Jobb oldali statisztikai sáv
        stat_frame = tk.Frame(main_frame, bg="#1E293B", width=280, padx=15, pady=15)
        stat_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        stat_frame.pack_propagate(False)

        tk.Label(
            stat_frame,
            text="Domináns Érzelem",
            font=("Segoe UI", 11, "bold"),
            bg="#1E293B",
            fg="#94A3B8"
        ).pack(anchor="w", pady=(0, 4))

        self.lbl_dominant = tk.Label(
            stat_frame,
            text="😐 Keresés...",
            font=("Segoe UI", 16, "bold"),
            bg="#334155",
            fg="#FFFFFF",
            pady=8
        )
        self.lbl_dominant.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            stat_frame,
            text="Érzelmi Valószínűségek",
            font=("Segoe UI", 10, "bold"),
            bg="#1E293B",
            fg="#94A3B8"
        ).pack(anchor="w", pady=(0, 8))

        # Érzelem sávok
        self.prob_bars = {}
        for name, emoji, color in EMOTION_LABELS:
            row = tk.Frame(stat_frame, bg="#1E293B")
            row.pack(fill=tk.X, pady=3)

            lbl_txt = tk.Label(
                row,
                text=f"{emoji} {name[:12]}",
                font=("Consolas", 9),
                bg="#1E293B",
                fg="#E2E8F0",
                width=14,
                anchor="w"
            )
            lbl_txt.pack(side=tk.LEFT)

            # Százalékos érték
            lbl_val = tk.Label(
                row,
                text="0%",
                font=("Consolas", 9, "bold"),
                bg="#1E293B",
                fg="#38BDF8",
                width=6,
                anchor="e"
            )
            lbl_val.pack(side=tk.RIGHT)

            self.prob_bars[name] = lbl_val

        # Alsó telemetria
        self.lbl_telemetry = tk.Label(
            self.root,
            text="Telemetria inicializálás...",
            font=("Consolas", 10),
            bg="#0284C7",
            fg="#FFFFFF",
            pady=6
        )
        self.lbl_telemetry.pack(fill=tk.X)

        self.prev_time = time.time()
        self.fps_buffer = []
        self.running = True

        self.update_loop()
        self.root.mainloop()

    def update_loop(self):
        if not self.running:
            return

        # 1. Képkocka olvasása
        if not self.use_synthetic and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Webkamera nem elerheto", (140, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # 2. Arckivágás és Érzelemelemzés
        t0 = time.time()
        faces = self.pipeline.extract_face_crops(frame)
        detection_ms = (time.time() - t0) * 1000.0

        dominant_text = "😐 Nincs arc a képen"
        dominant_bg = "#334155"
        all_probs_to_show = np.zeros(8)

        if len(faces) > 0:
            for (bbox, face_crop) in faces:
                x1, y1, x2, y2 = bbox
                t_cls = time.time()
                top_idx, top_name, top_emoji, top_color, top_prob, probs = self.pipeline.classify_emotion(face_crop)
                all_probs_to_show = probs

                dominant_text = f"{top_emoji} {top_name}\n({top_prob*100:.1f}%)"
                dominant_bg = top_color

                # Rajzolás a képre: Keret az arc körül
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 200), 3)

                # Névtábla az arc felett
                tag_str = f"{top_emoji} {top_name} ({int(top_prob*100)}%)"
                cv2.putText(frame, tag_str, (x1, max(25, y1 - 10)),
                            cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 200), 2)
                break  # Az első, legfőbb arcot jelenítjük meg a statisztikában

        # Statisztikai GUI frissítése
        self.lbl_dominant.config(text=dominant_text, bg=dominant_bg)
        for (name, emoji, color), p in zip(EMOTION_LABELS, all_probs_to_show):
            self.prob_bars[name].config(text=f"{p*100:4.1f}%")

        # FPS számítás
        curr_time = time.time()
        dt = curr_time - self.prev_time
        fps = 1.0 / dt if dt > 0 else 30.0
        self.prev_time = curr_time
        self.fps_buffer.append(fps)
        if len(self.fps_buffer) > 15:
            self.fps_buffer.pop(0)
        avg_fps = np.mean(self.fps_buffer)

        telemetry_text = (
            f"FPS: {avg_fps:.1f}  |  Detekció: {detection_ms:.1f} ms  |  "
            f"Hardver: AMD Ryzen 5 CPU (Helyi ONNX + YOLO)  |  Költség: 0 Ft"
        )
        self.lbl_telemetry.config(text=telemetry_text)

        # Kép konverzió Tkinter formátumra
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
        print("[OK] Arckifejezés felismerő alkalmazás bezárva.")


if __name__ == "__main__":
    EmotionApp()
