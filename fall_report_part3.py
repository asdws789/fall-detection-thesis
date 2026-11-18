# -*- coding: utf-8 -*-
"""
Szakdolgozati Beszámoló és Részletes Kutatási Terv (Esésdetektálás + Raspberry Pi Edge AI)
3. RÉSZ (Átdolgozott):
- 4. Fejezet (Rendszerarchitektúra, Cloud GPU + RPi hardverspecifikáció, UML diagramok, M=1 tenzor)
- 5. Fejezet (Empirikus Esettanulmány: A Törpe-Osztó Anomália levezetése és javítása)
"""

PART3_MD = r"""## 4. Rendszerarchitektúra és szoftverspecifikáció (UML tervezés)

### 4.1 Végponttól-végpontig tartó (End-to-End) adatfolyam architektúra
A rendszer valós idejű működését egy moduláris, aszinkron adatfolyam biztosítja, amely a fizikai kameraszenzortól a riasztási eseményig terjed.

```mermaid
flowchart TD
    subgraph Bemenet és Előfeldolgozás
        A["Kamera Bemenet (Raspberry Pi Cam v3 / USB)"] --> B["Képkocka Beolvasás (OpenCV / V4L2)"]
        B --> C["YOLOv8n-Pose INT8 Inferencia (ONNX Runtime ARM NEON)"]
    end

    subgraph Gráf Előkészítés
        C --> D["17 Kulcspont Kinyerése (x, y, conf)"]
        D --> E["Térbeli Normalizálás (Csípőközép & Testhossz)"]
        E --> F["Csúszóablak Puffer (T=32 frame, ~1.0 s)"]
        F --> G["Tér-Időbeli Tenzor: (1, 3, 32, 17, 1)"]
    end

    subgraph Osztályozás és Döntés
        G --> H["ST-GCN Gráfmodell Inferencia (INT8 ONNX)"]
        H --> I["Kimeneti Valószínűségek (Softmax)"]
        I --> J["Háromfázisú Hiszterézis Szűrő (Temporal Filter)"]
    end

    subgraph Állapot és Riasztás
        J --> K{"Döntési Állapot"}
        K -- "Normál mozgás (Séta, Állás, Ülés)" --> L["Zöld állapot (Csendes monitorozás)"]
        K -- "ESÉS ÉSZLELVE!" --> M["VÉSZHELYZETI RIASZTÁS!"]
        M --> N1["Helyi Buzzer / Sípoló Hangjelzés (GPIO)"]
        M --> N2["MQTT Eseményküldés (Home Assistant)"]
        M --> N3["Titkosított HTTPS Webhook / Telegram Vészjelzés"]
    end
```

---

### 4.2 Hardveres architektúra és számítási infrastruktúra specifikáció

A kutatás megvalósításához és a beágyazott futtatáshoz három hardverkörnyezet feladatait határoltuk el:
1. **Neurális modell tanítási és kísérleti platform (Cloud GPU Workstation):**
   * *Infrastruktúra:* Google Colab és Kaggle felhő alapú számítási környezet.
   * *Hardveres gyorsító:* Dedikált **Nvidia Tesla T4 GPU (16 GB GDDR6 VRAM)** vagy Nvidia Pascal P100 GPU.
   * *Szerepe:* Az ST-GCN mély gráfkonvolúciós hálózat és a Bi-LSTM baseline modellek 50–100 epochos betanítása az URFD és Le2i adathalmazokon, Focal Loss optimalizáció, valamint az INT8 poszt-tanítási kalibráció súlygenerálása. A felhős GPU garantálja a percek alatti lefutást, kiküszöbölve a CPU-s tanítás napokig tartó szűk keresztmetszetét.
2. **Helyi fejlesztői munkaállomás (Host PC):**
   * *Processzor:* AMD Ryzen 5 5500 (6 fizikai mag, 12 szál, 3.6 GHz alap / 4.2 GHz boost órajel, 16 MB L3 cache).
   * *Memória:* 16 GB DDR4 3200 MHz RAM.
   * *Operációs rendszer:* Windows 11 Home / Linux Ubuntu 22.04 LTS.
   * *Szerepe:* Helyi adatkezelés, videókocka-előkészítés, kulcspont-kinyerés, a naiv kinematikai baseline tesztelése és a lokális webkamerás diagnosztika.
3. **Beágyazott célhardver (Embedded Edge Device):**
   * *Alaplapi mikroszámítógép:* **Raspberry Pi 5** (vagy Raspberry Pi 4B fallback).
     * CPU: Broadcom BCM2712 négymagos ARM Cortex-A76 processzor @ 2.4 GHz (Pi 5), illetve BCM2711 négymagos Cortex-A72 @ 1.5 GHz (Pi 4B).
     * RAM: 4 GB vagy 8 GB LPDDR4X SDRAM.
     * Multimédia: VideoCore VII GPU, hardveres H.264 dekóder.
   * *Kamera interfész:* **Raspberry Pi Camera Module 3** (Sony IMX708 szenzor, széles látószögű 120°-os FOV objektívvel, 2-sávos MIPI CSI-2 interfésszel) vagy szabványos USB UVC kamera.
   * *Hűtés és ház:* Hivatalos aktív hűtőborda + PWM vezérelt ventilátor (Active Cooler) a termikus órajelfojtás (thermal throttling) megelőzésére.
   * *Tápellátás:* 27W USB-C PD tápegység (5V / 5A). Átlagos teljesítményfelvétel: 6–9 Watt.

---

### 4.3 UML Komponens-diagram (Component Diagram)

A szoftverrendszer moduláris architektúrája szétválasztja az adatbevitelt, a gépi látást, a gráfelemzést és a hálózati értesítéseket.

```mermaid
classDiagram
    class FrameCaptureService {
        +open_camera(device_id)
        +get_latest_frame() : np.ndarray
        +release()
    }
    class PoseEstimationEngine {
        -ort_session : InferenceSession
        +detect_keypoints(frame) : KeypointArray
    }
    class GraphPreprocessor {
        -buffer : CircularQueue[32]
        +normalize_skeleton(keypoints) : NormalizedKeypoints
        +build_st_tensor() : np.ndarray
    }
    class STGCNClassifier {
        -stgcn_session : InferenceSession
        +predict_action(tensor) : ActionProbabilities
    }
    class DecisionStateMachine {
        -current_state : State
        -time_on_floor : float
        +update(action_probs, orientation) : State
        +reset()
    }
    class EmergencyAlertService {
        +trigger_local_buzzer()
        +publish_mqtt(event)
        +send_telegram_alert(msg)
    }

    FrameCaptureService --> PoseEstimationEngine : nyers képkocka
    PoseEstimationEngine --> GraphPreprocessor : 17 kulcspont
    GraphPreprocessor --> STGCNClassifier : tér-időbeli tenzor
    STGCNClassifier --> DecisionStateMachine : esési valószínűség
    DecisionStateMachine --> EmergencyAlertService : vészjelzés aktiválása
```

---

### 4.4 UML Szekvencia-diagram (Sequence Diagram: Esés Detektálása és Riasztás)

Az alábbi diagram részletezi egy valós esési esemény időbeli lefolyását és az alrendszerek közötti szekvenciális üzenetváltásokat:

```mermaid
sequenceDiagram
    autonumber
    actor Felhasználó as Idős Személy
    participant Kamera as RPi Camera v3
    participant PoseEngine as YOLOv8-Pose (INT8)
    participant Preproc as Gráf Puffer & Normalizáló
    participant GCN as ST-GCN Gráf Hálózat
    participant StateMachine as Döntési Állapotgép
    participant Alert as Riasztási Szolgáltatás (IoT)
    actor Gondozó as Gondozó / Hozzátartozó

    Felhasználó->>Kamera: Elveszíti az egyensúlyát, a padlóra esik
    loop Minden képkocka (25 FPS)
        Kamera->>PoseEngine: Nyers képkocka átadása memóriában
        PoseEngine->>PoseEngine: 17 anatómiai kulcspont regressziója
        Note over PoseEngine: RGB kép azonnal megsemmisül a RAM-ból!
        PoseEngine->>Preproc: (x, y, conf) koordináták
        Preproc->>Preproc: Csípőközép normalizálás & csúszóablak bővítés
    end

    Preproc->>GCN: 32 képkockás tenzor: (1, 3, 32, 17, 1)
    GCN->>GCN: Tér-időbeli konvolúció (ST-GCN)
    GCN->>StateMachine: P(Fall) = 0.94 (Magas esési valószínűség)
    
    StateMachine->>StateMachine: Állapotváltás: DROP_DETECTED
    Note over StateMachine: 0.6 másodperces inaktivitási és fekvési ellenőrzés
    
    StateMachine->>StateMachine: Állapot megerősítése: FALLEN (Esés igazolva)
    StateMachine->>Alert: Riasztási parancs aktiválása (time_on_floor: 1.0s)
    
    par Helyi riasztás
        Alert->>Alert: Helyi GPIO sípoló (Buzzer) aktiválása
    and IoT Hálózati vészjelzés
        Alert->>Alert: MQTT üzenet küldése (Home Assistant)
        Alert->>Gondozó: Titkosított Telegram vészjelzés: "Esés észlelve!"
    end
```

---

### 4.5 UML Állapotgép-diagram (State Machine Diagram)

A téves riasztások elkerülését garantáló négyállapotú véges automata:

```mermaid
stateDiagram-v2
    [*] --> NORMAL : Rendszer indulása

    NORMAL --> DROP_DETECTED : Zuhanás észlelve (v_y > 0.5 vagy P(Fall) > 0.8)
    NORMAL --> FALLEN : Lassú esés / Tartós fekvés (Dőlésszög > 55° és t > 0.6s)

    DROP_DETECTED --> FALLEN : Vízszintes testtartás igazolva (Fekvés a padlón)
    DROP_DETECTED --> NORMAL : Visszaállás (Átmeneti leguggolás / cipőkötés, t > 0.8s)

    FALLEN --> FALLEN : Földön töltött idő növelése (time_on_floor += dt)
    FALLEN --> RECOVERY : Felállási mozdulat kezdete
    FALLEN --> NORMAL : Teljes felegyenesedés igazolva (Dőlésszög < 35° és AR < 0.85)

    RECOVERY --> NORMAL : Sikeres felállás
    RECOVERY --> FALLEN : Visszaesés a talajra
```

---

### 4.6 Térbeli normalizálás és csúszóablak képzés ($M=1$ tenzor)

A kamera előtti relatív távolság és az egyéni testmagasság hatásainak semlegesítésére minden mintavételezett vázat geometriai transzformációnak vetünk alá:
1. **Origó eltolása (Translation Invariance):** A test globális súlypontját, a csípőközéppontot ($C_{hip} = \frac{v_{11} + v_{12}}{2}$) választjuk új koordináta-eredőnek $(0, 0)$.
2. **Skálázás (Scale Invariance):** Minden kulcspont koordinátát elosztunk a pillanatnyi törzshosszal ($L_{torso} = \|C_{shoulder} - C_{hip}\|_2$), így a váz arányai függetlenné válnak a kameratávolságtól:
   $$\tilde{P}_i = \frac{P_i - C_{hip}}{L_{torso}}$$

A normalizált koordinátákból egy $T=32$ elemű FIFO körpuffer (Circular Buffer) épül fel. Az ST-GCN bemeneti tenzorának dimenziója:
$$\mathbf{X} \in \mathbb{R}^{B \times C \times T \times V \times M} = (1 \times 3 \times 32 \times 17 \times 1)$$
Ahol $B=1$ a batch méret, $C=3$ a csatornaszám ($x, y, conf$), $T=32$ az időablak, $V=17$ az ízületek száma, és $M=1$ az egyetlen felügyelt személy. Ha a képen átmenetileg többen tartózkodnak, a pózbecslő a legmagasabb megbízhatóságú dobozt választja ki.

---

### 4.7 Háromfázisú hiszterézis döntési logika és időmérés

A döntéshozatal nem egyetlen pillanatnyi képkockán alapul, hanem három szigorú fázist követel meg:
1. **1. Fázis: Dinamikai Zuhanás:** Az ST-GCN osztályozó magas valószínűséggel ($P_{fall} > 0.85$) jelzi az esési mozgásmintát, vagy a súlypont vertikális sebessége meghaladja a zuhanási küszöböt ($v_y > 0.5$).
2. **2. Fázis: Geometriai Orientáció:** A személy hossztengelye (vállközép és csípőközép egyenese) a függőlegessel bezárt szöge meghaladja az $55^{\circ}$-ot, és a befoglaló téglalap oldalaránya szélesség-dominánssá válik ($W/H > 1.15$).
3. **3. Fázis: Időbeli Megerősítés (Temporal Persistence):** A riasztás csak akkor válik véglegessé, ha a személy a zuhanást követően legalább $0.6$ másodpercen keresztül a földön marad. Ezzel megelőzhető a gyors leülés, ágyra huppanás vagy cipőkötés miatti hamis vészjelzés. Ha az állapot megerősítést nyer, a rendszer számlálni kezdi a **földön töltött időt** (`time_on_floor`), amelyet másodperc alapon rögzít és továbbít.

---

### 4.8 Hálózati értesítési és IoT alrendszer (Zero Pixel Leakage)

A rendszer tervezési filozófiája szerint a külvilág felé **semmilyen képi adat vagy videófolyam nem kerül kibocsátásra**. Esés észlelésekor kizárólag strukturált JSON metaadatok hagyják el az eszközt:

```json
{
  "event": "FALL_CONFIRMED",
  "device_id": "rpi5-living-room-01",
  "timestamp": "2026-10-31T17:15:20Z",
  "confidence": 0.962,
  "time_on_floor_seconds": 15.4,
  "torso_angle_deg": 78.5,
  "status": "UNRESPONSIVE"
}
```

* **MQTT Protokoll:** A Raspberry Pi a helyi okosotthon szerver (pl. Home Assistant) felé publikálja a telemetriát az `elderly/safety/fall` témakörben, amely felkapcsolhatja a világítást és értesítheti az ápolókat.
* **Titkosított Webhook / Telegram Bot:** Közvetlen push-értesítés a gondozó okostelefonjára, szöveges riasztással és a földön töltött idő frissítésével.
* **Helyi Vészcsengő (Hardware Buzzer):** A Raspberry Pi GPIO kimenetére kapcsolt zümmer azonnal hangjelzést ad. Ha a felhasználó képes felállni, a felállással a rendszer automatikusan némítja a riasztást.

---

## 5. Empirikus esettanulmány: A naiv kinematikai heurisztikák korlátai és a „törpe-osztó” (Dwarf-Denominator) anomália

### 5.1 A kiinduló kísérleti elrendezés
A szakdolgozati kutatás korai fázisában kifejlesztettünk és teszteltünk egy kézzel definiált szabályrendszerre épülő kinematikai esésdetektáló prototípust (`simple_fall_detector.py`). A cél az volt, hogy referencia-alapot (Baseline 1) képezzünk a később megvalósítandó ST-GCN mély tanulási modellhez, és felmérjük a webkamerás pózbecslés megbízhatóságát.

A naiv algoritmus a szakirodalomban leggyakrabban idézett három szabályt kombinálta:
1. Súlypont (csípőközép) vertikális sebessége:
   $$v_y = \frac{\Delta y_{com}}{H_{bbox} \cdot \Delta t} > 1.2\text{ testmagasság / másodperc}$$
2. Törzs dőlésszöge a függőlegeshez képest: $\theta > 55^{\circ}$
3. Bounding box oldalaránya (Aspect Ratio): $AR = \frac{W}{H} > 1.15$

### 5.2 A tapasztalt ellenmondásos viselkedés
A laboratóriumi szobai tesztek során a rendszer **két súlyos, paradox anomáliát mutatott**:
* **1. Anomália (Nem jelzett eséskor):** Amikor a tesztalany kontrolláltan a szőnyegre esett (elkerülve a sérülést), az esés időtartama $1.0-1.4\text{ másodpercig}$ tartott. A számított pillanatnyi zuhanási sebesség ($v_y \approx 0.45-0.70$) nem érte el a merev $1.2$-es határértéket. Mivel az állapotgép a fekvő pozíciót csak előzetes gyors zuhanási állapot után tekintette esésnek, a tesztalany földön fekvése alatt a rendszer tévesen **végig normál (zöld) állapotban maradt**.
* **2. Anomália (Riasztott felkeléskor):** Amikor a földön fekvő személy megkezdte a felkelést (letámaszkodott a karjával, megemelte a vállát), a kijelző váratlanul **pirosra váltott, és vészhelyzeti esésriasztást adott ki**!

```mermaid
flowchart TD
    subgraph A Naiv Kinematikai Hiba Menete
        A["1. Ember kontrolláltan elesik"] -->|Lassú zuhanás: v = 0.6 < 1.2| B["Rendszer: NORMÁL (Nincs esés!)"]
        B --> C["2. Ember a földön fekszik (H lecsökken 70 pixelre)"]
        C --> D["3. Ember megkezdi a felkelést (emelkedik 40 px-t)"]
        D -->|Osztás a törpe magassággal: 40px / 70px| E["Számított sebesség: 3.8 testmagasság/mp!"]
        E --> F["🚨 TÉVES PIROS RIASZTÁS FELKELÉSKOR!"]
    end
```

### 5.3 Matematikai és biomechanikai hibaok levezetése (Denominator Collapse)
A hibaelemzés feltárta a hiba egzakt matematikai forrását:
* **A „Törpe-osztó” (Dwarf-Denominator) jelenség:** A képlet a pillanatnyi befoglaló téglalap magasságával ($H_{bbox}$) normalizált. Álló embernél a magasság nagy ($H_{stand} \approx 350-450\text{ pixel}$). Fekvő embernél azonban a doboz magassága mindössze a fekvő test vastagságára, $H_{floor} \approx 60-80\text{ pixelre}$ zsugorodik össze!
* **Numerikus szingularitás:** Amikor a fekvő személy megmozdul a felkeléshez, a vállak minimális, mindössze $\Delta y \approx 40\text{ pixeles}$ elmozdulása a parányi nevező miatt extrém sebességugrást eredményez:
  $$v_{számított} = \frac{40\text{ px}}{70\text{ px} \cdot 0.15\text{ s}} \approx 3.81\text{ testmagasság/másodperc}$$
  Ez a számított érték több mint háromszorosa volt a zuhanási küszöbnek ($3.81 > 1.2$)!
* **Előjel-hiba és köztes póz:** A képi koordináta-rendszerben az origó a bal felső sarokban van, így a koordináták lefelé növekednek ($y \downarrow$). Felkeléskor a mozgás iránya felfelé mutat ($\Delta y < 0$). Az előjelkezeletlen vagy abszolútértékes modul a felfelé irányuló gyorsulást lefelé zuhanásként értelmezte. Mivel a felkelés első fázisában (térdelés, négykézláb póz) a test még döntött ($\theta > 40^{\circ}$) és széles ($AR > 1.0$), a naiv rendszer azonnal teljesültnek vette a fekvés és a zuhanás együttes feltételét.

### 5.4 A mérnöki javítás (Baseline V2 architektúra)
A hiba kiküszöbölésére a kinematikai modellt refaktoráltuk (`simple_fall_detector.py` V2):
1. **Skálainvariáns Dimenzió-Norma ($\text{ref\_dim}$):**  
   A sebesség számításánál a doboz pillanatnyi magassága helyett a befoglaló téglalap maximális dimenzióját rögzítjük:
   $$\text{ref\_dim} = \max(W_{bbox}, H_{bbox}, 50.0)$$
   Mivel az emberi test hossztengelye állva a magasságban ($H$), fekve pedig a szélességben ($W$) reprezentálódik, a $\max(W, H)$ közel állandó marad az esés és felkelés teljes folyamata alatt, megelőzve a nevező összeomlását.
2. **Előjelhelyes Vektoriális Irányvizsgálat:**  
   Szigorúan szétválasztottuk a lefelé zuhanást ($v_y > 0$) a felfelé emelkedéstől ($v_y < 0$). Felfelé irányuló mozgás esetén a rendszer azonnal blokkolja az esési állapotba lépést.
3. **Tartós Testtartás Analízis (Posture Persistence):**  
   A rendszer két önálló úton képes esést igazolni:
   * *A) Dinamikus út:* Jelentős zuhanás ($v_y > 0.5$) és vízszintes pozíció.
   * *B) Statikus út (Óvatos, tompított esés):* Ha a test vízszintesbe kerül ($\theta > 55^{\circ}$ vagy $W/H > 1.15$) és ebben a helyzetben marad legalább $0.6$ másodpercig, a rendszer sebességküszöb nélkül is validálja a vészhelyzetet.
4. **Felállási Rekupáció:**  
   Kiegyenesedéskor ($\theta < 35^{\circ}$ és $W/H < 0.85$) az állapotgép késleltetés nélkül visszaáll normál állapotba.

### 5.5 Tudományos konklúzió: Miért igazolja ez az ST-GCN szükségességét?
Ez az esettanulmány empirikus, kézzelfogható bizonyítékot szolgáltat arra, hogy a kézzel tervezett geometriai heurisztikák és merev határértékek rendkívül sérülékenyek a valós élet változatos szituációiban. Az ilyen lokális szabályok képtelenek komplex összefüggéseket modellezni.

Ez a mérnöki tapasztalat teremti meg a szakdolgozat tudományos létjogosultságát: a **Tér-Időbeli Gráfkonvolúciós Hálózat (ST-GCN)** alkalmazását. Az ST-GCN nem szorul kézzel beállított küszöbértékekre; a teljes csontváz-topológia időbeli koordináta-folyamát mély tanulási rétegekkel dolgozza fel, így természetes módon, robusztusan képes megkülönböztetni a felkelés, a leülés és a valós zuhanás komplex tér-időbeli fázisait.
"""

print("[OK] Part 3 (revised) written successfully.")
