# -*- coding: utf-8 -*-
"""
Part 2 of the Thesis Research & Implementation Plan
Contains:
- 4. Domain-specifikus szórakozóhelyi kihívások és kutatási válaszok
- 5. Rendszerarchitektúra és feldolgozási folyamat (End-to-End Pipeline)
- 6. Adathalmazok és adatgyűjtési stratégia
"""

PART2_MD = r"""## 4. Domain-specifikus szórakozóhelyi kihívások és kutatási válaszok

A szórakozóhelyi környezet az egyik legbonyolultabb operatív terület a számítógépes látás számára. A hagyományos felügyeleti környezetekhez (pl. üres irodafolyosók, utcai forgalomfigyelés) képest itt a környezeti és emberi változók szélsőséges értékeket vesznek fel. A kutatási terv az alábbi négy kritikus kihívást és a rájuk adott mérnöki-tudományos válaszokat specifikálja:

### 4.1 Tánc vs. Verekedés mint "Hard Negative" anomália
A szakirodalomban elérhető erőszakdetektorok leggyakoribb hibája a dinamikus tánc (breakdance, hip-hop, pogózás, ugrálás) téves riasztásként (False Positive) történő megjelölése. Ennek oka, hogy mind a tánc, mind a verekedés során:
* A végtagok sebessége és gyorsulása meghaladja a normál séta vagy állás értékeit.
* A testek szoros közelségbe kerülnek egymáshoz.
* A gesztusok kiterjedése nagy teret fog át.

#### Kinematikai és dinamikai különbségek
A kutatásunk hipotézise (H2), hogy a tánc és az erőszak mélyebb kinematikai tulajdonságaiban fundamentálisan különbözik:

| Kinematikai paraméter | Ritmikus tánc viselkedés | Valós agresszió / Verekedés | ST-GCN diszkriminációs mechanizmus |
| :--- | :--- | :--- | :--- |
| **Időbeli periodicitás (Fourier-spektrum)** | Erős periodikus harmonikus komponensek a zene ütemére (BPM szinkronizáció). | Aperiodikus, sztochasztikus, kaotikus impulzusok sorozata. | Az időbeli konvolúció (TCN) rétegek képesek felismerni az ismétlődő fázisokat. |
| **Térbeli szimmetria** | Jellemzően bilaterális szimmetria vagy szabályos testkoordináció (pl. mindkét kar vagy láb összehangolt ritmusa). | Aszimmetrikus kitérések: hirtelen védekező blokkolás, egyoldali ütések, egyensúlyvesztés. | A térbeli gráfkonvolúció szomszédsági mátrixa és a csont-vektorok aszimmetriája. |
| **Sebességprofil és rántás (Jerk)** | Folyamatos, sima ívű trajektóriák még gyors mozgásnál is (korlátos rántás). | Diszkontinuus, ütközéses sebességváltozások (hatalmas rántás a fizikai becsapódáskor). | A szomszédos képkockák közötti koordináta-különbségek ($\Delta x, \Delta y$) eloszlása. |
| **Résztvevők közötti korreláció** | Táncpartnereknél a mozgás gyakran komplementer vagy párhuzamosan tükrözött. | Az áldozat és a támadó mozgása antagonisztikus: az egyik előre tör, a másik hátrál vagy összeesik. | Kétszemélyes interakciós gráfok csatolása (Inter-person graph edges). |

A megoldási stratégia: A tanító adatbázisba szándékosan nagyszámú, energikus táncvideót illesztünk "kemény negatív" (Hard Negative) példaként, és az időablak hosszát minimum $T=48$ képkockára választjuk, hogy a periodikus ritmus kirajzolódhasson.

### 4.2 Sűrű tömeg és súlyos takarás (Occlusion Handling)
A szórakozóhelyeken az emberek rendkívül szorosan állnak vagy mozognak egymás mellett. Ennek következtében a kamera látószögéből a testrészek jelentős része (különösen a lábak és az alsótest) gyakran takarásba kerül.

#### Mérnöki megoldások:
1. **Láthatósági konfidencia integrálása a gráfba:**  
   A YOLOv8-Pose minden kulcsponthoz visszaad egy $conf_i \in [0, 1]$ értéket. Ahelyett, hogy csak a 2D koordinátákat táplálnánk be, a gráfcsúcs jellemzővektora háromdimenziós:
   $$v_{ti} = (x_{ti}, y_{ti}, conf_{ti})$$
   Ha egy ízület takarásban van ($conf_{ti} < 0.25$), a hálózat nem hamis koordinátaként, hanem alacsony súlyú információként kezeli.
2. **Időbeli lineáris és spline interpoláció:**  
   Rövid idejű takarások esetén (1-5 képkocka), ha az ízület eltűnik, de előtte és utána ismert a pozíciója, a rendszer lokális időbeli spline interpolációval kitölti a hiányzó koordinátákat.
3. **Felsőtest-prioritásos súlyozás:**  
   Mivel a lökdösődés és az ütések 90%-a a kéz, kar és törzs mozgásában jelenik meg, az osztályozó modell térbeli pooling rétegeiben nagyobb súlyt rendelünk a felsőtest ízületeihez (vállak, könyökök, csuklók, nyak/fej).

### 4.3 Extrém és dinamikus fényviszonyok (Stroboszkóp, félhomály)
A diszkókban és klubokban a fényviszonyok másodpercenként többször változnak:
* Félhomály és sötét zónák a tánctéren.
* Pulzáló, villogó stroboszkópeffektek (10-20 Hz frekvenciával).
* Erős színezett reflektorok (monokróm vörös, kék, zöld megvilágítás).

#### Miért elengedhetetlen a váz-alapú absztrakció?
Az RGB-alapú optikai áramlás (Optical Flow) algoritmusok a fényintenzitás állandóságának elvén (Brightness Constancy Assumption) alapulnak:
$$I(x, y, t) \approx I(x + \Delta x, y + \Delta y, t + \Delta t)$$
Amikor a stroboszkóp felvillan, a képpontok intenzitása pillanatszerűen 10-ről 255-re ugrik. Az optikai áramlás ezt hatalmas virtuális mozgásként érzékeli, ami katasztrofális téves riasztáshoz vezet.
Ezzel szemben a YOLOv8-Pose konvolúciós jellemzőtérképei a kontúrokra és strukturális gradientekre fókuszálnak. Miután a 17 kulcspont kinyerésre került, az ST-GCN kizárólag a normalizált $(x, y)$ koordinátákat látja. A modell számára a képkocka színe, fényereje teljesen láthatatlan, így a stroboszkóp jelenléte zéró közvetlen hatással van az ST-GCN osztályozási logikájára.

### 4.4 Nem standard kameraszögek és perspektivikus torzítás
A biztonsági kamerákat a szórakozóhelyeken szinte kivétel nélkül magasan (3-5 méter magasságban), a falak sarkára vagy a mennyezetre szerelik, és ferdén lefelé néznek (High-angle oblique view).
* **A ferde szög hatása:** A függőleges testméretek megrövidülnek (foreshortening), az emberi váz arányai torzulnak a képsíkon a talajhoz képest.
* **Perspektíva-invariáns normalizálás:**  
  A kutatás során kidolgozunk egy relatív koordináta-transzformációt. Minden detektált személynél az origót a két csípőpont felezőpontjába helyezzük át:
  $$x'_{ti} = \frac{x_{ti} - x_{hip\_center, t}}{S_t}, \quad y'_{ti} = \frac{y_{ti} - y_{hip\_center, t}}{S_t}$$
  Ahol a skálázási tényező $S_t$ a törzshossz (nyak/vállközép és csípőközép euklideszi távolsága). Ezáltal a modell a kamerától való távolságtól és a kamera magasságából adódó méretkülönbségektől függetlenül, egységnyi koordinátatérben látja a testeket.

---

## 5. Rendszerarchitektúra és feldolgozási folyamat (End-to-End Pipeline)

### 5.1 Rendszerkomponensek és folyamatábra
A tervezett biztonsági rendszer egy szigorúan moduláris, aszinkron adatfolyam-architektúrára épül. A folyamat lépéseit a következő Mermaid folyamatábra szemlélteti:

```mermaid
flowchart TD
    A["Bemeneti Videó / RTSP Kamera Stream"] --> B["Képkocka Puffer és Előfeldolgozás (OpenCV Thread)"]
    B --> C["YOLOv8-Pose Inferencia (2D Kulcspont Kinyerés)"]
    C --> D["Többszemélyes Követő (ByteTrack MOT Engine)"]
    D --> E["Személyenkénti Trajektória Puffer (Sliding Window: T=48)"]
    E --> F["Térbeli Normalizálás és Csont-vektor Generálás"]
    F --> G["Tenzorkonstrukció: (B, C, T, V, M)"]
    G --> H["ST-GCN Osztályozó Modell (PyTorch GPU Engine)"]
    H --> I["Kimeneti Valószínűségi Vektorok (Softmax)"]
    I --> J["Időbeli Simítás és Hiszterézis Szűrő (Temporal Smoothing)"]
    J --> K{"Agresszió Küszöbérték Meghaladva?"}
    K -- "Igen (Feszültség / Verekedés)" --> L["Riasztás Generálás és Operátori UI Dashboard"]
    K -- "Nem (Normál / Tánc)" --> M["Puffer Frissítés és Következő Képkocka"]
```

#### A modulok részletes funkciói:
1. **Videó Beolvasó és Képkocka Pufferelő Modul (Frame Grabber):**  
   Dedikált szálon (Thread) olvassa az IP kamera RTSP streamjét vagy a tesztvideókat. Feladata a dekódolási késleltetés kiküszöbölése és a legfrissebb képkocka átadása a feldolgozónak.
2. **Pózbecslő Motor (YOLOv8-Pose):**  
   Batch mérettel futtatja a képeket, és visszaadja az összes detektált ember 17 kulcspontját és bounding boxát.
3. **Követési Motor (ByteTrack Tracker):**  
   Minden észlelt személyhez stabil globális azonosítót (`track_id`) rendel a képkockák között, feloldva az átmeneti takarásokat.
4. **Normalizáló és Időablak Képző Modul:**  
   Személyenként egy $T$ hosszúságú körkörös puffert (Circular Buffer) tart fenn. Elvégzi a koordináta-transzlációt és skálázást.
5. **Osztályozó Motor (ST-GCN Deep Neural Network):**  
   Lefuttatja a gráfkonvolúciós hálózatot, és megadja a cselekvési osztályok valószínűségeit.
6. **Döntési és Hiszterézis Modul (Alert Logic):**  
   Kiküszöböli a pillanatnyi ingadozásokat (False Alarms) időbeli simítással, és szükség esetén riasztási eseményt küld az operátori felületre.

### 5.2 Bemeneti tenzorkonstrukció
Az ST-GCN modell egy standard 5-dimenziós tenzort fogad bemenetként:
$$\mathcal{X} \in \mathbb{R}^{B \times C \times T \times V \times M}$$
Ahol:
* $B$ = Batch méret (egy lépésben feldolgozott minták száma, inferenciánál jellemzően 1).
* $C$ = Csatornák száma. Alapesetben $C=3$ ($x$ koordináta, $y$ koordináta, $conf$ konfidencia). Kétáramú hálózatnál a csont-ágnál $C=3$ ($\Delta x, \Delta y, length$).
* $T$ = Időbeli képkockák száma az ablakban. Kísérleteinkben $T \in \{32, 48, 64\}$ értékeket tesztelünk. 30 FPS rögzítés mellett a $T=48$ ablak 1.6 másodperc valós időnek felel meg, ami optimális kompromisszum a gyors reakcióidő és a stabil mozgásminta-felismerés között.
* $V$ = Ízületi csúcsok száma a gráfban ($V=17$ a COCO topológia szerint).
* $M$ = Egyidejűleg elemzett személyek maximális száma az interakcióban ($M=2$ a közvetlen konfrontációhoz, de kiterjeszthető $M=4$-re csoportos konfliktusoknál). Ha csak egy személy van jelen, a második személy tenzorszelete nullákkal van kitöltve (Zero-padding).

### 5.3 Normalizálási transzformációk algoritmusa
A nyers pixelkoordináták közvetlen használata súlyos torzításokhoz vezetne (a kamera közelében álló személy koordinátái nagyságrendekkel nagyobbak lennének, mint a háttérben lévőké). A feldolgozási láncban az alábbi standardizálási algoritmust valósítjuk meg:

```python
def normalize_skeleton_window(joint_data):
    \"\"\"
    joint_data shape: (T, V, 3) -> [time, joints, (x, y, conf)]
    \"\"\"
    # 1. Csípő középpont meghatározása (bal csípő: index 11, jobb csípő: index 12)
    hip_center = (joint_data[:, 11, :2] + joint_data[:, 12, :2]) / 2.0  # shape: (T, 2)
    
    # 2. Váll középpont meghatározása (bal váll: index 5, jobb váll: index 6)
    shoulder_center = (joint_data[:, 5, :2] + joint_data[:, 6, :2]) / 2.0  # shape: (T, 2)
    
    # 3. Törzshossz mint skálázási tényező (euklideszi távolság)
    torso_length = np.linalg.norm(shoulder_center - hip_center, axis=-1, keepdims=True)  # shape: (T, 1)
    # Ha a törzshossz extrém kicsi (takarás), átlagos értékre állítjuk
    torso_length = np.where(torso_length < 1e-4, np.mean(torso_length) + 1e-4, torso_length)
    
    normalized_joints = np.zeros_like(joint_data)
    # 4. Transzláció a csípőközéppontba és skálázás a törzshosszal
    for t in range(joint_data.shape[0]):
        normalized_joints[t, :, :2] = (joint_data[t, :, :2] - hip_center[t]) / torso_length[t]
        normalized_joints[t, :, 2] = joint_data[t, :, 2]  # Konfidencia változatlan marad
        
    return normalized_joints
```

### 5.4 Döntési logika, hiszterézis és False Positive elnyomás
A neurális hálózat kimenetén kapott képkockánkénti predikciók zajosak lehetnek (pl. egy hirtelen fejrántás egyetlen képkockára magas erőszak-valószínűséget adhat). Ahhoz, hogy elkerüljük a biztonsági szolgálatot feleslegesen terhelő téves riasztásokat, **kétlépcsős hiszterézis- és simítási algoritmust** alkalmazunk:

1. **Mozgóablakos Valószínűség-simítás (Temporal Exponential Moving Average):**
   $$P_{smooth}(t) = \alpha \cdot P(t) + (1 - \alpha) \cdot P_{smooth}(t-1)$$
   Ahol $\alpha \in [0.2, 0.4]$ a simítási tényező.
2. **Kétküszöbös Hiszterézis (Dual-Threshold Hysteresis):**
   * **Aktiválási küszöb ($\theta_{high} = 0.75$):** A riasztás csak akkor kapcsol be, ha a simított valószínűség átlépi a magas küszöböt, és ott marad legalább $N_{consec} = 8$ egymást követő képkockán keresztül (~0.25 másodperc).
   * **Deaktiválási küszöb ($\theta_{low} = 0.40$):** A riasztás mindaddig aktív marad, amíg a valószínűség tartósan a legalacsonyabb küszöb alá nem esik.
3. **Kategória-prioritás:**
   Ha a "Lökdösődés" (Pre-violence) osztály detektálódik, a rendszer "Sárga figyelmeztetés" (Warning) állapotba lép, felhangosítja az operátori nézetet, és fókuszba helyezi az adott kamerát. Ha az "Akut verekedés" osztály aktiválódik, "Vörös riasztás" (Critical Alert) generálódik hangjelzéssel.

---

## 6. Adathalmazok és adatgyűjtési stratégia

### 6.1 Nyilvános referencia adathalmazok elemzése
A váz-alapú agressziófelismerés betanításához és objektív benchmarkingjához a kutatás során nemzetközileg elismert, nyilvános felügyeleti videó-adatbázisokat használunk:

| Adathalmaz neve | Videók száma | Forrás típusa | Megfigyelési perspektíva | Annotáció típusa | Alkalmazás a szakdolgozatban |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RWF-2000** (Cheng et al., 2020) | 2000 klip (5 mp/klip, 30 FPS) | Valós biztonsági kamerák (CCTV) | Változatos utcai és beltéri fix kamerák | Bináris címkék: 1000 Harc / 1000 Nem harc | **Fő tanító és validációs bázis.** A YOLOv8-Pose-zal kinyerjük a 17 kulcspontot, és ebből képezzük a vázadatbázist. |
| **CCTV-Fights** (Perez et al., 2019) | 1000 videó (összesen 8 óra) | Valós megfigyelő kamerák és mobilfelvételek | Valós utcai és zárt téri helyzetek | **Időbeli keret-szintű annotáció** (pontos kezdő- és végpontok) | **Pre-eszkaláció és reakcióidő mérése.** Kiválóan alkalmas az RQ4 vizsgálatára. |
| **UCF-Crime** (Sultani et al., 2018) | 1900 hosszú videó | CCTV megfigyelő kamerák | Magasan elhelyezett ipari kamerák | 13 anomália kategória (közte Fight és Assault) | Kiegészítő tesztkészlet a túlzsúfolt helyszínek és rossz minőségű képek tesztelésére. |
| **NTU RGB+D 120** (Liu et al., 2020) | 114 480 akcióvideó | Laboratóriumi Kinect rögzítés | 3 kameraállás, 32 előadó | 120 osztály (köztük lökdösődés, ütés, rúgás) | Referencia a tiszta vázkinyeréshez és a csont-gráf topológia optimalizálásához. |

### 6.2 Szórakozóhely-specifikus saját kísérleti adathalmaz (Staged Nightclub Dataset)
Mivel a nemzetközi adatbázisok szinte kizárólag utcai vagy nappali felvételeket tartalmaznak, a szórakozóhelyi sajátosságok méréséhez elengedhetetlen egy kontrollált saját adathalmaz létrehozása.

#### A kísérleti adatgyűjtés forgatókönyvei:
A felvételeket 6 önkéntes résztvevő bevonásával, különböző szcenáriók szerint rögzítjük:
1. **Szcenárió A - Normál klubélet (30 videó):** Beszélgetés, sétálás a teremben, italrendelés a pultnál, koccintás.
2. **Szcenárió B - Intenzív tánc és szórakozás (40 videó - Hard Negatives):** Gyors ritmusú tánc, fej- és karmozgás, ugrálás, pogózás szimulálása, baráti átkarolás.
3. **Szcenárió C - Feszült helyzet és lökdösődés (35 videó - Pre-escalation):** Két fél hevesen gesztikulálva vitázik, egymáshoz hajolnak, az egyik meglöki a másikat, visszalökés, szétválasztási kísérlet.
4. **Szcenárió D - Nyílt agresszió és verekedés (35 videó):** Ütés indítása, birkózás, földre vitel, többszemélyes összekapaszkodás.

#### Környezeti paraméterek szimulációja:
* **Megvilágítás:** Szabályozható stúdióreflektorok, színes RGB LED panelek, valamint stroboszkópeffektus (12 Hz villogás) alkalmazása.
* **Kameraállás:** Egy magas állványra (3.2 méter magasságban) rögzített széles látószögű kamera (45 fokos döntésszöggel), szimulálva a fali rögzítést.

#### Etikai és GDPR protokoll:
Minden felvétel kizárólag a résztvevők előzetes, írásos tájékoztatáson alapuló beleegyezésével készül. A videók személyes adatnak minősülnek, ezért jelszóval védett, titkosított meghajtón tároljuk őket. Miután a YOLOv8-Pose kinyerte a koordinátákat, a végső publikus kutatási csomagba kizárólag az anonimizált `.npy` formátumú vázadatok kerülnek be.

### 6.3 Adatbővítési (Data Augmentation) eljárások váz-gráfokon
A mély tanuló modellek hajlamosak a túlilleszkedésre, ha a vázadatok túl specifikus pozíciókból származnak. Mivel a képi transzformációk (pl. színátmenet, blur) a vázadatokon nem értelmezhetők, speciális **geometriai és időbeli gráf-augmentációs pipeline-t** valósítunk meg:

1. **Véletlenszerű térbeli rotáció (Spatial 2D Rotation):**  
   A vázat a súlypontja körül elforgatjuk egy véletlen $\theta \in [-15^{\circ}, +15^{\circ}]$ szöggel, szimulálva a ferde kameraállásokat:
   $$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}$$
2. **Horizontális tükrözés (Horizontal Flip):**  
   A vízszintes tengely mentén tükrözzük a koordinátákat ($x' = -x$). **Kritikus lépés:** az anatómiai konzisztencia megőrzése érdekében az ízületi indexeket fel kell cserélni (pl. bal váll $\leftrightarrow$ jobb váll, bal csukló $\leftrightarrow$ jobb csukló).
3. **Időbeli skálázás és mintavételezés (Temporal Resampling):**  
   A mozgás sebességének variálására az időablakot interpolációval összenyomjuk vagy megnyújtjuk $\pm 20\%$-kal (gyorsabb vagy lassabb ütések, mozdulatok szimulálása).
4. **Ízületi Gauss-zaj (Joint Coordinate Jittering):**  
   Kis mértékű fehérzajt adunk az ízületekhez: $x' = x + \epsilon$, ahol $\epsilon \sim \mathcal{N}(0, \sigma^2)$ ($\sigma = 0.01$). Ez felkészíti az ST-GCN-t a pózbecslő mérési hibáira.
5. **Kulcspont-kiesés szimulációja (Keypoint Dropout):**  
   Véletlenszerűen kiválasztunk 1-3 ízületet az ablakban, és koordinátáikat nullára, konfidenciájukat alacsony értékre állítjuk. Ez kényszeríti a modellt arra, hogy részleges takarás esetén is a megmaradt ízületekből vonjon le következtetést.
"""

print("Part 2 defined successfully.")
