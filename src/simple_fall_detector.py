# -*- coding: utf-8 -*-
"""
Egyszerű Kinematikai Esésdetektáló Rendszer (Baseline 1 Modell - V2 Javított)
Téma: Gráf alapú viselkedéselemzés - Esésdetektálás
Hardver: AMD Ryzen 5 CPU optimalizációval (YOLOv8-Pose)
Készítette: Szakdolgozó Hallgató

Javítások az előző verzióhoz képest:
1. Skálainvariáns normalizálás: ref_size = max(box_w, box_h), megszűnt a földön fekve felkeléskor
   fellépő zéró-osztó/törpe-magasság miatti sebesség-robbanás (amely a felkelést esésnek nézte).
2. Előjel-helyes sebesség: lefelé mozgás (zuhanás: vy > 0) különválasztva a felfelé mozgástól (felkelés: vy < 0).
3. Posture-persistence (tartós fekvés detektálás): ha valaki lassabban esik el vagy a földön fekszik
   (torso_angle > 55° VAGY W/H > 1.1) több mint 0.6 másodpercig, azonnal esést jelez, nem igényel
   irreálisan gyors zuhanást.
4. Megbízható kulcspont-kezelés: hip/shoulder confidence vizsgálat, zajszűrés.
5. Vizuális visszajelzés: gerincvektor és testtartás megjelenítése a képernyőn.
"""

import sys
import time
import math
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

try:
    from ultralytics import YOLO
except ImportError:
    print("[HIBA] Az 'ultralytics' nincs telepítve! Futtasd: pip install ultralytics")
    sys.exit(1)


# ----------------- KINEMATIKAI ÉS ESÉSDETEKTÁLÓ OSZTÁLY -----------------
class KinematicFallDetector:
    def __init__(self):
        # [(timestamp, com_x, com_y, box_h)]
        self.history = []
        self.state = "NORMAL"  # NORMAL, WARNING, DROP_DETECTED, FALLEN
        self.baseline_height = None
        self.unstable_counter = 0
        self.track_frames = 0
        self.drop_time = None
        self.warning_time = None
        self.fall_confirmed_time = None
        self.last_seen_time = None
        self.last_bbox = None
        self.time_on_floor = 0.0

    def reset(self):
        self.history.clear()
        self.state = "NORMAL"
        self.baseline_height = None
        self.unstable_counter = 0
        self.track_frames = 0
        self.drop_time = None
        self.warning_time = None
        self.fall_confirmed_time = None
        self.last_seen_time = None
        self.last_bbox = None
        self.time_on_floor = 0.0

    def handle_disappearance(self, current_time=None, frame_w=720):
        """
        Kezeli azokat az eseteket, amikor a YOLOv8 teljesen elveszíti a célpontot
        (pl. földre esés után a járókeret vagy bútor kitakarja a személyt).
        Kiszűri a látómező szélén történő normál távozást (FOV edge exit).
        """
        if current_time is None:
            current_time = time.time()

        if self.state == "FALLEN":
            if self.fall_confirmed_time is not None:
                self.time_on_floor = current_time - self.fall_confirmed_time
            return "FALLEN", "EMBER A PADLON (TAKARASBAN)"

        # Kép széle kilépés szűrése (ha kiment az ajtón / kamera szélén távozott)
        is_edge_exit = False
        if self.last_bbox is not None:
            bx1, _, bx2, _ = self.last_bbox
            if bx1 < 30 or bx2 > (frame_w - 30):
                is_edge_exit = True

        if not is_edge_exit:
            if (self.drop_time and current_time - self.drop_time <= 1.5) or \
               (self.state in ["WARNING", "DROP_DETECTED"] and self.warning_time and current_time - self.warning_time <= 1.2):
                self.state = "FALLEN"
                self.fall_confirmed_time = current_time
                return "FALLEN", "HIRTELEN ELTUNES ZUHANAS UTAN"

        return self.state, None

    def update(self, keypoints, bbox, current_time=None, frame_w=720, frame_h=480):
        """
        keypoints: (17, 3) tömb [x, y, conf]
        bbox: [x1, y1, x2, y2]
        current_time: opcionális szinkronizált videó időbélyeg másodpercben
        frame_w, frame_h: képkocka felbontása (ajtón belépés és pultmagasság szűréshez)
        Visszaad: (state, info_dict)
        """
        if current_time is None:
            current_time = time.time()
        curr_time = current_time

        x1, y1, x2, y2 = bbox
        box_w = max(1.0, float(x2 - x1))
        box_h = max(1.0, float(y2 - y1))
        aspect_ratio = box_w / box_h  # Állás: 0.3 - 0.6, Fekvés: > 1.15

        # Ha a szoba üres volt több mint 1.5 másodpercig (új belépő a képbe):
        if self.last_seen_time is not None and (curr_time - self.last_seen_time) > 1.5:
            self.baseline_height = None
            self.unstable_counter = 0
            self.track_frames = 0
            self.drop_time = None
            self.warning_time = None
            if self.state != "FALLEN":
                self.state = "NORMAL"

        self.track_frames += 1
        self.last_seen_time = curr_time
        self.last_bbox = bbox

        # Kép széle érintettség: ha a személy a képkeret határán van (ajtón belépés):
        touches_edge = (x1 <= 15 or x2 >= (frame_w - 15) or y1 <= 10)
        is_entering = touches_edge and (self.track_frames < 12)

        # 1. Ízületek kiolvasása (COCO-17 kulcspontok)
        l_sh, r_sh = keypoints[5], keypoints[6]
        l_hip, r_hip = keypoints[11], keypoints[12]
        l_ank, r_ank = keypoints[15], keypoints[16]

        sh_conf = min(l_sh[2], r_sh[2])
        hip_conf = min(l_hip[2], r_hip[2])
        ank_conf = min(l_ank[2], r_ank[2])
        has_legs = ank_conf > 0.25 and hip_conf > 0.25

        sh_center_x = (l_sh[0] + r_sh[0]) / 2.0
        sh_center_y = (l_sh[1] + r_sh[1]) / 2.0
        hip_center_x = (l_hip[0] + r_hip[0]) / 2.0
        hip_center_y = (l_hip[1] + r_hip[1]) / 2.0
        ank_center_y = (l_ank[1] + r_ank[1]) / 2.0

        # Súlypont (Center of Mass - CoM):
        if hip_conf > 0.35:
            com_y = hip_center_y
            com_x = hip_center_x
        elif sh_conf > 0.35:
            com_y = sh_center_y
            com_x = sh_center_x
        else:
            com_y = (y1 + y2) / 2.0
            com_x = (x1 + x2) / 2.0

        # Álló magasság becslése: CSAK akkor kalibráljuk ha a test nem a kép szélén vágott
        # és nem pult/bútor mögött vagy ülve/fekve emelkedik el a padlótól!
        is_elevated = (y2 < frame_h * 0.70)
        if not touches_edge and not is_elevated and aspect_ratio < 0.65:
            if self.baseline_height is None:
                self.baseline_height = box_h
            elif self.state == "NORMAL" and box_h > self.baseline_height * 0.75:
                self.baseline_height = 0.95 * self.baseline_height + 0.05 * box_h

        effective_baseline = self.baseline_height if self.baseline_height else box_h
        height_ratio = box_h / max(50.0, effective_baseline)
        ref_size = max(box_w, box_h, 50.0)

        # 2. Skálainvariáns gerinc dőlésszög számítása (Coronal Roll + Sagittal Pitch)
        torso_vector = None
        roll_angle = 0.0
        torso_ratio = 0.28
        if sh_conf > 0.25 and hip_conf > 0.25:
            dx = sh_center_x - hip_center_x
            dy = abs(sh_center_y - hip_center_y)
            roll_angle = math.degrees(math.atan2(abs(dx), dy + 1e-5))
            torso_ratio = dy / max(1.0, box_h)
            torso_vector = (int(hip_center_x), int(hip_center_y), int(sh_center_x), int(sh_center_y))
        else:
            roll_angle = min(90.0, max(0.0, (aspect_ratio - 0.45) * 80.0))

        # Sagittális hajlás becslése: normál állásnál dy/box_h ~ 0.26 - 0.32
        pitch_angle = 0.0
        if torso_ratio < 0.16:
            pitch_angle = min(80.0, (0.16 - torso_ratio) / 0.12 * 60.0)

        torso_angle = max(roll_angle, pitch_angle)

        # 3. Vertikális sebesség számítása (lefelé pozitív)
        self.history.append((curr_time, com_x, com_y, box_h))
        self.history = [h for h in self.history if curr_time - h[0] <= 0.5]

        drop_velocity = 0.0
        if len(self.history) >= 2:
            oldest_t, oldest_x, oldest_y, _ = self.history[0]
            dt = curr_time - oldest_t
            if dt > 0.08 and abs(com_x - oldest_x) < (ref_size * 1.5):
                pixel_diff = com_y - oldest_y
                drop_velocity = (pixel_diff / ref_size) / dt

        # 4. Biomechanikai és Anatómiai Osztályozás

        # A) ÜLŐ TESTHELYZET (Szék / fotel / kanapé):
        is_seated = False
        if has_legs and (ank_center_y - hip_center_y > 20) and (hip_center_y - sh_center_y > 25) and aspect_ratio < 1.15:
            is_seated = True
        elif (0.35 < height_ratio < 0.75) and (torso_angle < 25.0) and (drop_velocity < 0.20):
            is_seated = True

        # B) KONYHAPULT / ASZTAL FELETTI GÖRNYEDÉS / HAJOLÁS (Counter Leaning):
        # Ha a test alsó határa magasan van a padló felett (y2 < 0.72 * frame_h),
        # nincs lefelé zuhanási sebesség (drop_velocity < 0.25) és nem előzte meg zuhanás:
        is_counter_leaning = False
        if (y2 < frame_h * 0.72) and (drop_velocity < 0.25) and (self.drop_time is None) and not has_legs:
            is_counter_leaning = True

        # C) KANAPÉ / FOTEL / ÁGY / BÚTORON ELTERÜLÉS VAGY FEKVÉS (Furniture Lounging / Resting):
        # A test alsó része magasan van a padló felett (y2 < frame_h * 0.70), és nincs lefelé zuhanási sebesség
        is_furniture_resting = False
        if (y2 < frame_h * 0.70) and (abs(drop_velocity) < 0.28):
            if (torso_angle > 28.0) or (aspect_ratio > 0.95) or is_seated:
                is_furniture_resting = True

        # D) FÖLDÖN ÖSSZEOMLÁS / FEKVÉS (FALLEN):
        # Valós padlóra zuhanás feltétele: a test alsó része leér a padlózónába (y2 >= 0.70 * frame_h)
        is_near_floor = (y2 >= frame_h * 0.70)

        if is_entering or is_furniture_resting or is_counter_leaning:
            # Ha épp most lép be az ajtón/szélen, bútoron pihen vagy pultra hajol: nem padlóra zuhanás
            is_floor_collapse = False
            is_floor_horizontal = False
        else:
            is_floor_collapse = (height_ratio < 0.52 and torso_angle > 35.0 and is_near_floor and not is_seated)
            is_floor_horizontal = (aspect_ratio > 1.25 and torso_angle > 45.0 and is_near_floor)

        # E) KÖZTES ESÉSVESZÉLY / INSTABILITÁS (WARNING):
        raw_unstable = (
            (torso_angle > 40.0) or
            (torso_angle > 30.0 and (drop_velocity > 0.22 or height_ratio < 0.75)) or
            (drop_velocity > 0.35)
        ) and not is_seated and not is_counter_leaning and not is_entering and not is_furniture_resting

        # Időbeli hiszterézis: 3 egymást követő képkocka kell a riasztáshoz
        if raw_unstable:
            self.unstable_counter += 1
        else:
            self.unstable_counter = max(0, self.unstable_counter - 1)

        is_unstable = (self.unstable_counter >= 3)

        # F) STABIL ÁLLÓ / BIZTONSÁGOS HELYZET (NORMAL):
        is_upright = (torso_angle < 22.0) and (aspect_ratio < 0.75) and (height_ratio > 0.78 or is_seated or is_counter_leaning or is_furniture_resting)

        # 5. Döntési Állapotgép
        if self.state == "FALLEN":
            if is_upright and not is_floor_collapse:
                self.state = "NORMAL"
                self.fall_confirmed_time = None
                self.time_on_floor = 0.0
            else:
                if self.fall_confirmed_time is not None:
                    self.time_on_floor = curr_time - self.fall_confirmed_time

        elif self.state in ["NORMAL", "WARNING", "DROP_DETECTED"]:
            # 1. Prioritás: Tényleges esés / padlóra zuhanás
            if is_floor_collapse or is_floor_horizontal:
                self.state = "FALLEN"
                self.fall_confirmed_time = curr_time
            elif self.state == "DROP_DETECTED" and height_ratio < 0.65 and (torso_angle > 32.0 or aspect_ratio > 0.90) and is_near_floor and not is_seated and not is_furniture_resting:
                self.state = "FALLEN"
                self.fall_confirmed_time = curr_time
            elif drop_velocity > 0.35 and torso_angle > 38.0 and is_near_floor and not is_seated and not is_counter_leaning and not is_furniture_resting and not is_entering:
                self.state = "FALLEN"
                self.fall_confirmed_time = curr_time

            # 2. Prioritás: Zuhanási fázis (Impact előtt)
            elif drop_velocity > 0.45 and not is_seated and not is_counter_leaning and not is_furniture_resting and not is_entering:
                self.state = "DROP_DETECTED"
                self.drop_time = curr_time

            # 3. Prioritás: Köztes esésveszély / egyensúlyvesztés
            elif is_unstable:
                self.state = "WARNING"
                self.warning_time = curr_time

            # 4. Prioritás: Biztonságos normál mozgás / Riasztás lecsengése
            else:
                if self.state == "DROP_DETECTED" and (curr_time - (self.drop_time or 0) > 0.8):
                    self.state = "NORMAL"
                    self.drop_time = None
                elif self.state == "WARNING":
                    if (curr_time - (self.warning_time or 0) > 0.5) or is_upright or is_seated or is_counter_leaning or is_furniture_resting:
                        self.state = "NORMAL"
                        self.drop_time = None
                elif is_upright or is_seated or is_counter_leaning or is_furniture_resting or is_entering:
                    self.state = "NORMAL"
                    self.drop_time = None

        info = {
            "drop_velocity": drop_velocity,
            "torso_angle": torso_angle,
            "roll_angle": roll_angle,
            "aspect_ratio": aspect_ratio,
            "height_ratio": height_ratio,
            "time_on_floor": self.time_on_floor,
            "is_unstable": is_unstable,
            "is_seated": is_seated,
            "is_counter_leaning": is_counter_leaning,
            "is_furniture_resting": is_furniture_resting,
            "is_entering": is_entering,
            "is_upright": is_upright,
            "torso_vector": torso_vector,
            "com": (int(com_x), int(com_y))
        }
        return self.state, info


# ----------------- GRAFIKUS ALKALMAZÁS (TKINTER) -----------------
class FallDetectionApp:
    def __init__(self):
        print("\n========================================================")
        print("  Szakdolgozati Rendszer - Valós Idejű Esésdetektáló V2")
        print("========================================================")
        print("[1/3] YOLOv8n-pose modell betöltése...")
        self.model = YOLO("yolov8n-pose.pt")
        self.detector = KinematicFallDetector()

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
            print("[FIGYELEM] Élő webkamera nem elérhető, szintetikus háttérrel indul.")

        print("[3/3] GUI Ablak felépítése...")
        self.root = tk.Tk()
        self.root.title("Szakdolgozat: Esésdetektálás Baseline V2 (Javított Kinematika)")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Fő videó keret
        self.lbl_video = tk.Label(self.root, bg="#111111")
        self.lbl_video.pack(fill=tk.BOTH, expand=True)

        # Állapotsáv (Fő vizuális jelző)
        self.lbl_status = tk.Label(
            self.root,
            text="FIGYELÉS AKTÍV: NORMÁL ÁLLAPOT",
            font=("Segoe UI", 16, "bold"),
            bg="#2E7D32",  # Zöld
            fg="white",
            pady=12
        )
        self.lbl_status.pack(fill=tk.X)

        # Telemetria és Részletes diagnosztika sáv
        self.lbl_telemetry = tk.Label(
            self.root,
            text="Telemetria inicializálás...",
            font=("Consolas", 11),
            bg="#0F172A",
            fg="#38BDF8",
            pady=8
        )
        self.lbl_telemetry.pack(fill=tk.X)

        # Vezérlőgombok
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

        self.lbl_posture_badge = tk.Label(
            btn_frame,
            text="Tartás: ÁLLÁS",
            font=("Segoe UI", 10, "bold"),
            bg="#334155",
            fg="#F8FAFC",
            padx=10,
            pady=4
        )
        self.lbl_posture_badge.pack(side=tk.RIGHT, padx=15)

        self.prev_time = time.time()
        self.fps_buffer = []
        self.running = True

        self.update_loop()
        self.root.mainloop()

    def reset_detector(self):
        self.detector.reset()
        print("[INFO] Detektor állapot manuálisan visszaállítva.")

    def update_loop(self):
        if not self.running:
            return

        # 1. Képkocka beolvasása
        if not self.use_synthetic and self.cap is not None:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Webkamera nem elerheto", (140, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # 2. YOLOv8n-pose inferencia
        t0 = time.time()
        results = self.model(frame, verbose=False, conf=0.40)
        inference_ms = (time.time() - t0) * 1000.0

        # FPS számítás
        curr_time = time.time()
        dt = curr_time - self.prev_time
        fps = 1.0 / dt if dt > 0 else 30.0
        self.prev_time = curr_time
        self.fps_buffer.append(fps)
        if len(self.fps_buffer) > 15:
            self.fps_buffer.pop(0)
        avg_fps = np.mean(self.fps_buffer)

        # 3. Kiértékelés
        annotated_frame = results[0].plot()
        current_state = "NORMAL"
        info = {
            "drop_velocity": 0.0,
            "torso_angle": 0.0,
            "aspect_ratio": 0.0,
            "time_on_floor": 0.0,
            "is_horizontal": False,
            "is_upright": True,
            "torso_vector": None,
            "com": None
        }

        if len(results[0].boxes) > 0 and results[0].keypoints is not None:
            bbox = results[0].boxes.xyxy[0].cpu().numpy()
            kpts = results[0].keypoints.data[0].cpu().numpy()
            current_state, info = self.detector.update(kpts, bbox, frame_w=frame.shape[1], frame_h=frame.shape[0])

            # Rajzoljunk diagnosztikai vizualizációt a képre:
            # Súlypont (CoM) pontja
            if info["com"] is not None:
                cv2.circle(annotated_frame, info["com"], 7, (0, 255, 255), -1)

            # Gerincvektor kirajzolása színkóddal
            if info["torso_vector"] is not None:
                hx, hy, sx, sy = info["torso_vector"]
                if info["torso_angle"] > 55.0:
                    vec_color = (0, 0, 255)  # Piros (Vízszintes/Fekvő)
                elif info["torso_angle"] > 35.0:
                    vec_color = (0, 215, 255)  # Sárga (Hajlott/Ülő)
                else:
                    vec_color = (0, 255, 0)  # Zöld (Függőleges/Álló)
                cv2.line(annotated_frame, (hx, hy), (sx, sy), vec_color, 4)

        # 4. GUI Állapot és Vizuális Riasztás Frissítése
        h, w, _ = annotated_frame.shape

        if current_state == "FALLEN":
            status_text = f"🚨 VÉSZHELYZET: ESÉS ÉSZLELVE! (Földön: {info['time_on_floor']:.1f} mp)"
            status_bg = "#B91C1C"  # Élénkpiros
            posture_text = "Tartás: FEKVŐ (FÖLDÖN)"
            posture_bg = "#991B1B"
            # Vastag piros villogó/figyelmeztető keret
            cv2.rectangle(annotated_frame, (0, 0), (w, h), (0, 0, 255), 14)
            cv2.putText(annotated_frame, "ESES / FEKVO HELYZET!", (30, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1.1, (0, 0, 255), 3)

        elif current_state == "DROP_DETECTED":
            status_text = "⚠️ GYORS ZUHANÁS ÉRZÉKELVE! (Kiértékelés...)"
            status_bg = "#D97706"  # Narancs/Sárga
            posture_text = "Tartás: ZUHANÁS FOLYAMATBAN"
            posture_bg = "#B45309"
            cv2.rectangle(annotated_frame, (0, 0), (w, h), (0, 165, 255), 8)

        else:
            status_text = "✅ BIZTONSÁGOS: NORMÁL MOZGÁSFORMÁK"
            status_bg = "#15803D"  # Zöld
            if info["is_upright"]:
                posture_text = "Tartás: EGYENES / ÁLLÁS"
                posture_bg = "#166534"
            elif info["torso_angle"] > 35.0:
                posture_text = "Tartás: HAJOLT / ÜLŐ"
                posture_bg = "#854D0E"
            else:
                posture_text = "Tartás: NORMÁL"
                posture_bg = "#334155"

        self.lbl_status.config(text=status_text, bg=status_bg)
        self.lbl_posture_badge.config(text=posture_text, bg=posture_bg)

        # Sebesség irány szöveg
        v_val = info["drop_velocity"]
        if v_val > 0.3:
            v_dir = f"LEFELÉ (+{v_val:.2f})"
        elif v_val < -0.3:
            v_dir = f"FELKELÉS / EMELKEDÉS ({v_val:.2f})"
        else:
            v_dir = f"STABIL ({v_val:.2f})"

        telemetry_text = (
            f"FPS: {avg_fps:.1f} | Inferencia: {inference_ms:.1f} ms | "
            f"Törzsszög: {info['torso_angle']:.1f}° | W/H arány: {info['aspect_ratio']:.2f} | "
            f"Sebesség: {v_dir}"
        )
        self.lbl_telemetry.config(text=telemetry_text)

        # OpenCV BGR -> PIL RGB -> Tkinter PhotoImage
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
        print("[OK] Esésdetektáló alkalmazás bezárva.")


if __name__ == "__main__":
    FallDetectionApp()
