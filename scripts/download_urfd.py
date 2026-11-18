import os
import sys
import urllib.request
import zipfile

raw_dir = r"C:\uni_stuff\anti_thesis\data\raw\urfd"
os.makedirs(raw_dir, exist_ok=True)

items = [
    ("fall-02", "http://fenix.ur.edu.pl/~mkepski/ds/data/fall-02-cam0-rgb.zip"),
    ("adl-02", "http://fenix.ur.edu.pl/~mkepski/ds/data/adl-02-cam0-rgb.zip")
]

for name, url in items:
    zip_path = os.path.join(raw_dir, f"{name}.zip")
    ext_dir = os.path.join(raw_dir, name)
    
    if os.path.exists(ext_dir) and len(os.listdir(ext_dir)) > 0:
        print(f"[OK] {name} már létezik és ki van bontva.")
        continue
        
    print(f"Letöltés: {name} ({url})...")
    try:
        urllib.request.urlretrieve(url, zip_path)
        print(f"Kicsomagolás: {name} ide: {ext_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(ext_dir)
        print(f"[OK] {name} sikeresen letöltve és kibontva!")
    except Exception as e:
        print(f"[HIBA] Nem sikerült letölteni {name}: {e}")

print("Kész!")
