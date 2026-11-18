# Hardveres Futási Teljesítménymérés és Profilozás Jegyzőkönyv
**Modell:** YOLOv8n-Pose (Nano - 3.2M)
**Környezet:** AMD64 Family 25 Model 80 Stepping 0, AuthenticAMD | 6 mag / 12 szál | Python 3.13.7 | PyTorch 2.14.1+cpu
**Mintaelemszám:** N = 1500 képkocka (50 warmup után)
**Nyers CSV napló:** `profiling_1500_frames_yolov8n_cpu.csv`

## 5.3. Táblázat: Empirikus Komponensszintű Profilozási Eredmények

| Feldolgozási fázis | Megvalósító modul | Átlagos idő (t̄) | Szórás (±σ) | Min. idő | Max. idő | p95 késleltetés |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Képkocka beolvasás** | `VideoSource (OpenCV, 640x480)` | 1.54 ms | ± 0.70 ms | 1.10 ms | 27.15 ms | 1.74 ms |
| **YOLOv8n-Pose (Nano - 3.2M) inferencia** | `Ultralytics (PyTorch CPU)` | 69.65 ms | ± 3.82 ms | 62.05 ms | 119.95 ms | 74.56 ms |
| **Kulcspont-kinyerés** | `KeypointExtractor` | 0.07 ms | ± 0.05 ms | 0.01 ms | 0.29 ms | 0.13 ms |
| **Kinematika és FSM** | `KinematicsEngine + FSM` | 0.05 ms | ± 0.03 ms | 0.00 ms | 0.16 ms | 0.08 ms |
| **GUI renderelés és overlay** | `GUIController (Tkinter / PIL)` | 2.29 ms | ± 0.44 ms | 1.33 ms | 4.35 ms | 2.90 ms |
| **Teljes ciklusidő (GUI-val)** | **Teljes pipeline (End-to-End)** | **73.61 ms** | **± 4.26 ms** | **65.55 ms** | **146.42 ms** | **78.68 ms** |
| **Képkockasebesség (FPS)** | **Mért átviteli sebesség** | **13.62 FPS** | **± 0.61 FPS** | **6.83 FPS** | **15.26 FPS** | **12.71 FPS** |
| **Headless pipeline (Éles IoT)** | **GUI nélküli háttérfolyamat** | **71.32 ms** | **± 4.14 ms** | **63.32 ms** | **144.04 ms** | **76.33 ms** |
| **Headless FPS** | **Éles átviteli sebesség** | **14.06 FPS** | **± 0.62 FPS** | **6.94 FPS** | **15.79 FPS** | **13.10 FPS** |

## Matematikai és Módszertani Észrevételek (Konzulensi audit igazolása)

- **Komponens-minimumok összege:** `64.50 ms` $\leftrightarrow$ **Ténylegesen MÉRT End-to-End minimum:** `65.55 ms`
- **Komponens-maximumok összege:** `151.90 ms` $\leftrightarrow$ **Ténylegesen MÉRT End-to-End maximum:** `146.42 ms`
- **Következtetés:** A mérés igazolja, hogy a komponensek nem ugyanazon a képkockán érik el a szélsőértékeket (a mért min nagyobb, mint a minimumok összege; a mért max pedig a valódi pipeline fluktuációt tükrözi).

## Tudományos és Kutatási Értékelés (H4 Hipotézis)

* A mérések tanúsága szerint a natív, optimalizálatlan PyTorch CPU futtatókörnyezetben az átlagos sebesség **13.62 FPS**.
* Ez a kutatási terv szempontjából kulcsfontosságú empirikus bizonyíték: alátámasztja, hogy a **Szakdolgozat 2-ben elengedhetetlen a 6.3. fejezetben megfogalmazott hardveres optimalizáció (ONNX Runtime, OpenVINO, INT8 PTQ kvantálás)**, mivel natív CPU-n a modell önmagában nem éri el a stabil 25,0 FPS valós idejű küszöböt.