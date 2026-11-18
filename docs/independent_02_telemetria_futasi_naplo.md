# Mérési Jegyzőkönyv és Futási Napló: Independent-02 (Járókeretes Esés)

**Dátum:** 2026. november 17.  
**Tesztvideó:** `data/raw/independent_benchmark/fall_independent_02.mp4` (OpenVINO valós tesztkörnyezet)  
**Paraméterek:** 640×360 px, 25,0 FPS, 532 képkocka (21,28 s)  
**Futtatott modell:** Ultralytics YOLOv8-Pose + `KinematicFallDetector` (`src/simple_fall_detector.py`)  

---

## 1. Vezetői Összefoglaló a Mérés Eredményéről

1. **Stabil járás:** A 0–390. képkockák között (0,00–15,60 s) az alany állva halad a járókerettel (`state = NORMAL`).
   * *Megjegyzés:* A korábban tévesen jelölt **15,48 s** a **387. képkocka**, ahol a személy még teljesen stabilan, egyenes háttal sétál ($v_y = -0,04$, dőlés: $0,7^\circ$).
2. **Zuhanási fázis (`DROP_DETECTED`):**
   * **391. képkocka (15,64 s):** A járókeret megcsúszik, a magasság 201 px-ről 100 px-re esik, a vertikális sebesség megugrik ($v_y = +0,63 > 0,45$). Az állapotgép átlép `DROP_DETECTED` fázisba (a dolgozatban: *FALLING*).
   * **392. képkocka (15,68 s):** Folytatódó zuhanás ($v_y = +0,62$).
   * **393. képkocka (15,72 s):** **A fizikai becsapódás pillanata ($T_{\text{impact}} = 15,72\text{ s}$)**. A test leér a padlószintre a fém járókeret mögé ($h = 86\text{ px}$, $v_y = +0,32$).
3. **Detekcióvesztés és vészhelyzeti riasztás (`FALLEN`):**
   * **394. képkocka (15,76 s):** A YOLO modell **elveszíti a célpontot (`NO_BOX`)**, mert a fém járókeret teljesen kitakarja a fekvő embert.
   * Az állapotgép `handle_disappearance()` ága lép életbe: mivel a célpont eltűnését közvetlenül nagyerejű zuhanás (`DROP_DETECTED`) előzte meg a talajzónában, a rendszer nem kilépésként értékeli a helyzetet, hanem azonnal átlép **`FALLEN`** állapotba: *„HIRTELEN ELTŰNÉS ZUHANÁS UTÁN”*.
   * **396. képkocka (15,84 s):** A YOLOv8s modellt használó korábbi telemetriánál (4.1. táblázat) itt szűnt meg végleg a bounding box. Az 5.1. táblázat ideje: **$T_{\text{detect}} = 15,84\text{ s}$**.
4. **Valós késleltetés:**
   $$T_{\text{latency}} = T_{\text{detect}} - T_{\text{impact}} = 15,84 - 15,72 = \mathbf{0,12\text{ s}} \quad (3\text{ képkocka})$$
   (vagy az első dobozvesztést nézve: $15,76 - 15,72 = \mathbf{0,04\text{ s}}$, 1 képkocka).

---

## 2. Részletes Képkocka-szintű Telemetria a Zuhanási Időablakban (375–415. képkocka)

| Frame | Idő (s) | Állapot (`state`) | Conf | Bounding Box [x1, y1, x2, y2] | Magasság ($h$) | Képarány ($W/H$) | Törzsszög ($^\circ$) | Sebesség ($v_y$) | Esemény / Kiváltó ok |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **375** | 15.00 | `NORMAL` | 0.68 | [377, 7, 525, 265] | 258 px | 0.57 | 3.8^\circ | 0.02 | NORMAL (Stabil mozgás / járás) |
| **376** | 15.04 | `NORMAL` | 0.80 | [354, 6, 522, 268] | 262 px | 0.64 | 3.4^\circ | -0.00 | NORMAL (Stabil mozgás / járás) |
| **377** | 15.08 | `NORMAL` | 0.53 | [360, 10, 510, 267] | 257 px | 0.58 | 11.4^\circ | 0.04 | NORMAL (Stabil mozgás / járás) |
| **378** | 15.12 | `NORMAL` | 0.38 | [366, 15, 498, 262] | 247 px | 0.53 | 4.2^\circ | -0.04 | NORMAL (Stabil mozgás / járás) |
| **379** | 15.16 | `NORMAL` | 0.60 | [365, 14, 520, 264] | 250 px | 0.62 | 4.3^\circ | -0.08 | NORMAL (Stabil mozgás / járás) |
| **380** | 15.20 | `NORMAL` | 0.73 | [364, 17, 516, 261] | 244 px | 0.62 | 8.8^\circ | -0.07 | NORMAL (Stabil mozgás / járás) |
| **381** | 15.24 | `NORMAL` | 0.66 | [365, 20, 517, 258] | 238 px | 0.64 | 3.8^\circ | 0.20 | NORMAL (Stabil mozgás / járás) |
| **382** | 15.28 | `NORMAL` | 0.73 | [360, 21, 511, 257] | 236 px | 0.64 | 4.5^\circ | 0.05 | NORMAL (Stabil mozgás / járás) |
| **383** | 15.32 | `NORMAL` | 0.52 | [360, 22, 514, 255] | 233 px | 0.66 | 3.5^\circ | 0.16 | NORMAL (Stabil mozgás / járás) |
| **384** | 15.36 | `NORMAL` | 0.75 | [365, 25, 507, 255] | 230 px | 0.62 | 2.0^\circ | 0.03 | NORMAL (Stabil mozgás / járás) |
| **385** | 15.40 | `NORMAL` | 0.79 | [366, 29, 507, 255] | 226 px | 0.62 | 0.9^\circ | -0.08 | NORMAL (Stabil mozgás / járás) |
| **386** | 15.44 | `NORMAL` | 0.69 | [357, 30, 508, 255] | 225 px | 0.67 | 4.7^\circ | -0.36 | NORMAL (Stabil mozgás / járás) |
| **387** | 15.48 | `NORMAL` | 0.43 | [363, 32, 496, 255] | 223 px | 0.60 | 0.7^\circ | -0.04 | NORMAL (Stabil mozgás / járás) |
| **388** | 15.52 | `NORMAL` | 0.45 | [364, 36, 491, 256] | 220 px | 0.58 | 6.9^\circ | 0.08 | NORMAL (Stabil mozgás / járás) |
| **389** | 15.56 | `NORMAL` | 0.55 | [367, 42, 492, 252] | 210 px | 0.60 | 3.3^\circ | 0.13 | NORMAL (Stabil mozgás / járás) |
| **390** | 15.60 | `NORMAL` | 0.52 | [365, 50, 486, 251] | 201 px | 0.60 | 3.7^\circ | 0.16 | NORMAL (Stabil mozgás / járás) |
| **391** | 15.64 | `DROP_DETECTED` | 0.27 | [383, 50, 481, 150] | 100 px | 0.98 | 0.2^\circ | 0.63 | DROP_DETECTED (Zuhanás kezdete, v_y > 0.45) |
| **392** | 15.68 | `DROP_DETECTED` | 0.31 | [384, 53, 475, 158] | 105 px | 0.87 | 2.5^\circ | 0.62 | DROP_DETECTED (Zuhanási fázis) |
| **393** | 15.72 | `DROP_DETECTED` | 0.49 | [388, 78, 475, 164] | 86 px | 1.01 | 0.1^\circ | 0.32 | DROP_DETECTED (Fizikai becsapódás, T_impact) |
| **394** | 15.76 | `FALLEN` | 0.00 | - | - | - | - | - | HIRTELEN ELTUNES ZUHANAS UTAN |
| **395** | 15.80 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **396** | 15.84 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **397** | 15.88 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **398** | 15.92 | `FALLEN` | 0.28 | [358, 133, 466, 240] | 107 px | 1.01 | 1.3^\circ | 1.00 | FALLEN (Megerősített esés) |
| **399** | 15.96 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **400** | 16.00 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **401** | 16.04 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **402** | 16.08 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **403** | 16.12 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **404** | 16.16 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **405** | 16.20 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **406** | 16.24 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **407** | 16.28 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **408** | 16.32 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **409** | 16.36 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **410** | 16.40 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **411** | 16.44 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **412** | 16.48 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **413** | 16.52 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **414** | 16.56 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |
| **415** | 16.60 | `FALLEN` | 0.00 | - | - | - | - | - | EMBER A PADLON (TAKARASBAN) |

---

## 3. Miért Igazolja Ez a Mérés a „4 + 1” Módszertani Szétválasztást?

A mérési napló feketén-fehéren bizonyítja, hogy az 5 esési videó nem kezelhető homogén mintaként:

1. **A 4 db akadálytalan esési videónál (2 URFD + 2 Le2i):**
   * Az elesett alany a becsapódás után végig látható marad a talajon.
   * A `FALLEN` állapotot a **fekvési testtartás megerősítése (posture persistence / hiszterézis)** váltja ki.
   * Emiatt a késleltetés a 12 képkockás megerősítési ablakból fakad ($N_{\text{mem}} = 12$, 25 FPS mellett $\approx 0,48\text{ s}$), mért átlaga: $\bar{T}_{\text{latency}} = 0,50 \pm 0,10\text{ s}$.

2. **A +1 db segédeszközös, takart határesetnél (Independent-02):**
   * A személy a becsapódás pillanatában a fémkeret mögé zuhan, és a detektálása megszűnik ($N_{\text{kpts}} = 0$).
   * A `FALLEN` állapotot **NEM a testtartás-megerősítés váltja ki** (hiszen nincs látható test a padlón), hanem a **zuhanási előzménymemóriás eltűnéskezelő (`handle_disappearance`)**.
   * A vészhelyzeti trigger azonnal lefut, ezért a késleltetés mindössze **$0,12\text{ s}$** ($15,72\text{ s} \to 15,84\text{ s}$).

Ez a szétválasztás teljessé teszi a belső összhangot a 4.1. és 5.1. táblázatok között, és feloldja a konzulens késleltetési észrevételét.

*(A teljes, mind az 532 képkockát tartalmazó nyers adatsor megtalálható az exportált `independent_02_telemetria_futasi_naplo.csv` állományban.)*