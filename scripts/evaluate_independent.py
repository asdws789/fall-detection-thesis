import os
import sys
import cv2
from ultralytics import YOLO

sys.path.insert(0, r"C:\uni_stuff\anti_thesis\src")
from simple_fall_detector import KinematicFallDetector

model_path = r"C:\uni_stuff\anti_thesis\yolov8n-pose.pt"
model = YOLO(model_path)
folder = r"C:\uni_stuff\anti_thesis\data\raw\independent_benchmark"

videos = [
    ("fall_independent_01.mp4", "FALL", "Valós Esés 1 (EikeSan benchmark)"),
    ("fall_independent_02.mp4", "FALL", "Valós Esés 2 (OpenVINO benchmark)"),
    ("adl_independent_01.mp4", "ADL", "Normál Mozgás (Intel IoT Séta benchmark)")
]

print("="*65)
print("  FÜGGETLEN BENCHMARK ADATHALMAZOK AUTOMATIKUS KIÉRTÉKELÉSE")
print("  (A modell tanításához NEM használt, külső valós videók)")
print("="*65)

for fname, gt, desc in videos:
    vpath = os.path.join(folder, fname)
    if not os.path.exists(vpath):
        print(f"[HIBA] Nem található: {fname}")
        continue
        
    cap = cv2.VideoCapture(vpath)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    detector = KinematicFallDetector()
    
    fall_detected = False
    fall_frame = None
    fall_time = 0.0
    fall_metrics = {}
    
    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        res = model(frame, verbose=False, conf=0.30)[0]
        if len(res.boxes) > 0 and res.keypoints is not None:
            bbox = res.boxes.xyxy[0].cpu().numpy()
            kpts = res.keypoints.data[0].cpu().numpy()
            state, info = detector.update(kpts, bbox)
            if state == "FALLEN" and not fall_detected:
                fall_detected = True
                fall_frame = idx
                fall_time = idx / fps
                fall_metrics = info
        idx += 1
        
    cap.release()
    
    # Kiértékelés
    if gt == "FALL":
        status = "✅ TRUE POSITIVE" if fall_detected else "❌ FALSE NEGATIVE"
    else:
        status = "✅ TRUE NEGATIVE" if not fall_detected else "⚠️ FALSE POSITIVE"
        
    print(f"\nVideó: {fname} ({desc})")
    print(f"  Hossz: {total_frames} képkocka ({total_frames/fps:.1f} mp, {fps:.1f} FPS)")
    print(f"  Elvárt állapot: {gt} | Detektálás: {'ESÉS DETEKTÁLVA' if fall_detected else 'NORMÁL MOZGÁS'}")
    print(f"  Eredmény: {status}")
    if fall_detected:
        print(f"  Riasztás pillanata: {fall_time:.2f} mp (képkocka: {fall_frame}/{total_frames})")
        print(f"  Telemetria riasztáskor: Törzsszög={fall_metrics.get('torso_angle', 0):.1f}°, W/H={fall_metrics.get('aspect_ratio', 0):.2f}, Zuhanási sebesség={fall_metrics.get('drop_velocity', 0):.2f}")

print("\n" + "="*65)
