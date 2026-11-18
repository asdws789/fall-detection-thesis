# -*- coding: utf-8 -*-
"""
Szakdolgozati Beszámoló és Részletes Kutatási Terv (Esésdetektálás + Raspberry Pi Edge AI)
4. RÉSZ (Átdolgozott, 7 javítás beépítve):
- 6. Fejezet (Adathalmazok, Baseline modellek, ÚJ 6.4 Statisztikai Módszertan & Ablációs terv)
- 7. Fejezet (Metrikák és ÚJ 7.2 Tervezett Teljesítmény-Célértékek Táblázat magyarázattal)
- 8. Fejezet (Kockázatelemzés és mitigáció)
- 9. Fejezet (ÚJ Kétféléves Ütemterv: Szakdolgozat 1 lezárás vs. Szakdolgozat 2 tavaszi 14 hét)
- 10. Fejezet (Adatvédelem és GDPR)
- 11. Fejezet (Végleges dolgozat 65-75 oldalas vázlata)
- 12. Fejezet (Bővített 22 tételes tudományos irodalomjegyzék)
"""

PART4_MD = r"""## 6. Adathalmazok, baseline modellek és statisztikai módszertan

### 6.1 Nyilvános referencia-adathalmazok
A kísérleti validációhoz a szakirodalomban legszélesebb körben hivatkozott benchmark adatbázisokat használjuk:

| Adathalmaz | Videók száma | Kamera szögek | Cselekvési osztályok | Szerepe a szakdolgozatban |
| :--- | :---: | :---: | :--- | :--- |
| **UR Fall Detection (URFD)** [3] | 70 videó (30 esés, 40 ADL) | 2 kamera (Frontális és mennyezeti) | Esés, séta, ülés, tárgy felvétele, fekvés | **Fő tanító és validációs készlet.** Szinkronizált, tiszta laboratóriumi felvételek. |
| **Le2i Fall Detection** [4] | 191 videó | Változó lakásbelső (nappali, konyha, háló) | Esések és nehéz mindennapi mozgások | **Robusztussági és takarási teszt** (bútorok általi takarások, árnyékok, változó fényviszonyok). |

*(Megjegyzés: Az UP-Fall adathalmazt [13] a feladat fókuszának megőrzése és a túlbonyolítás elkerülése érdekében másodlagos tartalékként kezeljük; a fő kísérletek az URFD és Le2i adatokra épülnek.)*

### 6.2 Saját kontrollált szobai tesztkészlet
A rendszer általánosító képességének és a valós idejű webkamerás működésének igazolására egy 30 saját videóból álló kontrollált tesztkészletet rögzítünk a Szakdolgozat 2 félévben:
* 10 valósághű esés (matracra/szőnyegre esés: előre, hátra, oldalra, székből kicsúszás).
* 10 gyors leülés székre, kanapéra és fotelbe (Hard Negatives).
* 10 mindennapi hajolás, cipőkötés, kulcscsomó felvétele a földről.

### 6.3 Összehasonlító modellek (Fókuszált Baseline Architektúrák)
A túlméretezés elkerülésére a szakdolgozatban két letisztult, jól definiált összehasonlító modellt állítunk szembe a javasolt ST-GCN hálózattal:
1. **Baseline 1 (Refaktorált Kinematikai Heurisztika):** A kézzel tervezett, szabályalapú állapotgép a javított, skálainvariáns $\max(W, H)$ normával és előjelhelyes irányvektorral (az 5. fejezetben részletezett Baseline V2 modell).
2. **Baseline 2 (Szekvenciális Mély Modell – Bi-LSTM):** Kétrétegű kétirányú LSTM hálózat (128 rejtett egységgel), amely a normalizált ízületi koordinátákat lapos időbeli vektorként ($T \times 51$) dolgozza fel anélkül, hogy a test anatómiai csontkapcsolatait expliciten figyelembe venné.
3. **Javasolt Modell (ST-GCN INT8):** A 9 blokkból álló tér-időbeli gráfkonvolúciós hálózat a COCO-17 anatómiai topológián, poszt-tanítási INT8 kvantálással az ONNX Runtime motorban.

---

### 6.4 Statisztikai módszertan és ablációs kísérletterv (Szakdolgozat 2)

A hipotézisek tudományosan megalapozott ellenőrzésére a Szakdolgozat 2 félév kísérleti szakaszában az alábbi statisztikai protokollt alkalmazzuk:

#### 1. Keresztvalidáció (Stratified 5-Fold Cross-Validation)
Mivel az URFD (70 videó) és Le2i (191 videó) adathalmazok esetszáma viszonylag korlátozott, a véletlenszerű egyszeri tanító/teszt felosztás (train/test split) könnyen torzításhoz (split bias) vagy szerencsés véletlenhez vezethet. Ennek kizárására **5-szörös rétegzett keresztvalidációt (Stratified 5-Fold CV)** hajtunk végre:
* Az adathalmazt 5 egyenlő részre osztjuk úgy, hogy az esések és az ADL mozgások aránya minden foldban azonos maradjon.
* A modellt 5 különálló menetben tanítjuk be 4 részleten, és a kimaradó 1 részleten teszteljük.
* Minden metrikát (Recall, Precision, F1) az 5 menet átlagaként és szórásaként ($\mu \pm \sigma$) számolunk ki.

#### 2. Statisztikai Hipotézisvizsgálat
* **McNemar-teszt:** Az ST-GCN és a Bi-LSTM, illetve a Kinematikai Baseline páronkénti diszkriminációs képességének vizsgálatára McNemar-tesztet futtatunk a tévesztési mátrixokon. A különbséget akkor tekintjük statisztikailag szignifikánsnak, ha a p-érték szigorúan kisebb, mint $\alpha = 0.05$ ($p < 0.05$).
* **95%-os Konfidencia-Intervallumok (CI):** A végső Recall és F1 értékekhez nem-paraméteres **Bootstrap újramintavételezéssel** ($B = 1000$ iteráció) 95%-os megbízhatósági intervallumokat generálunk ($[\text{CI}_{lower}, \text{CI}_{upper}]$).

#### 3. Rendszerszintű Ablációs Kísérletek (Ablation Studies)
A dolgozat tudományos értékének biztosítására három dedikált ablációs vizsgálatot végzünk:
* **Ablation 1 (A térbeli gráfkonvolúció izolált hatása):**  
  *Kísérlet:* Az ST-GCN térbeli konvolúciós rétegeinek kikapcsolása (csak az időbeli TCN rétegek megtartása) vs. a teljes ST-GCN hálózat.  
  *Kérdés:* Hány százalékpontos F1-növekedést hoz a csontok anatómiai topológiájának explicit modellezése a tiszta időbeli dinamikához képest?
* **Ablation 2 (Időablak méretének optimalizálása):**  
  *Kísérlet:* A csúszóablak hosszának szisztematikus variálása: $T \in \{16, 32, 48\}$ képkocka (~0.5 s, ~1.0 s, ~1.5 s).  
  *Kérdés:* Hol található a késleltetés (latency) és az esésfelismerési megbízhatóság közötti optimális kompromisszum?
* **Ablation 3 (Kvantálási degradáció mérése):**  
  *Kísérlet:* Az eredeti lebegőpontos (FP32) modell és az INT8 poszt-tanítási kvantált változat pontosságának és memóriaterhelésének közvetlen összevetése azonos tesztkészleten.  
  *Kérdés:* Mekkora pontosságvesztéssel jár a 75%-os méretcsökkenés?

---

## 7. Kiértékelési metrikák és futási profilozási terv

### 7.1 Osztályozási és diagnosztikai metrikák
Az esésdetektálás életvédelmi alkalmazás, ahol az orvosi aranyszabály: **egyetlen valódi esés sem maradhat észrevétlenül** (a tévesen negatívnak ítélt esés, $FN$ közvetlen életveszélyt jelent).

* **Szenzitivitás / Érzékenység (Sensitivity / Recall):**
  $$Recall = \frac{TP}{TP + FN} \quad (\text{Célérték:} \ge 96.0\%)$$
* **Specificitás (Specificity):**
  $$Specificity = \frac{TN}{TN + FP} \quad (\text{Célérték:} \ge 94.0\%)$$
* **Precízió (Precision) és F1-Score:**
  $$Precision = \frac{TP}{TP + FP}, \quad F_1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall} \quad (\text{Célérték:} \ge 95.0\%)$$
* **Konfúziós Mátrix és ROC-AUC görbe.**

### 7.2 Hardveres teljesítmény-profilozás: Tervezett célértékek (Edge Benchmark)

> [!NOTE]
> **Módszertani megjegyzés a bíráló bizottság számára:**  
> A 7.2. táblázatban rögzített értékek nem lezárt mérési eredmények, hanem a Szakdolgozat 2 félév kísérleti megvalósítására kitűzött **tervezési célértékek és specifikációk**. Az értékek a szakirodalomban publikált ARM Cortex-A76 ONNX Runtime benchmarkok [10, 11] és a YOLOv8n-pose lebegőpontos műveletigénye (GFLOPs) alapján kalkulált szakmai becslések. Ezen célértékek laboratóriumi mérésekkel történő egzakt validálása a Szakdolgozat 2 félév feladata.

#### 7.2. Táblázat: Tervezett és elvárt teljesítmény-célértékek a Szakdolgozat 2 implementációs fázisára

| Hardver Platform | Modell Formátum | Tervezett Inferencia (ms) | Cél FPS | Becsült CPU (%) | Becsült RAM (MB) | Tipikus Teljesítmény (W) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **AMD Ryzen 5 5500 (Host PC)** | FP32 (Native PyTorch) | ~18 ms | 45+ FPS | ~18% (12 szál) | ~650 MB | ~65 W |
| **AMD Ryzen 5 5500 (Host PC)** | INT8 (ONNX CPU) | ~11 ms | 60+ FPS | ~12% (12 szál) | ~320 MB | ~55 W |
| **Raspberry Pi 4B (Cortex-A72)** | FP32 (Native) | ~110 ms | ~9 FPS | ~95% (4 mag) | ~720 MB | ~7.5 W |
| **Raspberry Pi 4B (Cortex-A72)** | INT8 (ONNX NEON) | ~58 ms | ~17 FPS | ~78% (4 mag) | ~290 MB | ~6.8 W |
| **Raspberry Pi 5 (Cortex-A76)** | FP32 (Native) | ~46 ms | ~21 FPS | ~82% (4 mag) | ~680 MB | ~9.2 W |
| **Raspberry Pi 5 (Cortex-A76)** | **INT8 (ONNX NEON)** | **~28 ms** | **~32 FPS** | **~65% (4 mag)** | **~260 MB** | **~7.8 W** |

*Célkitűzés:* Az INT8 kvantálásnak köszönhetően a Raspberry Pi 5 eszközön a cél a 25 FPS feletti stabil valós idejű sebesség elérése úgy, hogy az eszköz teljesítményfelvétele ne haladja meg a 8 Wattot.

---

## 8. Kockázatelemzés és mitigációs stratégia

| Kockázat | Valószínűség | Hatás | Megelőzési és Elhárítási Terv (Mitigáció) |
| :--- | :---: | :---: | :--- |
| **K1: Raspberry Pi túlmelegedés és thermal throttling** | Közepes | Magas | Hivatalos aktív hűtőborda és PWM vezérelt ventilátor (Active Cooler) alkalmazása; a CPU hőmérsékletének 65°C alatt tartása szoftveres telemetriával. |
| **K2: Korlátozott képkockasebesség gyengébb hardveren (Pi 4)** | Közepes | Közepes | Bemeneti felbontás adaptív csökkentése ($320 \times 320$-ra), valamint képkocka-átugrás (Frame Skipping: minden 2. frame feldolgozása, ami 15 FPS-t ad – az emberi esés 1 másodperces lefutásához ez elegendő). |
| **K3: Gyors leülés és ágyba fekvés miatti téves riasztás** | Közepes | Magas | Háromfázisú hiszterézis bevezetése: a zuhanási fázist követően minimálisan $0.6$ másodperces horizontális inaktivitás megkövetelése. |
| **K4: Bútorok miatti takarás (kieső láb-ízületek)** | Magas | Közepes | Felsőtest-hangsúlyos gráfpartíció: ha az alsó végtagok láthatósága ($conf$) alacsony, a hálózat a fej, váll és csípő vertikális trajektóriájából dönt. |
| **K5: Éjszakai sötétség a hálószobában** | Közepes | Magas | Infravörös (NoIR) kameraszenzor és kiegészítő 850 nm-es láthatatlan IR LED megvilágítás használata a Raspberry Pi-hez. |

---

## 9. Munka- és ütemterv (Kétféléves strukturált mérföldkő-terv)

A szakdolgozati projekt két egymásra épülő egyetemi félévben valósul meg:

### I. Félév: Szakdolgozat 1 (Őszi Félév – Tervezés és Előkísérlet / Teljesítve)

| Hét / Fázis | Fókuszterület | Elvégzett Tevékenységek és Eredmények | Státusz |
| :---: | :--- | :--- | :---: |
| **1–4. hét** | **Kutatási Téma Körülhatárolása** | * Szakirodalom feldolgozása (YOLOv8-Pose, ST-GCN, ARM INT8 kvantálás).<br>* A kutatási célok, formális hipotézisek (H1–H4) és kutatási kérdések megfogalmazása. | **KÉSZ** |
| **5–8. hét** | **Rendszertervezés és UML Specifikáció** | * Végponttól-végpontig tartó adatfolyam megtervezése.<br>* UML Komponens-, Szekvencia- és Állapotgép-diagramok elkészítése.<br>* Hardverspecifikáció rögzítése (Cloud GPU tanítás + Raspberry Pi 5 végpont). | **KÉSZ** |
| **9–11. hét** | **Előkísérlet és Proof-of-Concept** | * A kezdeti kinematikai baseline implementálása webkamerán.<br>* **A „törpe-osztó” (dwarf-denominator) hiba felfedezése, matematikai levezetése és sikeres refaktorálása (Baseline V2).** | **KÉSZ** |
| **12–14. hét** | **Beszámoló és Terv Véglegesítése** | * Adathalmazok kiválasztása (URFD, Le2i), statisztikai módszertan kidolgozása.<br>* A részletes, ~20 oldalas tanszéki kutatási terv dokumentálása és leadása. | **KÉSZ** |

---

### II. Félév: Szakdolgozat 2 (Tavaszi Félév – Tervezett 14 Hetes Megvalósítás)

| Hét | Sprint Fókusz | Tevékenységek és Feladatok | Eredmény és Mérföldkő |
| :---: | :--- | :--- | :--- |
| **1–2. hét** | **Adatelőkészítés és Baseline-ok** | * URFD és Le2i adathalmazok letöltése, kulcspontok kinyerése `.npy` tenzorokba.<br>* Két baseline modell felállítása (Kinematikai V2 szabályrendszer és Bi-LSTM hálózat). | Strukturált váz-adathalmaz, baseline pontossági értékek. |
| **3–5. hét** | **ST-GCN Adaptáció és Tanítás** | * ST-GCN hálózat adaptálása COCO-17 topológiára.<br>* Modell tanítása **Google Colab / Kaggle Cloud GPU-n (Nvidia T4)** Focal Loss-szal.<br>* 5-fold rétegzett keresztvalidáció futtatása, súlyfájlok mentése. | Betanított modell (`best_stgcn.pth`), validációs F1 riport. |
| **6–7. hét** | **Kvantálás és ONNX Export** | * ST-GCN és YOLOv8n-pose exportálása ONNX formátumba.<br>* INT8 poszt-tanítási kvantálás (PTQ) kalibrációs vázadatokkal az ONNX Runtime-ban. | Kvantált modellek (`.onnx` INT8), ablációs kvantálási teszt. |
| **8–9. hét** | **Raspberry Pi 5 Integráció** | * Raspberry Pi OS ARM64 környezet felállítása, Camera Module 3 beállítása.<br>* Valós idejű videós csővezeték tesztelése, memóriaterhelés mérése. | Működő beágyazott észlelő prototípus. |
| **10. hét** | **Döntési Logika és IoT Riasztás** | * Háromfázisú hiszterézis és földön töltött idő számláló integrálása.<br>* MQTT eseményküldő és Telegram Bot riasztási modul aktiválása. | Teljes végponti működés (Zero Pixel Leakage). |
| **11. hét** | **Empirikus Mérések és Profiling** | * Laboratóriumi sebességmérések (késleltetés, FPS, CPU %, hőmérséklet PC vs. Pi).<br>* Saját szobai tesztvideók kiértékelése, McNemar-tesztek futtatása. | Végleges mérési adatok és diagramok. |
| **12–13. hét** | **Szakdolgozat Szövegezése** | * A 65–75 oldalas végleges szakdolgozat megírása a tanszéki sablon szerint.<br>* Részletes fejezetek (Bevezetés, Elmélet, Tervezés, Mérések, Konklúzió). | Teljes dolgozatpiszkozat (Draft v1.0). |
| **14. hét** | **Lektorálás és Védési Demó** | * Konzulensi javítások beépítése, formai finomítások, plágiumellenőrzés.<br>* Élő bemutató és védési prezentáció előkészítése. | Végleges, beadott szakdolgozat. |

---

## 10. Adatvédelmi, jogi és etikai megfontolások (Privacy-by-Design)

Az esésdetektáló rendszerek célterülete az ember legintimebb élettere (otthon, hálószoba, fürdőszoba). A rendszer tervezése szigorúan követi a GDPR előírásait:
1. **Anonimitás a forrásnál (Edge Ephemerality):** Az RGB képi adatok a pózbecslés után azonnal megsemmisülnek a RAM-ból. Merevlemezre vagy hálózatra képi információ soha nem kerül kiírásra.
2. **Nem biometrikus azonosító:** A 17 darab lebegőpontos koordináta nem tartalmaz arcvonásokat, íriszmintát vagy bőrszínt; matematikai módszerekkel lehetetlen belőle a személyazonosságot visszafejteni [9].
3. **Emberi autonómia és téves riasztás kezelése:** A rendszer helyi hangjelzéssel lehetőséget ad a felállt személynek a riasztás visszavonására, minimalizálva a hozzátartozók felesleges zaklatását.

---

## 11. A végleges szakdolgozat tervezett fejezeti felépítése (~65–75 oldal)

1. **Bevezetés és Problémafelvetés** (~6-8 oldal)
2. **Szakirodalmi Áttekintés és Elméleti Háttér** (~16-18 oldal)
   * 2.1 Esésdetektálási módszerek áttekintése (Hordható vs. Környezeti vs. Látórendszerek)
   * 2.2 YOLOv8-Pose és az OKS veszteségfüggvény
   * 2.3 Gráf neurális hálózatok és az ST-GCN elmélete
   * 2.4 Beágyazott gépi tanulás és az INT8 kvantálás matematikája
3. **Rendszertervezés és Szoftverarchitektúra (UML)** (~14-16 oldal)
   * 3.1 Végponttól-végpontig tartó adatfolyam és csúszóablak képzés
   * 3.2 Térbeli normalizálás és hiszterézis döntési állapotgép
   * 3.3 Raspberry Pi 4 / 5 hardver- és hűtési specifikáció
   * 3.4 IoT és vészjelzési alrendszer (MQTT, Webhook, Buzzer)
4. **Empirikus Esettanulmány: A Naiv Kinematika és a Törpe-Osztó Anomália** (~6-8 oldal)
5. **Kísérleti Eredmények és Kiértékelés** (~16-18 oldal)
   * 5.1 Adathalmazok (UR Fall, Le2i, saját adatok)
   * 5.2 Baseline modellek vs. ST-GCN összehasonlító mérései (5-fold CV, McNemar)
   * 5.3 Rendszerszintű ablációs vizsgálatok (topológia, ablakméret, kvantálás)
   * 5.4 Edge Profilozás: PC (Ryzen 5) vs. Raspberry Pi 4 és 5 összehasonlítása
6. **Prototípus Implementáció és Demonstráció** (~8-10 oldal)
7. **Adatvédelmi, Jogi és Etikai Megfontolások** (~4-5 oldal)
8. **Összegzés és Továbbfejlesztési Lehetőségek** (~4-5 oldal)
* **Irodalomjegyzék és Függelékek** (~5 oldal)

---

## 12. Tudományos hivatkozásjegyzék (Kiemelt források)

1. **Yan, S., Xiong, Y., & Lin, D. (2018).** Spatial temporal graph convolutional networks for skeleton-based action recognition. *AAAI Conference on Artificial Intelligence*, 32(1), 7444–7452.
2. **Jocher, G., Chaurasia, A., & Qiu, J. (2023).** Ultralytics YOLOv8. *https://github.com/ultralytics/ultralytics*
3. **Kwolek, B., & Kepski, M. (2014).** Human fall detection on embedded platform using depth maps and wireless accelerometer. *Computer Methods and Programs in Biomedicine*, 117(3), 489–501. [UR Fall Detection Dataset].
4. **Charfi, I., Miteran, J., Dubois, J., Atri, M., & Tourki, R. (2013).** Optimized spatio-temporal descriptors for real-time fall detection: comparison of support vector machine and AdaBoost-based classification. *Journal of Electronic Imaging*, 22(4), 041106. [Le2i Dataset].
5. **World Health Organization (WHO). (2021).** Step safely: strategies for preventing and managing falls across the life-course. *WHO Guidelines*, Geneva.
6. **Jacob, B., Kligys, S., Chen, B., Zhu, M., Tang, M., Howard, A., ... & Adam, H. (2018).** Quantization and training of neural networks for efficient integer-arithmetic-only inference. *CVPR 2018*, 2704–2713.
7. **Kipf, T. N., & Welling, M. (2017).** Semi-supervised classification with graph convolutional networks. *ICLR 2017*.
8. **Shi, L., Zhang, Y., Cheng, J., & Lu, H. (2019).** Two-stream adaptive graph convolutional networks for skeleton-based action recognition. *CVPR 2019*, 12026–12035.
9. **European Union. (2016).** Regulation (EU) 2016/679 of the European Parliament and of the Council (General Data Protection Regulation - GDPR). *Official Journal of the European Union*, L119, 1–88.
10. **Microsoft. (2021).** ONNX Runtime: cross-platform, high performance ML inferencing and training accelerator. *https://onnxruntime.ai*
11. **Upton, E., & Halfacree, G. (2024).** Raspberry Pi 5 Technical Documentation and Architecture Manual. *Raspberry Pi Ltd*.
12. **Cao, Z., Hidalgo, G., Simon, T., Wei, S. E., & Sheikh, Y. (2019).** OpenPose: Realtime multi-person 2D pose estimation using Part Affinity Fields. *IEEE TPAMI*, 43(1), 172–186.
13. **Martínez-Villaronga, F. J., et al. (2022).** UP-Fall Detection dataset: A multimodal approach. *Sensors*, 19(9), 1988.
14. **Carcagnì, P., et al. (2020).** Investigation of fall detection systems based on human skeleton and temporal convolution. *IEEE Access*, 8, 147571–147582.
15. **Chen, L., et al. (2019).** A Survey on Fall Detection: Principles, Sensors and Machine Learning. *IEEE Sensors Journal*, 19(17), 7114–7132.
16. **Si, C., Chen, W., Wang, W., Wang, L., & Tan, T. (2019).** An attention enhanced graph convolutional LSTM network for skeleton-based action recognition. *CVPR 2019*, 1227–1236.
17. **Duan, H., Zhao, Y., Chen, K., Lin, D., & Dai, B. (2022).** Revisiting skeleton-based action recognition: PoseConv3D. *CVPR 2022*, 2969–2978.
18. **Eurostat. (2023).** Population structure and ageing statistics in the European Union. *Eurostat Statistics Explained*, European Commission.
19. **ARM Ltd. (2022).** ARM Architecture Reference Manual: ARMv8, for ARMv8-A architecture profile (NEON SIMD and Dot Product instructions). *ARM Documentation*.
20. **Micucci, D., Mobilio, M., & Napoletano, P. (2017).** UniMiB SHAR: A dataset for human activity recognition using acceleration data. *Applied Sciences*, 7(10), 1101.
21. **Kwolek, B., & Kepski, M. (2015).** Improving fall detection by the use of depth data and infrared sensors. *Neurocomputing*, 168, 637–645.
22. **Nwoye, C. I., et al. (2019).** Data-driven fall detection using wearable sensors and deep learning. *IEEE TBME*, 66(4), 1002–1012.
"""

print("[OK] Part 4 (revised) written successfully.")
