# -*- coding: utf-8 -*-
"""
Hello World Webkamera Teszt - YOLOv8-Pose Emberi Pózbecslés
Hardver: AMD Ryzen 5 5500 CPU optimalizációval
Támogatás: Intelligens kamerakereső szenzor-bemelegítéssel + Tkinter natív ablak fallback
"""

import sys
import time
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

print("=" * 65)
print("  SZAKDOLGOZATI PÓZBECSLÉS TESZT (YOLOv8n-pose)")
print("  Hardver: CPU inferencia (AMD Ryzen 5)")
print("=" * 65)

try:
    from ultralytics import YOLO
except ImportError:
    print("\n[HIBA] Az 'ultralytics' csomag nincs telepítve!")
    print("Telepítéshez futtasd: pip install ultralytics opencv-python pillow\n")
    sys.exit(1)

# 1. Modell betöltése (~6 MB-os nano pózbecslő)
MODEL_NAME = "yolov8n-pose.pt"
print(f"\n[1/3] '{MODEL_NAME}' modell betöltése...")
t_start = time.time()
model = YOLO(MODEL_NAME)
print(f"[OK] Modell sikeresen betöltve {time.time() - t_start:.2f} másodperc alatt.")

# 2. Intelligens kamerakeresés és bemelegítés
print("\n[2/3] Webkamera keresése és szenzor bemelegítése...")

def find_working_camera():
    backends = [
        ("DirectShow (CAP_DSHOW)", cv2.CAP_DSHOW),
        ("Alapértelmezett (CAP_ANY)", cv2.CAP_ANY)
    ]
    for b_name, b_code in backends:
        for idx in [0, 1, 2, 3]:
            try:
                cap = cv2.VideoCapture(idx, b_code)
                if not cap.isOpened():
                    continue
                # Sok laptop kamerájának (pl. Lenovo, HP, Asus) 200-400 ms kell a bekapcsoláshoz
                for _ in range(8):
                    time.sleep(0.08)
                    ret, frame = cap.read()
                    if ret and frame is not None and frame.size > 0:
                        print(f"[OK] Működő webkamera megtalálva! (Index: {idx}, Backend: {b_name})")
                        return cap, idx
                cap.release()
            except Exception:
                pass
    return None, -1

cap, working_idx = find_working_camera()

if cap is None:
    print("\n" + "!" * 65)
    print(" [FIGYELMEZTETÉS] Élő webkamera hardveresen nem válaszol!")
    print(" Gyakori laptop-specifikus okok és azonnali megoldások:")
    print(" 1. Windows Adatvédelem tiltja a kamerát:")
    print("    -> Gépház -> Adatvédelem és biztonság -> Kamera.")
    print("    -> Kapcsold BE: 'Kamera elérése' és 'Asztali alkalmazások hozzáférése'!")
    print(" 2. Fizikai lencsevédő retesz:")
    print("    -> A képernyő tetején húzd el a kis műanyag csúszkát (shutter)!")
    print(" 3. Billentyűzet kamera-gomb (Fn gomb):")
    print("    -> Nézd meg az F-billentyűket (pl. Fn + F10 / Fn + F6 áthúzott kamera ikon).")
    print("!" * 65)
    print("\n[INFO] Szintetikus tesztmód aktiválása (Mesterséges képkockák elemzése)...")
    use_synthetic = True
else:
    use_synthetic = False
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("\n[3/3] Grafikus megjelenítő indítása...")

# Teszteljük az OpenCV imshow-t
use_opencv_gui = True
try:
    dummy = np.zeros((10, 10, 3), dtype=np.uint8)
    cv2.imshow("test_probe", dummy)
    cv2.destroyWindow("test_probe")
except Exception:
    use_opencv_gui = False
    print("[INFO] Natív Tkinter ablakkezelő aktiválva a megjelenítéshez.")

# ----------------- TKINTER MEGJELENÍTŐ -----------------
class PoseAppTkinter:
    def __init__(self, cap, model, use_synthetic=False):
        self.cap = cap
        self.model = model
        self.use_synthetic = use_synthetic
        
        self.root = tk.Tk()
        self.root.title("Szakdolgozat - YOLOv8-Pose Webkamera Teszt (AMD Ryzen 5)")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.lbl_video = tk.Label(self.root)
        self.lbl_video.pack()
        
        self.lbl_info = tk.Label(
            self.root, 
            text="Inicializálás...", 
            font=("Calibri", 12, "bold"), 
            bg="#1B365D", 
            fg="white", 
            pady=8
        )
        self.lbl_info.pack(fill=tk.X)
        
        self.prev_time = time.time()
        self.fps_buffer = []
        self.running = True
        
        self.update_frame()
        self.root.mainloop()

    def update_frame(self):
        if not self.running:
            return
            
        if not self.use_synthetic and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, "Kamera adatfolyam megszakadt", (80, 240), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Webkamera nem elerheto (Ellenorizd a kameravedelmet!)", (30, 220), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
            cv2.putText(frame, "Modell: YOLOv8n-pose | Hardver: AMD Ryzen 5", (30, 260), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (200, 200, 200), 1)

        t0 = time.time()
        results = self.model(frame, verbose=False, conf=0.45)
        inference_ms = (time.time() - t0) * 1000.0

        curr_time = time.time()
        dt = curr_time - self.prev_time
        self.prev_time = curr_time
        fps = 1.0 / dt if dt > 0 else 30.0
        self.fps_buffer.append(fps)
        if len(self.fps_buffer) > 20:
            self.fps_buffer.pop(0)
        avg_fps = np.mean(self.fps_buffer)

        annotated = results[0].plot()
        num_persons = len(results[0].boxes) if results[0].boxes is not None else 0

        info_text = f"FPS: {avg_fps:.1f}  |  Inferencia: {inference_ms:.1f} ms (Ryzen 5 CPU)  |  Eszlelt szemely: {num_persons}"
        self.lbl_info.config(text=info_text)

        rgb_img = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)
        img_tk = ImageTk.PhotoImage(image=pil_img)
        
        self.lbl_video.img_tk = img_tk
        self.lbl_video.configure(image=img_tk)
        
        self.root.after(10, self.update_frame)

    def on_close(self):
        self.running = False
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()
        print("\n[OK] Alkalmazás leállítva.")

# ----------------- OPENCV GUI -----------------
def run_opencv_loop(cap, model):
    prev_time = time.time()
    fps_buffer = []
    print("-> Kilépéshez nyomd meg a 'Q' billentyűt a képablakon!\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        t0 = time.time()
        results = model(frame, verbose=False, conf=0.45)
        inference_ms = (time.time() - t0) * 1000.0
        
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 30.0
        prev_time = curr_time
        fps_buffer.append(fps)
        if len(fps_buffer) > 20:
            fps_buffer.pop(0)
        avg_fps = np.mean(fps_buffer)
        
        annotated = results[0].plot()
        num_persons = len(results[0].boxes) if results[0].boxes is not None else 0
        
        h, w, _ = annotated.shape
        cv2.rectangle(annotated, (0, 0), (w, 50), (20, 30, 45), -1)
        cv2.putText(annotated, f"FPS: {avg_fps:.1f} | Inferencia: {inference_ms:.1f} ms (Ryzen 5) | Szemely: {num_persons}", 
                    (20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 128), 2)
                    
        cv2.imshow("Szakdolgozat - YOLOv8-Pose Webkamera Teszt", annotated)
        if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q'), 27]:
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("\n[OK] Webkamera leállítva.")

if use_opencv_gui and not use_synthetic:
    run_opencv_loop(cap, model)
else:
    PoseAppTkinter(cap, model, use_synthetic=use_synthetic)
