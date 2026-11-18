# Hardveres Futási Teljesítménymérés és Profilozás Jegyzőkönyv
**Modell:** YOLOv8s-Pose (Small - 11.6M)
**Környezet:** AMD64 Family 25 Model 80 Stepping 0, AuthenticAMD | 6 mag / 12 szál | Python 3.13.7 | PyTorch 2.14.1+cpu
**Mintaelemszám:** N = 1500 képkocka (50 warmup után)
**Nyers CSV napló:** `profiling_1500_frames_yolov8s_cpu.csv`

## 5.3. Táblázat: Empirikus Komponensszintű Profilozási Eredmények

| Feldolgozási fázis | Megvalósító modul | Átlagos idő (t̄) | Szórás (±σ) | Min. idő | Max. idő | p95 késleltetés |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Képkocka beolvasás** | `VideoSource (OpenCV, 640x480)` | 1.55 ms | ± 0.31 ms | 1.00 ms | 10.21 ms | 1.78 ms |
| **YOLOv8s-Pose (Small - 11.6M) inferencia** | `Ultralytics (PyTorch CPU)` | 160.23 ms | ± 13.22 ms | 134.55 ms | 332.70 ms | 172.52 ms |
| **Kulcspont-kinyerés** | `KeypointExtractor` | 0.06 ms | ± 0.11 ms | 0.01 ms | 3.84 ms | 0.13 ms |
| **Kinematika és FSM** | `KinematicsEngine + FSM` | 0.05 ms | ± 0.03 ms | 0.01 ms | 0.32 ms | 0.09 ms |
| **GUI renderelés és overlay** | `GUIController (Tkinter / PIL)` | 2.24 ms | ± 0.47 ms | 1.30 ms | 9.99 ms | 2.92 ms |
| **Teljes ciklusidő (GUI-val)** | **Teljes pipeline (End-to-End)** | **164.14 ms** | **± 13.29 ms** | **138.26 ms** | **335.87 ms** | **176.73 ms** |
| **Képkockasebesség (FPS)** | **Mért átviteli sebesség** | **6.12 FPS** | **± 0.34 FPS** | **2.98 FPS** | **7.23 FPS** | **5.66 FPS** |
| **Headless pipeline (Éles IoT)** | **GUI nélküli háttérfolyamat** | **161.89 ms** | **± 13.25 ms** | **136.06 ms** | **333.90 ms** | **174.26 ms** |
| **Headless FPS** | **Éles átviteli sebesség** | **6.20 FPS** | **± 0.35 FPS** | **2.99 FPS** | **7.35 FPS** | **5.74 FPS** |

## Matematikai és Módszertani Észrevételek (Konzulensi audit igazolása)

- **Komponens-minimumok összege:** `136.87 ms` $\leftrightarrow$ **Ténylegesen MÉRT End-to-End minimum:** `138.26 ms`
- **Komponens-maximumok összege:** `357.07 ms` $\leftrightarrow$ **Ténylegesen MÉRT End-to-End maximum:** `335.87 ms`
- **Következtetés:** A mérés igazolja, hogy a komponensek nem ugyanazon a képkockán érik el a szélsőértékeket (a mért min nagyobb, mint a minimumok összege; a mért max pedig a valódi pipeline fluktuációt tükrözi).

## Tudományos és Kutatási Értékelés (H4 Hipotézis)

* A mérések tanúsága szerint a natív, optimalizálatlan PyTorch CPU futtatókörnyezetben az átlagos sebesség **6.12 FPS**.
* Ez a kutatási terv szempontjából kulcsfontosságú empirikus bizonyíték: alátámasztja, hogy a **Szakdolgozat 2-ben elengedhetetlen a 6.3. fejezetben megfogalmazott hardveres optimalizáció (ONNX Runtime, OpenVINO, INT8 PTQ kvantálás)**, mivel natív CPU-n a modell önmagában nem éri el a stabil 25,0 FPS valós idejű küszöböt.