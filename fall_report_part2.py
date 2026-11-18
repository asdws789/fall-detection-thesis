# -*- coding: utf-8 -*-
"""
Szakdolgozati Beszámoló és Részletes Kutatási Terv (Esésdetektálás + Raspberry Pi Edge AI)
2. RÉSZ: 3. Fejezet (Szakirodalmi áttekintés és elméleti háttér: YOLOv8-Pose, ST-GCN, INT8 Kvantálás & ARM NEON)
"""

PART2_MD = r"""## 3. Szakirodalmi áttekintés és elméleti háttér

### 3.1 2D Emberi Pózbecslés: Ultralytics YOLOv8-Pose
A rendszer bemeneti észlelési rétegét az Ultralytics által 2023-ban publikált **YOLOv8-Pose** architektúra alkotja, amely a valós idejű objektumdetektálás és kulcspont-regresszió ipari etalonjának számít.

```mermaid
flowchart LR
    A["Bemeneti Kép (RGB)"] --> B["CSPDarknet Backbone (Többskálás jellemzőkinyerés)"]
    B --> C["PANet Nyak (Feature Pyramid Fúzió)"]
    C --> D1["Detekciós Fej: Bounding Box (x, y, w, h)"]
    C --> D2["Osztályozási Fej: Személy konfidencia"]
    C --> D3["Pózbecslő Fej: 17 Kulcspont (x, y, conf)"]
```

#### Architekturális felépítés
1. **Backbone (Gerinchálózat):** Egy módosított CSPDarknet (Cross Stage Partial) struktúrát használ, amely C2f (Cross Stage Partial with 2 convolutions) modulokból épül fel. A C2f blokkok maradványkapcsolatokkal (residual connections) és párhuzamos gradiens-áramlásokkal maximalizálják a tanulási kapacitást, miközben minimalizálják a lebegőpontos műveletek számát (FLOPs).
2. **Neck (Nyak):** Egy Path Aggregation Network (PANet) struktúra, amely felfelé és lefelé irányuló piramis-fúzióval egyesíti a korai rétegek finom térbeli felbontását a mély rétegek szemantikai gazdagságával. Ez garantálja, hogy a távolabb álló vagy fekvő emberi alakzatok kis méretű végtagjai is pontosan lokalizálhatók maradnak.
3. **Decoupled Pose Head (Szétválasztott pózbecslő fej):** A korábbi YOLO verziókkal ellentétben a doboz-regresszió, az osztályozás és a kulcspont-predikció különálló konvolúciós ágakon történik.

#### A COCO-17 ízületi topológia
A hálózat az emberi testet 17 darab kulcsponttal reprezentálja:
* **Fej (0–4):** 0: Orr, 1: Bal szem, 2: Jobb szem, 3: Bal fül, 4: Jobb fül.
* **Felsőtest és karok (5–10):** 5: Bal váll, 6: Jobb váll, 7: Bal könyök, 8: Jobb könyök, 9: Bal csukló, 10: Jobb csukló.
* **Alsótest és lábak (11–16):** 11: Bal csípő, 12: Jobb csípő, 13: Bal térd, 14: Jobb térd, 15: Bal boka, 16: Jobb boka.

#### Object Keypoint Similarity (OKS) Veszteségfüggvény
A pózbecslő fej tanítása nem sima euklideszi távolságon, hanem a biometrikusan skálázott OKS metrikán alapszik:
$$OKS = \frac{\sum_{i=0}^{16} \exp\left(-\frac{d_i^2}{2 s^2 \sigma_i^2}\right) \delta(v_i > 0)}{\sum_{i=0}^{16} \delta(v_i > 0)}$$
Ahol:
* $d_i$ a becsült és a valós kulcspont közötti euklideszi távolság pixelben.
* $s$ a személy befoglaló téglalapjának skálája ($s = \sqrt{W \cdot H}$).
* $\sigma_i$ az adott ízület per-osztály szórása (a térd és boka $\sigma$-ja nagyobb a laza mozgásszabadság miatt, míg a szemek és orr $\sigma$-ja kicsi a merev anatómiának köszönhetően).
* $v_i$ a láthatósági jelző ($v_i > 0$ ha a pont nincs kitakarva), $\delta(\cdot)$ a Dirac-delta indikátor.

### 3.2 Tér-Időbeli Gráfkonvolúciós Hálózatok (ST-GCN)
A Yan et al. (AAAI 2018) által bevezetett **Spatio-Temporal Graph Convolutional Network (ST-GCN)** elméleti áttörést hozott az emberi cselekvésfelismerésben: az emberi csontvázat egy olyan dinamikus, nem-euklideszi gráfként definiálja, amely a térbeli anatómiát és az időbeli dinamikát egyetlen összefüggő tenzorként képes feldolgozni.

#### A tér-időbeli gráf definíciója
A gráf formális leírása:
$$\mathcal{G} = (\mathcal{V}, \mathcal{E})$$
* **Csúcsok ($\mathcal{V}$):** Az időablakban ($T$) megjelenő összes anatómiai ízület:
  $$\mathcal{V} = \{v_{ti} \mid t = 1, \dots, T; \, i = 1, \dots, N\}$$
  Jelen szakdolgozatban $N = 17$ ízület és $T = 32$ képkocka (~1.0 másodperc $30\text{ FPS}$ mellett).
* **Élek ($\mathcal{E}$):** Két diszjunkt élhalmaz uniója:
  1. *Térbeli élek ($\mathcal{E}_S$):* Az azonos időpillanatban ($t$) létező fizikai csontok az ízületek között:
     $$\mathcal{E}_S = \{(v_{ti}, v_{tj}) \mid (i, j) \in H\}$$
     Ahol $H$ az emberi csontváz anatómiai kapcsolatainak halmaza (pl. váll-csípő, csípő-térd, térd-boka).
  2. *Időbeli élek ($\mathcal{E}_T$):* Ugyanazon ízület egymást követő képkockák közötti időbeli összeköttetése:
     $$\mathcal{E}_T = \{(v_{ti}, v_{(t+1)i})\}$$

```mermaid
graph TD
    subgraph Időpillanat t
        S1["Váll (5,6)"] --- H1["Csípő (11,12)"]
        H1 --- K1["Térd (13,14)"]
        K1 --- A1["Boka (15,16)"]
    end
    subgraph Időpillanat t+1
        S2["Váll (5,6)"] --- H2["Csípő (11,12)"]
        H2 --- K2["Térd (13,14)"]
        K2 --- A2["Boka (15,16)"]
    end
    S1 -. "Időbeli él" .-> S2
    H1 -. "Időbeli él" .-> H2
    K1 -. "Időbeli él" .-> K2
    A1 -. "Időbeli él" .-> A2
```

#### A Térbeli Gráfkonvolúció Művelete
Egy tetszőleges $v_i$ csúcson a térbeli konvolúció a szomszédos ízületek jellemzőinek súlyozott aggregációjaként írható fel:
$$f_{out}(v_i) = \sum_{v_j \in B(v_i)} \frac{1}{Z_{ij}} f_{in}(v_j) \cdot W(l_i(v_j))$$
Ahol:
* $B(v_i) = \{v_j \mid d(v_i, v_j) \le 1\}$ az 1-távolságú (közvetlen) szomszédok halmaza.
* $Z_{ij} = |B(v_j)|$ a fokszám-alapú normalizáló tényező.
* $W$ a tanulható súlymátrix.
* $l_i(v_j)$ a partíciós címkéző függvény.

#### Spatial Configuration Partíciós Stratégia
A sima konvolúcióval ellentétben a gráfokon a szomszédoknak nincs természetes sorrendje. Az ST-GCN a szomszédságot $K=3$ csoportra bontja a test globális súlypontjához (csípőközép) viszonyított távolság alapján:
1. **Gyökércsoport ($K=0$):** Maga a vizsgált csúcs ($v_i$).
2. **Centripetális csoport ($K=1$):** Azok a szomszédok, amelyek közelebb helyezkednek el a súlyponthoz, mint $v_i$.
3. **Centrifugális csoport ($K=2$):** Azok a szomszédok, amelyek távolabb vannak a súlyponttól, mint $v_i$.

Mátrixos reprezentációban a teljes térbeli gráfkonvolúciós réteg:
$$f_{out} = \sum_{k=0}^{2} \Lambda_k^{-\frac{1}{2}} (A_k \odot M_k) \Lambda_k^{-\frac{1}{2}} f_{in} W_k$$
Ahol:
* $A_k$ a $k$-adik partícióhoz tartozó bináris szomszédsági mátrix ($17 \times 17$).
* $\Lambda_k^{ii} = \sum_j A_k^{ij} + \epsilon$ a normalizáló fokszámmátrix.
* $M_k$ egy tanulható fontossági maszk (Learnable Edge Weight Matrix), amely megtanulja, hogy esés közben mely csontkapcsolatok (pl. gerinc dőlése) bírnak nagyobb diagnosztikai súllyal.

#### Időbeli Konvolúció (TCN)
A térbeli kapcsolatok leképezése után a jellemzőket egy időbeli konvolúciós réteg (TCN) dolgozza fel. Ez egy klasszikus 1D konvolúció $K_t \times 1$ méretű szűrővel (jellemzően $9 \times 1$), amely az időtengely mentén rögzíti az ízületek gyorsulását, lassulását és trajektóriáját. A teljes ST-GCN hálózat 9 egymásra épülő tér-időbeli blokkból (ST-GCN Unit) áll, BatchNorm és Dropout rétegekkel kiegészítve.

---

### 3.3 Beágyazott mélytanulás és modell-kvantálás ARM architektúrára

A Raspberry Pi típusú beágyazott eszközökön a mély tanulási modellek közvetlen (FP32) futtatása a korlátozott memória-sávszélesség és a dedikált lebegőpontos tenzormagok hiánya miatt szűk keresztmetszetet jelent. A valós idejű futás kulcsa a **poszt-tanítási kvantálás (Post-Training Quantization - PTQ)** és az **ARM NEON SIMD optimalizáció**.

#### Az INT8 Kvantálás Matematikai Elmélete
A kvantálás célja a folytonos 32 bites lebegőpontos értékek ($r \in \mathbb{R}$, FP32) leképezése 8 bites előjeles vagy előjeltelen egészekre ($q \in \mathbb{Z}$, INT8, $[-128, 127]$ tartomány):
$$q = \text{round}\left(\frac{r}{S}\right) + Z$$
Ahol:
* $S$ (Scale factor) a skálázási tényező: egy pozitív valós lebegőpontos szám, amely az adatok dinamikatartományát határozza meg:
  $$S = \frac{r_{max} - r_{min}}{q_{max} - q_{min}} = \frac{r_{max} - r_{min}}{255}$$
* $Z$ (Zero-point) a valós nulla értékének megfelelő diszkrét egész eltolás (aszimmetrikus kvantálás esetén). Súlyok esetében szimmetrikus kvantálást ($Z = 0$) alkalmazunk, ami egyszerűsíti a hardveres szorzási műveletet:
  $$q = \text{clip}\left(\text{round}\left(\frac{r}{S}\right), -128, 127\right)$$

A dekvantálás művelete az eredeti érték visszaállítására:
$$\tilde{r} = S \cdot (q - Z)$$

```mermaid
flowchart LR
    A["FP32 Lebegőpontos Tenzor (4 Bájt / elem)"] --> B["Kalibrációs Adathalmaz (Min/Max statisztika)"]
    B --> C["Súlyok & Aktivációk Kvantálása (Scale S, Zero-point Z)"]
    C --> D["INT8 Fixpontos Tenzor (1 Bájt / elem)"]
    D --> E["75% Memóriamegtakarítás + 2.5x Gyorsabb ARM NEON Futás"]
```

#### Előnyök a beágyazott végponton
1. **Memóriaméret csökkentése:** A modell súlyfájljának és munka-memóriájának foglalása pontosan a negyedére ($75\%$-os csökkenés) esik vissza (pl. egy 12 MB-os modell mindössze 3 MB-ot igényel). Ez drasztikusan tehermentesíti a Raspberry Pi RAM sávszélességét.
2. **Gyorsítótár (L1/L2 Cache) hatékonyság:** A kisebb tenzorok kényelmesen elférnek a processzormagok szűk L2 gyorsítótárában, minimalizálva a lassú főmemória-elérések számát.

#### ARM NEON SIMD Vektoros Utasításkészlet
A Raspberry Pi processzoraiban található ARM Cortex-A magok (Cortex-A72 a Pi 4-ben, Cortex-A76 a Pi 5-ben) 128 bites **NEON SIMD (Single Instruction Multiple Data)** vektorregiszterekkel rendelkeznek. 

Egyetlen órajelciklus alatt:
* FP32 esetén: legfeljebb 4 lebegőpontos szorzás hajtható végre ($128 / 32 = 4$).
* INT8 esetén: a dedikált NEON vektorutasítások (pl. `SDOT` – Signed Dot Product) **egyetlen órajelciklus alatt négy pár 8 bites egész szorzatát adják hozzá egy 32 bites akkumulátorhoz**, így órajelenként akár **16 párhuzamos művelet** fut le magonként!

#### Beágyazott Inferencia Motorok Összehasonlítása

| Szempont | PyTorch Native (CPU) | ONNX Runtime (ARM64) | Tencent NCNN | Google TFLite |
| :--- | :--- | :--- | :--- | :--- |
| **Célplatform** | Asztali gép, szerver | Bármely architektúra | Speciálisan beágyazott ARM | Mobil, beágyazott |
| **INT8 Támogatás** | Korlátozott | **Kiváló (ORT Quantizer)** | Nagyon jó | Jó |
| **ARM NEON kihasználás** | Közepes | **Automatikus és optimális** | Kézzel assemblyben kódolt | Jó |
| **YOLOv8 & ST-GCN kompatibilitás** | Natív | **Teljes (Mindkét modell fut)** | Egyedi réteg-átalakítás kell | Nehézkes ST-GCN-re |
| **Késleltetés Raspberry Pi 5-ön** | ~120 ms | **~28-35 ms** | ~26-32 ms | ~35-45 ms |
| **A dolgozat választása** | Fejlesztésre | **Végponti telepítésre (Edge)** | Alternatív benchmark | - |
"""

print("[OK] Part 2 module written successfully.")
