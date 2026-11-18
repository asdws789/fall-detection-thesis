# -*- coding: utf-8 -*-
"""
Part 3 of the Thesis Research & Implementation Plan
Contains:
- 7. Kísérleti módszertan és modellfejlesztés
- 8. Kiértékelési metrikák, tesztelési keretrendszer és benchmark
- 9. Szoftverterv, architektúra és prototípus
"""

PART3_MD = r"""## 7. Kísérleti módszertan és modellfejlesztés

### 7.1 Osztályozási kategóriák és feladat-taxonómia
A kutatás során három fokozatban vizsgáljuk az agresszió-felismerési feladatot, lehetővé téve az elméleti és gyakorlati kompromisszumok pontos feltárását:

1. **Bináris Osztályozás (Baseline Task):**
   * Osztály 0: Nem erőszakos cselekvés (Séta, állás, beszélgetés, tánc).
   * Osztály 1: Erőszak / Verekedés (Ütés, rúgás, birkózás, lökés).
   * *Cél:* Közvetlen összehasonlíthatóság az RWF-2000 és CCTV-Fights szakirodalmi eredményeivel.
2. **Háromosztályos Korai Figyelmeztető Feladat (Main Proposed Task):**
   * Osztály 0: Nyugodt / Normál mozgás (Állás, séta, enyhe gesztusok, rendezett tánc).
   * Osztály 1: Feszültség / Pre-agresszió (Lökdösődés, heves mellkasnak feszülés, rángatás, fenyegető közeledés).
   * Osztály 2: Akut Verekedés (Aktív ütések, földharc, durva fizikai kontaktus).
   * *Cél:* A biztonsági beavatkozási időablak maximalizálása a lökdösődési fázis azonosításával.
3. **Négyosztályos Finomhangolt Taxonómia (Fine-Grained Extension):**
   * Osztály 0: Normál interakció.
   * Osztály 1: Intenzív / Ritmikus tánc (Hard Negative Class).
   * Osztály 2: Lökdösődés és konfliktus.
   * Osztály 3: Verekedés.
   * *Cél:* A tánc és verekedés közötti téves riasztások mélyreható statisztikai elemzése.

### 7.2 Baseline 1: Statisztikai ízületi szögek + Random Forest / XGBoost
Az ST-GCN hozzáadott értékének egzakt bizonyításához (RQ2) felépítünk egy klasszikus, szakirodalomban gyakran alkalmazott kinematikai baseline modellt (Aparicio Borjas et al., 2026 nyomán).

#### Jellemzőkinyerés a vázból (Feature Engineering):
Minden képkockán kiszámítjuk a biomechanikailag releváns ízületi szögeket három szomszédos pont között:
$$\theta = \arccos\left(\frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}\right)$$
Kiemelt szögek:
* Könyökszögek (váll-könyök-csukló mindkét oldalon).
* Vállszögek (csípő-váll-könyök).
* Térdszögek (csípő-térd-boka).
* Törzshajlási szög (vállközép-csípőközép a vertikális tengelyhez képest).

Az időablakon belül ($T=48$) a szögekből és azok első/második deriváltjából (szögsebesség $\omega = \frac{\Delta\theta}{\Delta t}$, szöggyorsulás $\alpha = \frac{\Delta\omega}{\Delta t}$) leíró statisztikai mutatókat generálunk:
* Átlag, szórás, minimum, maximum, interkvartilis terjedelem (IQR).
* Végtagok közötti távolságok és relatív közeledési sebességek (pl. a két csukló távolsága, csuklók távolsága a másik személy fejétől).

Az így előálló ~120-dimenziós jellemzővektorra egy erősen regularizált Random Forest (500 döntési fa, max_depth=15) és egy XGBoost modellt illesztünk.

### 7.3 Baseline 2: Szekvenciális Recurrent Modell (Bi-LSTM / GRU)
Második összehasonlító alapként egy Bidirectional LSTM modellt valósítunk meg, amely közvetlenül a normalizált koordináták időbeli sorozatát dolgozza fel anélkül, hogy ismerné a test anatómiai gráftopológiáját. Ez megmutatja, hogy a tiszta szekvencia-modellezés mire képes a gráf-alapú térbeli kapcsolatok nélkül.

### 7.4 A javasolt modell: ST-GCN és Two-Stream ST-GCN
A kutatás gerincét képező ST-GCN architektúra felépítése:
* **Bemeneti réteg:** Batch normalizáció a $(C=3, T=48, V=17, M=2)$ tenzoron.
* **ST-GCN Blokkok:** 9 egymásra épülő tér-időbeli konvolúciós blokk.
  * Blokkok 1-3: 64 csatorna, stride=1 (alacsony szintű geometriai összefüggések).
  * Blokkok 4-6: 128 csatorna, időbeli stride=2 a 4. blokkban (időbeli aggregáció).
  * Blokkok 7-9: 256 csatorna, időbeli stride=2 a 7. blokkban (magas szintű szemantikai fúzió).
* Minden blokk tartalmaz egy Spatial Graph Convolution réteget (Spatial Configuration Partitioning, 3 partíciós maszkkal), egy Batch Normalization réteget, ReLU aktivációt, egy Temporal Convolution réteget ($9 \times 1$ kernellel), Dropout réteget ($p=0.5$), valamint reziduális (Residual / Skip) kapcsolatot.
* **Globális Pooling és Osztályozó Fej:** Tér-időbeli Global Average Pooling (GAP), amely a jellemzőket egyetlen 256-dimenziós vektorrá simítja, majd egy Fully Connected réteg és Softmax adja meg az osztályvalószínűségeket.

#### Kétáramú (Two-Stream) fúzió:
Párhuzamosan betanítunk egy második, azonos felépítésű hálózatot a csont-vektorokra (Bone Stream). A tesztelés során a két modell kimeneti logitjait súlyozott fúzióval egyesítjük:
$$P_{final} = \lambda \cdot P_{joint} + (1 - \lambda) \cdot P_{bone}, \quad \lambda = 0.6$$

### 7.5 Tanítási protokoll, veszteségfüggvény és hiperparaméterek
Az agresszió-adatbázisokban a normál viselkedés jóval gyakoribb, mint a verekedés (osztály-kiegyensúlyozatlanság). Ennek kezelésére standard Cross-Entropy helyett **Focal Loss**-t alkalmazunk:
$$\mathcal{L}_{focal} = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$
Ahol $\gamma = 2.0$ a fókuszáló paraméter (amely lecsökkenti a könnyen osztályozható minták súlyát), $\alpha_t$ pedig az osztálysúly.

#### Optimalizálási konfiguráció:
* **Optimalizáló:** AdamW súlycsökkenéssel (Weight decay: $10^{-4}$).
* **Kezdeti tanulási ráta:** $\eta_0 = 10^{-3}$.
* **Ütemező (Scheduler):** Cosine Annealing Learning Rate ütemezés 50 korszakon (epoch) keresztül, minimum tanulási ráta $\eta_{min} = 10^{-6}$.
* **Batch méret:** 32 vagy 64 (hardverkapacitástól függően).
* **Early Stopping:** 10 korszak türelmi idő (Patience) a validációs loss alapján a túltanulás megakadályozására.
* **Keresztvalidáció:** Stratifikált 5-szörös keresztvalidáció (5-Fold Cross Validation), szigorúan figyelve arra, hogy ugyanannak a személynek vagy jelenetnek a részei ne kerülhessenek egyszerre a tanító és tesztelő halmazba (Subject-independent split).

---

## 8. Kiértékelési metrikák, tesztelési keretrendszer és benchmark

A rendszer minőségét nem csupán statikus gépi tanulási metrikákkal, hanem valós operatív biztonsági mutatókkal is értékeljük.

### 8.1 Klasszifikációs metrikák
* **Pontosság (Accuracy):**
  $$Acc = \frac{TP + TN}{TP + TN + FP + FN}$$
* **Precízió (Precision) és Szenzitivitás (Recall / True Positive Rate):**
  $$Precision = \frac{TP}{TP + FP}, \quad Recall = \frac{TP}{TP + FN}$$
* **F1-Score és Makro F1-Score:**
  $$F_1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}$$
  Többosztályos környezetben a Makro F1 ($F1_{macro}$) biztosítja, hogy a kisebbségi erőszakos osztályok teljesítménye egyenrangúan jelenjen meg az értékelésben.
* **Konfúziós Mátrix (Confusion Matrix):**  
  Megmutatja az osztályok közötti tévesztéseket, különös fókusszal a [Tánc $\rightarrow$ Verekedés] hibákra.
* **ROC-AUC és PR-AUC Görbék:**  
  A Receiver Operating Characteristic és Precision-Recall görbék alatti terület, amely a döntési küszöbtől független szeparálhatóságot méri.

### 8.2 Valós idejű és operatív felügyeleti metrikák
A biztonsági személyzet szempontjából a statikus képi pontosságnál fontosabb a riasztások megbízhatósága:

* **Óránkénti Téves Riasztási Arány (False Positive Alarm Rate per Hour - FPAR/h):**
  $$FPAR = \frac{\text{Tévesen generált riasztások száma}}{\text{Megfigyelt órák száma}}$$
  Egy használható rendszerben a cél: $FPAR < 1.0$ riasztás/óra egy tipikus tánctéri kameránál.
* **Érzékelési Késleltetés (Detection Latency):**  
  Az az időkülönbség, amely a verekedés fizikai megindulása ($t_{fight\_start}$) és a riasztási küszöb átlépése ($t_{alert}$) között eltelik:
  $$\Delta t_{detect} = t_{alert} - t_{fight\_start}$$
  Célérték: $\Delta t_{detect} \le 1.2$ másodperc.
* **Korai Előrejelzési Horizont (Early Warning Horizon):**  
  Temporálisan annotált tesztvideókon mérve: a lökdösődés kezdetétől az első súlyos testi ütésig eltelő időintervallum, amely alatt a rendszer sárga riasztást küld a személyzetnek.

### 8.3 Számítási teljesítmény és erőforrás-kihasználtság
A hardveres megvalósíthatóság igazolására méréseket végzünk az alábbi paraméterekre:
* **FPS (Frames Per Second):** A feldolgozott képkockák száma másodpercenként.
* **Komponensenkénti Profilozás (Pipeline Latency Breakdown):**
  * Videó dekódolás és kép-előkészítés (OpenCV): cél $< 3$ ms.
  * YOLOv8-Pose pózbecslés (TensorRT / PyTorch FP16): cél $< 15$ ms.
  * ByteTrack asszociáció: cél $< 2$ ms.
  * Normalizálás és pufferelés: cél $< 1$ ms.
  * ST-GCN inferencia (PyTorch FP16): cél $< 5$ ms.
  * Döntési logika és megjelenítés: cél $< 4$ ms.
  * **Teljes futási időkeret:** $\approx 30$ ms $\rightarrow \ge 33$ FPS.
* **VRAM és Memória lábnyom:** A modell GPU memóriahasználata (cél: $< 3$ GB VRAM a könnyű elérhetőség érdekében).

---

## 9. Szoftverterv, architektúra és prototípus

### 9.1 Technológiai stack és függőségek
A szoftverprototípus az iparban és akadémiai szférában legstabilabbnak számító nyílt forráskódú komponensekre támaszkodik:
* **Programozási nyelv:** Python 3.11+ (stabil C-API integrációk és aszinkron támogatás).
* **Mélytanulási keretrendszer:** PyTorch 2.3+ (CUDA 12.x támogatással, TorchScript / TensorRT exportálási lehetőséggel).
* **Számítógépes látás és pózbecslés:** Ultralytics (YOLOv8-Pose `yolov8n-pose.pt` vagy `yolov8s-pose.pt`), OpenCV-Python (képfolyam-kezelés, videó renderelés).
* **Követés és Gráfmodellezés:** ByteTrack / BoT-SORT (Ultralytics beépített tracker), PYSKL / MMAction2 referencia-struktúrák adaptációja.
* **Numerikus számítások:** NumPy, SciPy, Scikit-learn (baseline modellek és metrikák).
* **Operátori felület (Dashboard):** Streamlit vagy beágyazott OpenCV GUI valós idejű telemetriával és riasztási overlay-jel.

### 9.2 Moduláris könyvtár- és kódstruktúra
A projekt professzionális, moduláris könyvtárszerkezetben kerül megvalósításra:

```
C:\uni_stuff\anti_thesis\
│
├── configs/                        # Konfigurációs fájlok (YAML)
│   ├── dataset_rwf2000.yaml        # Adatbázis elérési utak és hiperparaméterek
│   ├── model_stgcn.yaml            # ST-GCN réteg- és tanítási paraméterek
│   └── inference_pipeline.yaml     # Éles követési és riasztási küszöbértékek
│
├── data/                           # Adatkönyvtár
│   ├── raw_videos/                 # Nyers teszt- és referenciavideók
│   ├── skeletons_extracted/        # Kinyert kulcspontok (.npy és .pkl formátumban)
│   └── staged_nightclub/           # Saját rögzítésű szórakozóhelyi szcenáriók
│
├── src/                            # Forráskód könyvtár
│   ├── __init__.py
│   ├── capture/                    # Videó beolvasó és RTSP kliens (többszálú)
│   │   ├── stream_reader.py
│   │   └── frame_buffer.py
│   ├── pose/                       # Pózbecslő és követő modul
│   │   ├── yolo_pose_detector.py
│   │   └── tracker_wrapper.py
│   ├── graph/                      # Gráfreprezentáció és adat-előkészítés
│   │   ├── skeleton_normalizer.py
│   │   ├── graph_topology.py       # COCO-17 szomszédsági mátrixok generálása
│   │   └── augmentation.py         # Tér-időbeli adatbővítés
│   ├── models/                     # Gépi tanulási és mélytanulási modellek
│   │   ├── baseline_rf.py          # Random Forest baseline modell
│   │   ├── baseline_lstm.py        # LSTM szekvenciális modell
│   │   ├── stgcn_layers.py         # Gráfkonvolúciós és TCN rétegek
│   │   └── stgcn_network.py        # Teljes ST-GCN architektúra
│   ├── engine/                     # Tanítási és validálási motor
│   │   ├── trainer.py              # Loss, optimizer, checkpoint kezelés
│   │   └── evaluator.py            # Metrikaszámítás, konfúziós mátrix rajzolás
│   ├── pipeline/                   # Valós idejű feldolgozási lánc
│   │   ├── real_time_worker.py     # Pipeline koordinátor
│   │   └── alert_manager.py        # Hiszterézis és riasztáslogika
│   └── ui/                         # Felhasználói felület és vizualizáció
│       ├── skeleton_renderer.py    # Váz kirajzolása a videóra
│       └── dashboard_app.py        # Operátori riasztási felület
│
├── tests/                          # Egységtesztek és integrációs tesztek
├── notebooks/                      # Kutatási jegyzetfüzetek (EDA, vizualizáció)
├── requirements.txt                # Python függőségek listája
└── README.md                       # Telepítési és futtatási útmutató
```

### 9.3 Többszálú (Multi-Threaded) feldolgozási architektúra
A valós idejű működés biztosításához az I/O műveleteket és a GPU számítást szét kell választani. Ha a videó beolvasása, a dekódolás, a neurális hálózat futtatása és a képernyőre rajzolás egyetlen szálon történne, a rendszer az I/O blokkolások miatt másodpercenként több képkockát veszítene.

Három független szálat (Worker Threads) alkalmazunk Python `queue.Queue` pufferekkel összekötve:
1. **Thread 1 (Capture Worker):** Folyamatosan olvassa az RTSP adatfolyamot, és a legfrissebb képkockát egy 2 elemű FIFO sorba helyezi (Drop-on-overflow stratégiával, elkerülve a puffer-késleltetést).
2. **Thread 2 (Inference Worker):** Kiveszi a képkockát, meghívja a YOLOv8-Pose modellt, frissíti a ByteTrack-et, és futtatja az ST-GCN osztályozót. A predikciókat és a vázakat továbbadja a renderelőnek.
3. **Thread 3 (Display & Alert Worker):** Kirajzolja a vázakat (zöld: normál, sárga: figyelmeztetés, piros: verekedés), megjeleníti a telemetriai adatokat (FPS, személyenkénti osztályvalószínűség), és hangjelzést vagy hálózati webhook riasztást küld.

### 9.4 Az operátori kezelőfelület (Dashboard) működése
A rendszer egy egyszerű, könnyen áttekinthető kezelőfelületet biztosít a biztonsági operátor számára:
* **Fő videónézet:** A kamerakép, amelyen a személyek fölött azonosító címke és aktuális státusz jelenik meg. A vázak színe azonnal jelzi az állapotot:
  * Zöld: Normál mozgás / Tánc ($P < 0.40$).
  * Sárga villogás: Lökdösődés / Feszült pre-agresszió ($0.40 \le P < 0.75$).
  * Piros pulzálás + Képernyőkeret: Verekedés ($P \ge 0.75$).
* **Eseménynapló (Incident Log):** Táblázatos formában rögzíti az esemény időbélyegét, a kamera azonosítóját, az érintett személyek `track_id`-jét és a csúcs-valószínűséget.
* **Exportálás:** Gombnyomásra elmenti a kritikus esemény előtti és utáni 5 másodperc vázadatait és a videórészletet belső vizsgálathoz.
"""

print("Part 3 defined successfully.")
