# Kötegelt Esésdetektálási Telemetriai és Kiértékelési Jegyzőkönyv
**Dátum:** 2026-11-17 14:54:04
**Modell:** YOLOv8s-Pose (Small - 11.6M paraméter) | PyTorch CPU backend
**Küszöbértékek:**
- Egyszerű AR: $AR > 1{,}0$
- Naív kinematika: $\theta > 45^\circ$ ÉS $v_y > 0{,}35$, vagy $AR > 1{,}15$ ÉS $\theta > 60^\circ$ (peremszűrők nélkül)
- Javított FSM: `KinematicFallDetector` állapotgép (ajtószélszűrő, konyhapult-védelem, kanapészint-modell, zuhanási memóriás `handle_disappearance`)
- Képkockasebességek: URFD: 30 FPS; Le2i: 25 FPS; Independent-02: 25 FPS

## 5.1. Táblázat: A 10 Benchmark Videó Programozott Kiértékelése

| Sorszám és videó | Típus | FPS | Valós tény (GT) | Annotált becsapódás (T_impact) | 1. Egyszerű AR (AR > 1.0) | 2. Naív kinematika | 3. Javított FSM (Jelen prototípus) | Észlelési késleltetés (T_latency) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **URFD Fall-01 (Előreesés)** | FALL | 30.0 | FALL | 3.17 s (Frame 95) | FALL (3.57s) [TP] | FALL (3.40s) [TP] | **FALL (3.57s) [TP]** | +0.40 s |
| **URFD Fall-02 (Hátraesés)** | FALL | 30.0 | FALL | 1.53 s (Frame 46) | FALL (1.80s) [TP] | FALL (2.03s) [TP] | **FALL (2.07s) [TP]** | +0.53 s |
| **URFD ADL-01 (Leülés székre)** | ADL | 30.0 | ADL | – | NORMAL [TN] | NORMAL [TN] | **NORMAL [TN]** | – |
| **URFD ADL-02 (Lehajolás)** | ADL | 30.0 | ADL | – | NORMAL [TN] | NORMAL [TN] | **NORMAL [TN]** | – |
| **Le2i Coffee-01 v1 (Szédülés, esés)** | FALL | 25.0 | FALL | 2.40 s (Frame 60) | FALL (2.16s) [TP] | FALL (2.24s) [TP] | **FALL (2.28s) [TP]** | -0.12 s |
| **Le2i Home-01 v2 (Pult melletti esés)** | FALL | 25.0 | FALL | 5.08 s (Frame 127) | FALL (1.72s) [TP] | FALL (2.16s) [TP] | **FALL (5.12s) [TP]** | +0.04 s |
| **Le2i Home-02 v41 (Ajtón belépés)** | ADL | 25.0 | ADL | – | 🚨 FALL (0.00s) (Hiba!) [FP] | 🚨 FALL (1.76s) (Hiba!) [FP] | **NORMAL [TN]** | – |
| **Le2i Home-02 v51 (Kanapéra ülés)** | ADL | 25.0 | ADL | – | 🚨 FALL (1.44s) (Hiba!) [FP] | 🚨 FALL (7.84s) (Hiba!) [FP] | **NORMAL [TN]** | – |
| **Le2i Home-02 v53 (Kanapén fekvés)** | ADL | 25.0 | ADL | – | 🚨 FALL (5.60s) (Hiba!) [FP] | NORMAL [TN] | **NORMAL [TN]** | – |
| **Independent-02 (Járókeretes esés)** | FALL | 25.0 | FALL | 15.72 s (Frame 393) | FALL (15.72s) [TP] | NORMAL (Hiba!) [FN] | **FALL (15.80s) [TP]** | +0.08 s |

## 5.2. Táblázat: Összehasonlító Metrikák és Konfúziós Mátrix

| Metrika | 1. Egyszerű AR küszöb | 2. Naív kinematika | 3. Javított FSM (Jelen prototípus) |
| :--- | :---: | :---: | :---: |
| **Valós TP (TP)** | 5 | 4 | **5** |
| **Valós FP (FP)** | 3 | 2 | **0** |
| **Valós TN (TN)** | 2 | 3 | **5** |
| **Valós FN (FN)** | 0 | 1 | **0** |
| **Pontosság (Accuracy)** | 70.0% | 70.0% | **100.0%** |
| **Érzékenység (Recall / TPR)** | 100.0% | 80.0% | **100.0%** |
| **Precízió (Precision)** | 62.5% | 66.7% | **100.0%** |
| **F1-score** | 0.769 | 0.727 | **1.000** |
| **Téves Pozitív Ráta (FPR)** | 60.0% | 40.0% | **0.0%** |

## Észlelési Késleltetések (Javított FSM)

- **URFD Fall-01 (Előreesés):** $T_{\text{impact}} = 3.17\text{ s} \to T_{\text{detect}} = 3.57\text{ s} \implies T_{\text{latency}} = +0.40\text{ s}$
- **URFD Fall-02 (Hátraesés):** $T_{\text{impact}} = 1.53\text{ s} \to T_{\text{detect}} = 2.07\text{ s} \implies T_{\text{latency}} = +0.53\text{ s}$
- **Le2i Coffee-01 v1 (Szédülés, esés):** $T_{\text{impact}} = 2.40\text{ s} \to T_{\text{detect}} = 2.28\text{ s} \implies T_{\text{latency}} = -0.12\text{ s}$
- **Le2i Home-01 v2 (Pult melletti esés):** $T_{\text{impact}} = 5.08\text{ s} \to T_{\text{detect}} = 5.12\text{ s} \implies T_{\text{latency}} = +0.04\text{ s}$
- **Independent-02 (Járókeretes esés):** $T_{\text{impact}} = 15.72\text{ s} \to T_{\text{detect}} = 15.80\text{ s} \implies T_{\text{latency}} = +0.08\text{ s}$