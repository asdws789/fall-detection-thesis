import os
import urllib.request

dest_dir = r"C:\uni_stuff\anti_thesis\data\raw\independent_test"
os.makedirs(dest_dir, exist_ok=True)

# URL-ek a független tesztkészlethez
base_url = "https://raw.githubusercontent.com/AwaisShah75/Real-Time-Person-Elderly-Fall-Detection-System/main/sample_videos/"
videos = [
    ("standing_fall_1.mp4", base_url + "standing_fall_1.mp4"),
    ("standing_fall_2.mp4", base_url + "standing_fall_2.mp4"),
    ("sitting_to_fall.mp4", base_url + "sitting_to_fall.mp4"),
    ("bed_rollout_fall.mp4", base_url + "bed_rollout_fall.mp4"),
    ("normal_activity_no_fall.mp4", base_url + "normal_activity_no_fall.mp4"),
]

for fname, url in videos:
    target_path = os.path.join(dest_dir, fname)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 10000:
        print(f"[OK] {fname} már létezik ({os.path.getsize(target_path)} bájt).")
        continue
    print(f"Letöltés: {fname}...")
    try:
        urllib.request.urlretrieve(url, target_path)
        sz = os.path.getsize(target_path)
        print(f"[OK] {fname} sikeresen letöltve ({sz / (1024*1024):.2f} MB)")
    except Exception as e:
        print(f"[HIBA] Nem sikerült letölteni {fname}: {e}")

print("Letöltések kész!")
