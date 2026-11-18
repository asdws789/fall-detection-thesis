# -*- coding: utf-8 -*-
"""
Érintetlen Új Adathalmaz Kiértékelő és Tesztelő Felület (Unseen Benchmark Player)
Téma: Gráf alapú modellek és viselkedéselemzés - Esésdetektálás
Használat: Bármilyen külső, letöltött videó automatikus detektálása és tesztelése
Modellek: YOLOv8s-Pose (Small) és YOLOv8n-Pose (Nano)
Készítette: Szakdolgozó Hallgató (BSc Mérnökinformatikus)
"""

import os
import sys
import time
import math
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)

from simple_fall_detector import KinematicFallDetector

try:
    from ultralytics import YOLO
except ImportError:
    print("[HIBA] Az 'ultralytics' csomag nincs telepítve! Futtasd: pip install ultralytics")
    sys.exit(1)

# Megbeszélt célmappa az új, letöltött adathalmazok számára
UNSEEN_DIR = os.path.join(WORKSPACE_DIR, "data", "raw", "unseen_benchmark")
os.makedirs(UNSEEN_DIR, exist_ok=True)

MODELS = {
    "YOLOv8s-Pose (Small - 11.6M param, Nagyobb pontosság)": os.path.join(WORKSPACE_DIR, "yolov8s-pose.pt"),
    "YOLOv8n-Pose (Nano - 3.2M param, Nagyobb sebesség / RPi)": os.path.join(WORKSPACE_DIR, "yolov8n-pose.pt")
}

VIDEO_EXTENSIONS = (".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm", ".flv")


class UnseenBenchmarkApp:
    def __init__(self):
        print("\n" + "="*70)
        print("  Szakdolgozati Rendszer: Érintetlen Új Adathalmaz Kiértékelő")
        print("="*70)
        print(f"[INFO] Célmappa: {UNSEEN_DIR}")

        self.loaded_models = {}
        default_model_key = list(MODELS.keys())[0]
        self.current_model_key = default_model_key
        print(f"[1/2] Alapértelmezett modell betöltése: {self.current_model_key}...")
        self.model = self.get_or_load_model(default_model_key)
        self.detector = KinematicFallDetector()

        # Lejátszási állapotok
        self.is_running = True
        self.is_paused = False
        self.playback_speed = 1.0  # 1.0x, 0.5x, 1.5x
        self.cap = None
        self.frames = []
        self.current_frame_idx = 0
        self.total_frames = 0
        self.fps = 25.0
        self.current_type = None  # "video" vagy "folder"
        self.current_item_path = None
        self.fall_detected_at = None
        self.warning_detected_at = None
        self.last_known_bbox = None
        self.restarting = False

        print("[2/2] Grafikus felület (GUI) inicializálása...")
        self.init_gui()
        self.scan_unseen_folder()

        self.root.after(100, self.update_loop)

    def get_or_load_model(self, model_key):
        if model_key in self.loaded_models:
            return self.loaded_models[model_key]
        m_path = MODELS.get(model_key)
        if not os.path.exists(m_path):
            print(f"[FIGYELEM] Modell fájl nem található ({m_path}), letöltés az ultralytics-szel...")
            m_path = os.path.basename(m_path)
        m = YOLO(m_path)
        self.loaded_models[model_key] = m
        return m

    def open_unseen_folder(self):
        """Megnyitja a megbeszélt mappát a Windows Fájlkezelőben"""
        try:
            os.startfile(UNSEEN_DIR)
        except Exception as e:
            try:
                subprocess.Popen(["explorer", UNSEEN_DIR])
            except Exception as ex:
                messagebox.showerror("Hiba", f"Nem sikerült megnyitni a mappát: {e}")

    def scan_unseen_folder(self):
        """Átvizsgálja az unseen_benchmark mappát videók és képsorozatok után"""
        found_items = []

        if os.path.exists(UNSEEN_DIR):
            for root, dirs, files in os.walk(UNSEEN_DIR):
                # 1. Videofájlok keresése
                for file in files:
                    if file.lower().endswith(VIDEO_EXTENSIONS):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, UNSEEN_DIR)
                        size_mb = os.path.getsize(full_path) / (1024 * 1024)
                        found_items.append({
                            "display": f"🎥 {rel_path} ({size_mb:.1f} MB)",
                            "path": full_path,
                            "type": "video"
                        })

                # 2. Képkocka mappák keresése (ha egy almappa tele van képekkel)
                for d in dirs:
                    d_path = os.path.join(root, d)
                    imgs = [f for f in os.listdir(d_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
                    if len(imgs) >= 10:  # Legalább 10 képkocka
                        rel_path = os.path.relpath(d_path, UNSEEN_DIR)
                        found_items.append({
                            "display": f"📁 [Képsorozat] {rel_path} ({len(imgs)} képkocka)",
                            "path": d_path,
                            "type": "folder"
                        })

        self.items_map = {item["display"]: item for item in found_items}

        if found_items:
            options = [item["display"] for item in found_items]
            self.video_combo["values"] = options
            if self.video_combo.get() not in options:
                self.video_combo.current(0)
            self.lbl_folder_status.config(
                text=f"✅ {len(found_items)} tesztvideó/adathalmaz betöltve a mappából.",
                fg="#4ADE80"
            )
            self.load_selected_video()
        else:
            self.video_combo["values"] = ["(A mappa üres - másolj be videókat!)"]
            self.video_combo.current(0)
            self.lbl_folder_status.config(
                text="⚠️ A mappa még üres! Kattints a 'Mappa megnyitása' gombra és másolj be videókat!",
                fg="#FBBF24"
            )

    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("Szakdolgozat: Érintetlen Új Adathalmaz Kiértékelő (Unseen Benchmark)")
        self.root.geometry("1200x920")
        self.root.minsize(1000, 750)
        self.root.configure(bg="#0F172A")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground="#1E293B", background="#334155",
                        foreground="#F8FAFC", font=("Segoe UI", 10))

        # --- FELSŐ VEZÉRLŐPULT ---
        ctrl_frame = tk.Frame(self.root, bg="#1E293B", bd=0, padx=14, pady=12)
        ctrl_frame.pack(fill=tk.X, padx=12, pady=(12, 6))

        # 1. Sor: Célmappa infó és gombok
        row1 = tk.Frame(ctrl_frame, bg="#1E293B")
        row1.pack(fill=tk.X, pady=(0, 8))

        lbl_dir_title = tk.Label(row1, text="📂 Célmappa (Ide másold az új videóidat):",
                                 font=("Segoe UI", 10, "bold"), fg="#94A3B8", bg="#1E293B")
        lbl_dir_title.pack(side=tk.LEFT, padx=(0, 8))

        lbl_dir_path = tk.Label(row1, text=f"...\\data\\raw\\unseen_benchmark\\",
                                font=("Consolas", 10), fg="#38BDF8", bg="#0F172A", padx=8, pady=2)
        lbl_dir_path.pack(side=tk.LEFT, padx=(0, 10))

        btn_open_folder = tk.Button(row1, text="📂 Mappa megnyitása Intézőben",
                                    command=self.open_unseen_folder,
                                    font=("Segoe UI", 9, "bold"), bg="#0284C7", fg="white",
                                    relief=tk.FLAT, padx=10, pady=2, cursor="hand2")
        btn_open_folder.pack(side=tk.LEFT, padx=5)

        btn_refresh = tk.Button(row1, text="🔄 Lista Frissítése",
                                command=self.scan_unseen_folder,
                                font=("Segoe UI", 9, "bold"), bg="#475569", fg="white",
                                relief=tk.FLAT, padx=10, pady=2, cursor="hand2")
        btn_refresh.pack(side=tk.LEFT, padx=5)

        # 2. Sor: Videó kiválasztása és Modell kiválasztása
        row2 = tk.Frame(ctrl_frame, bg="#1E293B")
        row2.pack(fill=tk.X, pady=(0, 6))

        lbl_vid = tk.Label(row2, text="Tesztvideó kiválasztása:", font=("Segoe UI", 10, "bold"),
                           fg="#F8FAFC", bg="#1E293B")
        lbl_vid.pack(side=tk.LEFT, padx=(0, 8))

        self.video_combo = ttk.Combobox(row2, width=45, state="readonly")
        self.video_combo.pack(side=tk.LEFT, padx=(0, 20))
        self.video_combo.bind("<<ComboboxSelected>>", lambda e: self.load_selected_video())

        lbl_mod = tk.Label(row2, text="Modell:", font=("Segoe UI", 10, "bold"),
                           fg="#F8FAFC", bg="#1E293B")
        lbl_mod.pack(side=tk.LEFT, padx=(0, 8))

        self.model_combo = ttk.Combobox(row2, values=list(MODELS.keys()), width=40, state="readonly")
        self.model_combo.current(0)
        self.model_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.model_combo.bind("<<ComboboxSelected>>", self.on_model_change)

        # 3. Sor: Állapotkijelző és Lejátszás vezérlők
        row3 = tk.Frame(ctrl_frame, bg="#1E293B")
        row3.pack(fill=tk.X, pady=(4, 0))

        self.lbl_folder_status = tk.Label(row3, text="Mappa ellenőrzése...",
                                          font=("Segoe UI", 9, "italic"), fg="#94A3B8", bg="#1E293B")
        self.lbl_folder_status.pack(side=tk.LEFT)

        # Jobb oldali lejátszás gombok
        btn_restart = tk.Button(row3, text="⏮ Újraindítás", command=self.restart_video,
                                font=("Segoe UI", 9, "bold"), bg="#334155", fg="white",
                                relief=tk.FLAT, padx=10, pady=3, cursor="hand2")
        btn_restart.pack(side=tk.RIGHT, padx=4)

        self.btn_pause = tk.Button(row3, text="⏸ Szünet", command=self.toggle_pause,
                                  font=("Segoe UI", 9, "bold"), bg="#334155", fg="white",
                                  relief=tk.FLAT, padx=12, pady=3, cursor="hand2")
        self.btn_pause.pack(side=tk.RIGHT, padx=4)

        lbl_speed = tk.Label(row3, text="Sebesség:", font=("Segoe UI", 9), fg="#94A3B8", bg="#1E293B")
        lbl_speed.pack(side=tk.RIGHT, padx=(15, 4))

        self.speed_combo = ttk.Combobox(row3, values=["0.5x (Lassított)", "1.0x (Normál)", "1.5x (Gyors)", "2.0x (Dupla)"],
                                        width=16, state="readonly")
        self.speed_combo.current(1)
        self.speed_combo.pack(side=tk.RIGHT, padx=4)
        self.speed_combo.bind("<<ComboboxSelected>>", self.on_speed_change)

        # --- FŐ VIDEÓ MEGJELENÍTŐ KONTÉNER ---
        self.video_container = tk.Frame(self.root, bg="#000000", bd=2, relief=tk.SOLID)
        self.video_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        self.lbl_video = tk.Label(self.video_container, bg="#000000")
        self.lbl_video.pack(fill=tk.BOTH, expand=True)

        # --- ÁLLAPOTSÁV (4-LÉPCSŐS DETEKTÁLÁS) ---
        self.lbl_status = tk.Label(
            self.root,
            text="✅ BIZTONSÁGOS: NORMÁL MOZGÁS",
            font=("Segoe UI", 15, "bold"),
            bg="#15803D",
            fg="white",
            pady=10
        )
        self.lbl_status.pack(fill=tk.X, padx=12, pady=(0, 4))

        # --- RÉSZLETES TELEMETRIA ÉS INFORMÁCIÓS SÁV ---
        self.lbl_telemetry = tk.Label(
            self.root,
            text="Frame: 0/0 | Inferencia: -- ms | Térbeli dőlésszög: --° | W/H: -- | Zuhanás sebesség: --",
            font=("Consolas", 10),
            bg="#0F172A",
            fg="#94A3B8",
            pady=4
        )
        self.lbl_telemetry.pack(fill=tk.X, padx=12, pady=(0, 4))

        # --- TÖRTÉNETI ESEMÉNYNAPLÓ (LOG PANEL) ---
        log_frame = tk.Frame(self.root, bg="#1E293B", padx=10, pady=6)
        log_frame.pack(fill=tk.X, padx=12, pady=(0, 10))

        lbl_log_title = tk.Label(log_frame, text="📋 Eseménynapló (Detektált események a videóban):",
                                 font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B")
        lbl_log_title.pack(side=tk.LEFT, padx=(0, 10))

        self.lbl_log_events = tk.Label(log_frame, text="Még nem történt kritikus esemény ezen a videón.",
                                       font=("Consolas", 9), fg="#F8FAFC", bg="#1E293B")
        self.lbl_log_events.pack(side=tk.LEFT)

    def on_speed_change(self, event):
        val = self.speed_combo.get()
        if "0.5x" in val:
            self.playback_speed = 0.5
        elif "1.5x" in val:
            self.playback_speed = 1.5
        elif "2.0x" in val:
            self.playback_speed = 2.0
        else:
            self.playback_speed = 1.0

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.btn_pause.config(text="▶ Folytatás" if self.is_paused else "⏸ Szünet",
                              bg="#2563EB" if self.is_paused else "#334155")

    def on_model_change(self, event):
        new_key = self.model_combo.get()
        print(f"[INFO] Váltás modellre: {new_key}...")
        self.model = self.get_or_load_model(new_key)
        self.current_model_key = new_key
        self.restart_video()

    def load_selected_video(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        choice = self.video_combo.get()
        if choice not in self.items_map:
            return

        item = self.items_map[choice]
        target_path = item["path"]
        self.current_type = item["type"]
        self.current_item_path = target_path

        self.detector.reset()
        self.fall_detected_at = None
        self.warning_detected_at = None
        self.last_known_bbox = None
        self.current_frame_idx = 0
        self.frames = []
        self.restarting = False
        self.lbl_log_events.config(text="Videó betöltve. Elemzés folyamatban...", fg="#F8FAFC")

        if self.current_type == "folder":
            png_files = sorted([f for f in os.listdir(target_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
            self.frames = [os.path.join(target_path, f) for f in png_files]
            self.total_frames = len(self.frames)
            self.fps = 25.0
        else:
            self.cap = cv2.VideoCapture(target_path)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 25.0

    def restart_video(self):
        self.restarting = False
        self.current_frame_idx = 0
        self.fall_detected_at = None
        self.warning_detected_at = None
        self.last_known_bbox = None
        self.detector.reset()
        if self.cap is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.lbl_status.config(text="✅ BIZTONSÁGOS: NORMÁL MOZGÁS", bg="#15803D")

    def update_loop(self):
        if not self.is_running:
            return

        if self.is_paused:
            self.root.after(100, self.update_loop)
            return

        if self.total_frames == 0:
            self.root.after(200, self.update_loop)
            return

        # 1. Képkocka beolvasása
        frame = None
        if self.current_type == "folder":
            if self.current_frame_idx < len(self.frames):
                frame = cv2.imread(self.frames[self.current_frame_idx])
        else:
            if self.cap is not None and self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    frame = None

        # Videó vége kezelés
        if frame is None or self.current_frame_idx >= self.total_frames:
            if not self.restarting:
                self.restarting = True
                if self.fall_detected_at is not None:
                    summary = f"🚨 VÉGEREDMÉNY: Esés detektálva {self.fall_detected_at:.2f} mp-nél!"
                    fg_c = "#EF4444"
                else:
                    summary = "✅ VÉGEREDMÉNY: Nincs esés (Normál mozgás / ADL)."
                    fg_c = "#22C55E"
                self.lbl_log_events.config(text=summary, fg=fg_c)
                self.root.after(3000, self.restart_video)

            self.root.after(100, self.update_loop)
            return

        timestamp_sec = self.current_frame_idx / (self.fps if self.fps > 0 else 25.0)

        # 2. Skálázás ha túl nagy a felbontás
        orig_h, orig_w = frame.shape[:2]
        if orig_w > 720:
            scale = 720.0 / orig_w
            frame = cv2.resize(frame, (720, int(orig_h * scale)))

        # 3. YOLOv8 Inferencia
        t0 = time.time()
        results = self.model(frame, verbose=False, conf=0.25)
        dt_ms = (time.time() - t0) * 1000.0

        annotated_frame = results[0].plot()
        current_state = self.detector.state
        info_dict = {"torso_angle": 0.0, "aspect_ratio": 0.0, "drop_velocity": 0.0, "height_ratio": 1.0}

        if len(results[0].boxes) > 0 and results[0].keypoints is not None:
            best_idx = int(np.argmax(results[0].boxes.conf.cpu().numpy()))
            bbox = results[0].boxes.xyxy[best_idx].cpu().numpy()
            kpts = results[0].keypoints.data[best_idx].cpu().numpy()
            self.last_known_bbox = bbox
            current_state, info_dict = self.detector.update(
                kpts, bbox, current_time=timestamp_sec, frame_w=frame.shape[1], frame_h=frame.shape[0]
            )

            # Események naplózása
            if current_state == "WARNING" and self.warning_detected_at is None:
                self.warning_detected_at = timestamp_sec
                self.lbl_log_events.config(
                    text=f"⚠️ Esésveszély / Megdőlés érzékelve: {timestamp_sec:.2f} mp-nél ({info_dict['torso_angle']:.1f}°)",
                    fg="#F59E0B"
                )

            if current_state == "FALLEN" and self.fall_detected_at is None:
                self.fall_detected_at = timestamp_sec
                self.lbl_log_events.config(
                    text=f"🚨 KRITIKUS: ESÉS DETEKTÁLVA: {timestamp_sec:.2f} mp-nél!",
                    fg="#EF4444"
                )

            # Törzsgerinc vektor kirajzolása színkóddal
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
            # Ha eltűnik a célpont a padlónál (takarás, járókeret, bútor)
            current_state, reason = self.detector.handle_disappearance(current_time=timestamp_sec, frame_w=frame.shape[1])
            if current_state == "FALLEN" and self.fall_detected_at is None:
                self.fall_detected_at = timestamp_sec
                self.lbl_log_events.config(
                    text=f"🚨 ESÉS TAKARÁSBAN: {timestamp_sec:.2f} mp-nél ({reason})",
                    fg="#EF4444"
                )

            if current_state == "FALLEN" and self.last_known_bbox is not None:
                bx1, by1, bx2, by2 = [int(v) for v in self.last_known_bbox]
                cv2.rectangle(annotated_frame, (bx1, by1), (bx2, by2), (0, 0, 255), 3)
                cv2.putText(annotated_frame, "EMBER A PADLON (TAKARASBAN)", (bx1, max(20, by1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # 4. GUI Frissítése
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
            f"Térbeli dőlés: {info_dict['torso_angle']:.1f}° | W/H: {info_dict['aspect_ratio']:.2f} | "
            f"Sebesség: {info_dict['drop_velocity']:.2f}"
        )
        self.lbl_telemetry.config(text=telemetry)

        # 5. Kép igazítása a megjelenítőhöz (Dinamikus felskálázás a teljes ablakméret kitöltésére)
        container_w = self.video_container.winfo_width()
        container_h = self.video_container.winfo_height()
        if container_w < 100 or container_h < 100:
            container_w, container_h = 1000, 620

        fh, fw = annotated_frame.shape[:2]
        scale = min((container_w - 6) / fw, (container_h - 6) / fh)
        disp_w = max(10, int(fw * scale))
        disp_h = max(10, int(fh * scale))

        disp_frame = cv2.resize(annotated_frame, (disp_w, disp_h), interpolation=cv2.INTER_LINEAR)
        rgb = cv2.cvtColor(disp_frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        img_tk = ImageTk.PhotoImage(image=pil_img)
        self.lbl_video.img_tk = img_tk
        self.lbl_video.configure(image=img_tk)

        self.current_frame_idx += 1

        # Képkocka késleltetés a beállított sebesség szerint
        delay_ms = max(10, int(25 / self.playback_speed))
        self.root.after(delay_ms, self.update_loop)

    def on_close(self):
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()


def main():
    app = UnseenBenchmarkApp()
    app.root.mainloop()


if __name__ == "__main__":
    main()
