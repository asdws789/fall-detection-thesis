# Gráf alapú modellek detektálása vizuális információn, különös tekintettel a viselkedéselemzésre

**Szakdolgozat / Diplomamunka Projekt (BSc)**  
**Kutatási fókusz:** Valós idejű esésdetektálás és kritikus mozgáselemzés emberi pózbecsléssel és tér-időbeli gráfkonvolúciós hálózatokkal (YOLOv8-Pose, ST-GCN, PyTorch)  
**Célhardver:** AMD Ryzen 5 5500 CPU (6 mag / 12 szál), 16 GB RAM, CPU-alapú valós idejű ONNX Runtime inferencia

---

## 📁 Mappastruktúra

```
anti_thesis/
├── docs/                       # Kutatási tervek, specifikációk és beszámolók
│   ├── szakdolgozati_kutatasi_terv_esesdetektalas.md  # 20 oldalas beszámoló alapja
│   ├── fejezet_1_bevezetes_esesdetektalas.md          # Dolgozat 1. fejezete
│   └── README.md
├── src/                        # Forráskódok
│   ├── __init__.py
│   └── webcam_test.py          # Hello World webkamerás pózbecslő teszt
├── data/                       # Adathalmazok
│   ├── raw/                    # Letöltött nyers benchmark videók (URFD, Le2i)
│   ├── processed/              # Kinyert 17 kulcspontos normalizált gráfok (.npy)
│   └── README.md
├── notebooks/                  # Kísérletező és adatvizualizációs Jupyter füzetek
├── run_webcam_test.bat         # Dupla kattintással indítható webkamera teszt
├── requirements.txt            # Python függőségek listája
├── .gitignore                  # Git verziókezelési kizárások
└── README.md                   # Ez a dokumentum
```

---

## 🚀 Gyorsindítás (Quickstart)

### 1. Függőségek telepítése
Nyiss egy terminált (PowerShell) ebben a mappában, és futtasd:
```bash
pip install -r requirements.txt
```
*(Minimális csomagok az első webkamerás teszthez: `pip install ultralytics opencv-python`)*

### 2. Hello World Webkamera Teszt indítása
Kétféleképpen indíthatod el:
* **Opció A:** Kattints duplán a `run_webcam_test.bat` fájlra a Windows Fájlkezelőben.
* **Opció B:** Futtasd parancssorból:
  ```bash
  python src/webcam_test.py
  ```

A megjelenő ablakban élőben láthatod a webkamerádat a 17 kulcsponttal és az aktuális FPS értékkel. A kilépéshez nyomd meg a **'Q'** billentyűt.
