# -*- coding: utf-8 -*-
"""
Webkamera Részletes Diagnosztika Windows alatt
Segít kideríteni, hogy miért nem látja az OpenCV a kamerát.
"""

import time
import cv2

print("=" * 60)
print("  WEBKAMERA HARDVERES ÉS SZOFTVERES DIAGNOSZTIKA")
print("=" * 60)

backends = [
    ("DirectShow (cv2.CAP_DSHOW)", cv2.CAP_DSHOW),
    ("Alapértelmezett (cv2.CAP_ANY)", cv2.CAP_ANY)
]

found = False

for b_name, b_code in backends:
    print(f"\n[+] Backend tesztelése: {b_name}")
    for idx in range(4):
        print(f"    -> Kamera index {idx} próbálkozás...", end="", flush=True)
        try:
            cap = cv2.VideoCapture(idx, b_code)
            if not cap.isOpened():
                print(" [NEM NYÍLT MEG]")
                continue
                
            print(" [MEGNYÍLT] -> Képkocka beolvasás (bemelegítés)...", end="", flush=True)
            # Sok laptop kamerának kell 200-400 ms bemelegedési idő!
            frame_ok = False
            for attempt in range(10):
                time.sleep(0.08)
                ret, frame = cap.read()
                if ret and frame is not None and frame.size > 0:
                    frame_ok = True
                    h, w, _ = frame.shape
                    print(f" [SIKERES! Felbontás: {w}x{h}]")
                    found = True
                    break
            
            if not frame_ok:
                print(" [IDŐTÚLLÉPÉS: nem adott képet]")
                
            cap.release()
        except Exception as e:
            print(f" [HIBA: {e}]")

print("\n" + "=" * 60)
if found:
    print("  EREDMÉNY: TALÁLTUNK MŰKÖDŐ WEBKAMERÁT!")
    print("  A webcam_test.py mostantól csatlakozni fog hozzá.")
else:
    print("  EREDMÉNY: EGYETLEN KAMERA INDEX SEM ADOTT KÉPET.")
    print("  Lehetséges okok Windows laptopokon:")
    print("  1. Windows Kamera Adatvédelem le van tiltva:")
    print("     -> Nyisd meg a Gépházat (Settings) -> Adatvédelem és biztonság -> Kamera.")
    print("     -> Kapcsold BE: 'Kamera elérése ezen az eszközön' és 'Asztali alkalmazások hozzáférése'.")
    print("  2. Fizikai retesz / takaróka a laptop tetején (Lenovo/HP/Asus ThinkShutter):")
    print("     -> Húzd el a lencse előtti kis műanyag csúszkát!")
    print("  3. Funkcióbillentyű (Fn gomb):")
    print("     -> Sok laptopon az Fn + F10 / Fn + F6 gomb fizikailag áramtalanítja a webkamerát.")
print("=" * 60)

input("\nNyomj Entert a bezáráshoz...")
