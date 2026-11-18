# -*- coding: utf-8 -*-
"""
Part 1 of the Thesis Research & Implementation Plan
Contains:
- Title Page & Metadata
- Executive Summary & Abstract (HU & EN)
- 1. Bevezetés és kutatási háttér
- 2. Kutatási célok, kérdések és hipotézisek
- 3. Szakirodalmi áttekintés és elméleti háttér
"""

PART1_MD = r"""# Szakdolgozati Kutatási és Rendszer-megvalósítási Terv

**Intézmény:** Számítástechnikai és Információs Rendszerek Tanszék  
**Képzés:** Mérnökinformatikus / Programtervező Informatikus BSc  
**Dokumentum típusa:** Szakdolgozati Részletes Kutatási és Megvalósítási Terv (Research & Implementation Plan)  
**Téma címe:** Verekedés- és agresszió-megelőzés szórakozóhelyi környezetben váz-alapú viselkedéselemzéssel (YOLOv8-Pose, ST-GCN, PyTorch)  
**Angol cím:** Nightclub Violence Detection and Prevention via Skeleton-Based Human Action Recognition  
**Dátum:** 2026/2027. tanév  
**Kulcsszavak:** Számítógépes látás, Pózelőrejelzés, YOLOv8-Pose, ST-GCN, Tér-időbeli gráfkonvolúció, Viselkedéselemzés, Agresszió-detekció, Többszemélyes követés, Valós idejű rendszerek, Adatvédelem (GDPR).

---

## Vezetői összefoglaló és absztrakt

### Magyar nyelvű absztrakt
A szórakozóhelyek és éjszakai szórakoztató létesítmények kritikus biztonsági kihívása a fizikai agresszió, a verekedések és a rendbontások időben történő felismerése és megelőzése. A hagyományos, emberi operátorokra támaszkodó videomegfigyelő rendszerek hatékonyságát erősen korlátozza a vizuális fáradtság, a nagyszámú egyidejű kamerakép és a szórakozóhelyi terek sajátos jellege (szélsőséges fényviszonyok, stroboszkópeffektek, sűrű tömeg, takarások). Továbbá az érvényben lévő európai adatvédelmi szabályozás (GDPR) szigorú korlátokat szab a személyes adatok, különösen az arcvonások folyamatos rögzítésének és tárolásának.

Jelen szakdolgozati kutatási terv egy olyan valós idejű, váz-alapú (skeleton-based) számítógépes látórendszer kutatását, megtervezését és prototípusának kifejlesztését célozza, amely kizárólag az emberi test ízületi pontjainak 2D tér-időbeli dinamikáját elemzi. A feldolgozási lánc a legmodernebb egyfokozatú pózbecslő modellt (YOLOv8-Pose) kombinálja megbízható többszemélyes követéssel (ByteTrack / BoT-SORT), valamint Tér-Időbeli Gráfkonvolúciós Hálózattal (ST-GCN - Spatial Temporal Graph Convolutional Network). A kutatás kiemelt fókusza a szórakozóhelyi környezetből adódó egyedi anomáliák kezelése: különösen a ritmikus, heves táncmozdulatok ("hard negative" minták) elkülönítése a valós agressziótól, valamint a korai konfliktusfázisok (lökdösődés, fenyegető gesztusok) azonosítása az eszkaláció megelőzése érdekében. A tervezett rendszer szigorúan tiszteletben tartja a "Privacy by Design" alapelvet, mivel az RGB képkockák eldobása után kizárólag topológiai koordináta-sorozatokkal dolgozik, és döntéstámogató riasztásokkal segíti a biztonsági személyzet munkáját.

### English Abstract
A primary safety challenge in nightlife venues, clubs, and entertainment facilities is the timely detection and de-escalation of physical violence, brawls, and aggressive behavior. Traditional video surveillance relying on human operators suffers from cognitive fatigue, camera blind spots, and the complex domain characteristics of nightclubs (extreme low light, flashing strobes, dense crowd occlusion). Furthermore, stringent data privacy regulations (GDPR) impose severe constraints on continuous video recording and face biometric processing.

This thesis research and implementation plan presents the end-to-end design, investigation, and software implementation of a real-time, privacy-preserving, skeleton-based action recognition system. By extracting 2D topological body keypoints via state-of-the-art YOLOv8-Pose and maintaining temporal identity trajectories using ByteTrack / BoT-SORT, the system feeds spatiotemporal joint graphs into a Spatial Temporal Graph Convolutional Network (ST-GCN). The research specifically tackles domain-specific night club anomalies: distinguishing high-energy dancing movements (hard negative samples) from genuine violence, and identifying pre-escalation friction (shoving, pushing, aggressive posturing) before severe physical trauma occurs. Built upon a "Privacy-by-Design" architecture that discards raw pixel streams in favor of abstract skeletal coordinates, the resulting solution delivers high-throughput, low-latency actionable alerts to security personnel.

---

## 1. Bevezetés és a kutatás háttere

### 1.1 A biztonsági felügyelet gyakorlati kihívásai éjszakai szórakozóhelyeken
Az éjszakai szórakozóhelyek, táncklubok és zárt rendezvények biztonsági irányítása komplex, többváltozós feladat. A zárt terekben egyszerre több száz vagy több ezer ember tartózkodik, akiknek a viselkedése az alkohol- és egyéb szerfogyasztás, a magas decibelszintű zene és a szociális interakciók intenzitása miatt gyorsan és kiszámíthatatlanul eszkalálódhat. A statisztikák alapján a szórakozóhelyeken bekövetkező súlyos testi sértések döntő többsége nem azonnali, előzmény nélküli erőszakkal kezdődik, hanem jól körülhatárolható verbális és pre-fizikai fázisokon megy keresztül:
1. **Feszültségkeltési szakasz:** A felek közötti testközelség drasztikusan lecsökken, heves és aszimmetrikus gesztikuláció, fenyegető testtartás jelenik meg.
2. **Pre-agresszív fizikai kontaktus:** Első kontaktusok, mint mellkasnak feszülés, taszítás, megragadás, lökdösődés.
3. **Akut agresszió és verekedés:** Ütések, rúgások, földre vitel, fegyverhasználat (pl. pohártörés), tömeges összecsapás.

A szórakozóhelyeken működő biztonsági személyzet (rendészek, "kidobók") és a kameraszobában ülő operátorok munkáját alapvetően determinálják a humán kognitív korlátok:
* **Figyelem-fáradás (Vigilance decrement):** Számítógépes látási és ergonómiai tanulmányok igazolják, hogy egy megfigyelő 20 percnyi intenzív videomonitorozás után a kritikus események közel 45%-át nem veszi észre, 40 perc elteltével pedig a hibázási arány meghaladja a 75%-ot.
* **Többkamerás holtterek és figyelem-megosztás:** Egy közepes méretű klubban 16-64 biztonsági kamera képe fut be egyidejűleg. Egy emberi operátor képtelen 30-40 képkocka/másodperces dinamikával folyamatosan követni az összes helyiséget (tánctér, pultok előtere, folyosók, dohányzók).
* **Késedelmes beavatkozás:** Mire az emberi szem észleli a verekedést, a fizikai sérülések gyakran már bekövetkeztek, és a konfliktusba további felek avatkoztak be, megsokszorozva a beavatkozás kockázatát.

A probléma feloldásának egyetlen reális, skálázható módja az automatizált, gépi intelligenciával támogatott valós idejű viselkedéselemzés.

### 1.2 Az RGB-alapú és a váz-alapú megközelítés paradigmaváltása
Az automatikus erőszakfelismerés (Violence Detection) kezdeti korszaka szinte kizárólag nyers RGB videófolyamokra és optikai áramlásra (Optical Flow) épült. A 3D Konvolúciós Hálózatok (C3D, I3D, SlowFast) és a modern videótranszformerek (TimeSformer, Video Swin) kiváló pontosságot értek el laboratóriumi referencia-adatbázisokon. Ugyanakkor éles szórakozóhelyi környezetben az RGB-alapú rendszerek három kritikus akadályba ütköznek:

| Szempont | RGB-alapú megközelítés (3D CNN / Video Transformer) | Váz-alapú megközelítés (YOLO-Pose + ST-GCN) | Szórakozóhelyi következmény |
| :--- | :--- | :--- | :--- |
| **Számítási igény (Compute & Latency)** | Hatalmas lebegőpontos műveletigény (GFLOPs); több stream valós idejű futtatása drága adatközponti GPU-kat (pl. A100/H100) igényel. | Kétfokozatú, de rendkívül gyors: a 2D pózbecslés könnyűsúlyú, a gráfkonvolúció pedig mindössze 17 pont koordinátáit számolja (~1-2 GFLOPs). | Olcsó, lokális GPU-kon (pl. RTX 3060/4060 vagy Jetson) is képes több kamerát valós időben (30+ FPS) kiszolgálni. |
| **Környezeti robusztusság (Illumination invariance)** | Erősen függ a színektől, textúráktól és fényintenzitástól. Szórakozóhelyen a stroboszkóp, a sötétség és a színezett reflektorok tévesen aktiválják az optikai áramlást. | **Környezet-invariáns:** Az ízületi koordináták normalizáltak; a hálózatot nem zavarja a fény színe, a ruha mintázata vagy a háttér vibrálása. | Megbízható működés a tánctér pulzáló fényviszonyai között is. |
| **Adatvédelem és GDPR megfelelés** | A nyers videófolyamok arcokat, személyes azonosítókat tartalmaznak, amelyek rögzítése és elemzése szigorú engedélyhez kötött és jogi kockázatot hordoz. | **Privacy-by-Design:** Az RGB képkockák azonnal eldobásra kerülnek a kulcspontok kinyerése után; a rendszer kizárólag anonim topológiai koordinátákat tárol. | Teljes GDPR kompatibilitás; a vázadat nem alkalmas személyazonosításra. |
| **Túlilleszkedés (Overfitting)** | A modellek hajlamosak a háttérre asszociálni (pl. egy sötét sikátor hátterét automatikusan veszélyesnek ítélik). | A modell kizárólag a mozgás kinematikáját és a testek egymáshoz viszonyított interakcióját vizsgálja. | Kiváló általánosítás különböző helyszínek és berendezések között. |

### 1.3 A korai agresszió-detekció és megelőzés koncepciója
A szakirodalomban elérhető erőszakfelismerő modellek jelentős része bináris osztályozást végez: a jelenetet "Fight" vagy "Non-Fight" kategóriába sorolja. A gyakorlati biztonságvédelem szempontjából azonban a már javában zajló verekedés detektálása csupán kármentés, nem pedig megelőzés.

Jelen kutatás központi gondolata, hogy a felismerési időablakot előre kell tolni a **pre-eszkalációs fázisba**. Ha a rendszer képes megbízhatóan felismerni a lökdösődést (shoving), a heves rángatást és a fenyegető konfrontációt, a biztonsági szolgálat még azelőtt beavatkozhat a helyszínen, hogy súlyos testi sértés vagy tömegverekedés alakulna ki. Ehhez olyan többosztályos (Multi-class) architektúra és finomhangolt időablak-kezelés szükséges, amely képes elkülöníteni a hétköznapi interakciókat a feszült helyzetektől.

### 1.4 A kutatás határai és terjedelme (Scoping)
Annak érdekében, hogy a szakdolgozat a BSc keretek között szigorúan kivitelezhető, tudományosan megalapozott és határidőre befejezhető legyen, rögzítjük a kutatás határait:
* **A kutatás részét képezi:**
  1. Nyilvános videó-adathalmazok (RWF-2000, CCTV-Fights) feldolgozása, és azokból kulcspont-alapú mozgásadatbázis felépítése.
  2. Saját, szórakozóhelyi sajátosságokat szimuláló (tánc, lökdösődés, verekedés, tömeg) kontrollált tesztvideók készítése és annotálása.
  3. YOLOv8-Pose és többszemélyes követő (ByteTrack) pipeline-ba illesztése és konfigurálása.
  4. Összehasonlító alapszintű baseline modell (kinematikai ízületi szögek + Random Forest / XGBoost) megvalósítása.
  5. Tér-időbeli Gráfkonvolúciós Hálózat (ST-GCN) betanítása, hiperparaméter-optimalizálása és kiértékelése.
  6. Szórakozóhely-specifikus stressztesztek (tánc vs. verekedés hibaelemzés, stroboszkóphatás mérése, takarások kezelése).
  7. Egy valós idejű, kameraképet vagy videót fogadó demó prototípus implementálása operátori riasztási felülettel.
* **Tudatosan kizárva a hatókörből:**
  1. Arcfelismerés, biometrikus azonosítás és rendszámfelismerés (adatvédelmi okokból).
  2. Hanganalízis és mikrofon-alapú sikoly-/zajdetekció (a szórakozóhelyeken a zene decibelszintje miatt a hangcsatorna túltelített és használhatatlan).
  3. Saját, nulláról tanított 2D pózbecslő gerinchálózat fejlesztése (helyette az ipari standard Ultralytics YOLOv8-Pose előtanított súlyait használjuk transzfer tanulással).
  4. Éles, több hónapos ipari telepítés valós szórakozóhelyen (jogi, felelősségbiztosítási és GDPR korlátok miatt laboratóriumi és szimulált tesztekre korlátozódik).

---

## 2. Kutatási célkitűzések, kérdések és hipotézisek

### 2.1 Kutatási célkitűzések
A szakdolgozati projekt hármas célt tűz ki:
1. **Tudományos cél:** Feltárni a váz-alapú gráfkonvolúciós hálózatok diszkriminatív képességét kaotikus szórakozóhelyi mozgásformák között, különös tekintettel a dinamikus tánc és az erőszak szétválasztására.
2. **Mérnöki cél:** Olyan end-to-end adatfeldolgozási és követési láncot felépíteni, amely képes több személy egyidejű, valós idejű (>25 FPS) követésére és akcióosztályozására megfizethető hardvereszközökön.
3. **Alkalmazott biztonsági cél:** Kidolgozni egy olyan korai figyelmeztető mechanizmust, amely csökkenti a téves riasztások számát (False Positive Suppression) és minimalizálja az érzékelési időkésést.

### 2.2 Kutatási kérdések (Research Questions)
A kutatás során az alábbi konkrét kérdésekre keresünk számszerűsíthető válaszokat:

* **RQ1: Megbízhatóság és diszkrimináció a tánc tükrében:**  
  *Kérdés:* Milyen pontossággal (Accuracy, F1-score) és mekkora téves riasztási arány (False Positive Rate) mellett képes az ST-GCN modell megkülönböztetni a ritmikus, intenzív táncmozdulatokat a valós agressziótól és lökdösődéstől?  
  *Mérési mód:* Konfúziós mátrix analízise kifejezetten táncjeleneteket tartalmazó negatív teszthalmazon.

* **RQ2: Gráfkonvolúció vs. Hagyományos Gépi Tanulási Baseline:**  
  *Kérdés:* Mekkora statisztikailag szignifikáns teljesítménytöbbletet (F1-score és ROC-AUC) biztosít a topológiai tér-időbeli összefüggéseket modellező ST-GCN egy mérnökileg előállított, ízületi szögekből és sebességekből építkező klasszikus baseline modellel (pl. Random Forest / XGBoost) szemben?  
  *Mérési mód:* Keresztvalidációs összehasonlító mérések azonos adatbázison.

* **RQ3: Valós idejű feldolgozás és időkésés (Latency):**  
  *Kérdés:* Képes-e a teljes pipeline (YOLOv8-Pose + ByteTrack + Normalizálás + ST-GCN) elérni a valós idejű feldolgozási küszöböt ($\ge 25$ FPS) egyetlen középkategóriás GPU-n (pl. RTX 3060/4060), és mekkora a rendszer teljes end-to-end reakcióideje az agresszív mozdulat megkezdésétől a riasztás megjelenéséig?  
  *Mérési mód:* Profiling, képkockánkénti futásidő-mérés komponensenként lebontva.

* **RQ4: Korai jelzés és a pre-eszkaláció felismerhetősége:**  
  *Kérdés:* Lehetséges-e egy 3-osztályos modellben (Normál / Feszült helyzet-lökdösődés / Verekedés) megbízhatóan szeparálni a lökdösődést, és átlagosan hány másodperccel a súlyos testi erőszak bekövetkezése előtt képes a rendszer korai figyelmeztetést generálni?  
  *Mérési mód:* Időbeli szegmentációs metrikák, "Time-to-Violence" előrejelzési ablak vizsgálata temporálisan annotált videókon.

### 2.3 Kutatási hipotézisek (Hypotheses)
A szakirodalom előzetes tanulmányozása alapján az alábbi hipotéziseket állítjuk fel, amelyeket a kísérleti eredményekkel fogunk igazolni vagy cáfolni:

* **H1 Hipotézis:** Az ST-GCN modell a térbeli szomszédsági mátrixok és időbeli konvolúciók révén legalább **8-12 százalékponttal magasabb F1-értéket** ér el a komplex agresszió-osztályozásban, mint a statikus ízületi szögekre épülő Random Forest baseline modell, mivel az agresszió lényege a pontok relatív dinamikus interakciójában rejlik.
* **H2 Hipotézis:** A táncmozdulatok önmagukban magas mozgási energiát mutatnak, de kinetikai fázisaik periodikusak és szimmetrikusak; ezzel szemben az agresszió aszimmetrikus és hirtelen gyorsulásokkal terhelt. Ezért az időablak $T \ge 48$ képkockára (~1.6 másodperc) történő növelése **legalább 30%-kal csökkenti a táncból eredő téves riasztások arányát** a rövid ($T=16$) ablakokhoz képest.
* **H3 Hipotézis:** A YOLOv8-Pose által generált 17 kulcspontos COCO reprezentáció a láthatósági és konfidencia értékek ($conf_i$) súlyozásával képes fenntartani a felismerési pontosság legalább 80%-át még 20-30%-os részleges testtakarás (occlusion) esetén is.
* **H4 Hipotézis:** A teljes optimalizált követési és osztályozási lánc futási ideje egy modern fogyasztói GPU-n nem haladja meg a **35 ms/frame** értéket, biztosítva a folyamatos, akadásmentes valós idejű felügyeletet.

---

## 3. Szakirodalmi áttekintés és elméleti háttér

### 3.1 Számítógépes látás az erőszakfelismerésben: Az optikai áramlástól a gráfmodellekig
A videó-alapú akciófelismerés (Action Recognition) és ezen belül az erőszakdetekció története jól leképezi a mély tanulás fejlődési szakaszait:

1. **Hagyományos gépi látási korszak (2010-2015):**  
   A korai kutatások kézzel tervezett vizuális jellemzőkre (Handcrafted features) épültek. A legelterjedtebb módszerek a térbeli és időbeli származtatottakat, optikai áramlást (Optical Flow), valamint a Histogram of Oriented Gradients (HOG) és Histogram of Optical Flow (HOF) deskriptorokat alkalmazták Support Vector Machine (SVM) osztályozóval. A szórakozóhelyi környezetben ezek a rendszerek teljesen kudarcot vallottak, mert a villódzó fények drasztikus műtermékeket hoztak létre az optikai áramlási mezőben.

2. **2D CNN + RNN / LSTM korszak (2015-2018):**  
   A konvolúciós hálózatok (VGG, ResNet) képkockánként kinyerték a vizuális reprezentációt, majd egy Long Short-Term Memory (LSTM) vagy Gated Recurrent Unit (GRU) hálózat modellezte az időbeli változást. Bár a pontosság javult, a modellek érzékenyek maradtak a háttér és a ruházat színére.

3. **3D Konvolúciók és Kétáramú Hálózatok (2017-2022):**  
   A C3D, az I3D (Inflated 3D ConvNet) és a SlowFast (Feichtenhofer et al., 2019) architektúrák áttörést hoztak az akciófelismerésben. A SlowFast hálózat például két párhuzamos ágon dolgozik: egy alacsony képkockasebességű ágon a térbeli szemantikáért, és egy nagy képkockasebességű gyors ágon a mozgásdinamikáért. Bár kiváló pontosságot nyújtanak, a számítási kapacitásigényük extrém magas, és az RGB adatok kezelése miatt súlyos adatvédelmi kérdéseket vetnek fel.

4. **Váz-alapú gráfkonvolúciós korszak (2018-napjainkig):**  
   Yan et al. (2018) publikációja (ST-GCN) paradigmaváltást indított el. Rádöbbentette a kutatói közösséget, hogy az emberi cselekvések felismeréséhez a háttér és a pixelek 99%-a felesleges redundancia vagy zaj. Ha az emberi testet ízületek gráfjaként reprezentáljuk, a feladat mérete több nagyságrenddel csökken, miközben a modell robusztussága és általánosító képessége drámaian megnő.

### 3.2 2D Emberi Pózbecslés (Human Pose Estimation): YOLOv8-Pose
Az emberi pózbecslés célja a test anatómiai kulcspontjainak (ízületek, arcvonások) lokalizálása a 2D képsíkon. Két fő megközelítés létezik:
* **Top-down (Fentről-lefelé):** Először egy objektumdetektor megtalálja az embereket (Bounding Box), majd minden egyes kivágott dobozra külön lefut egy pózbecslő modell (pl. HRNet, AlphaPose). Előnye a nagy pontosság, hátránya, hogy futásideje a képen lévő emberek számával lineárisan skálázódik. Sűrű szórakozóhelyi tömegben ez elfogadhatatlan lassulást eredményez.
* **Bottom-up (Lentről-felfelé):** A hálózat egyszerre detektálja az összes kulcspontot a képen, majd gráf-illesztéssel vagy asszociációs mezőkkel (Part Affinity Fields) rendeli őket személyekhez (pl. OpenPose). Bár futásideje független a személyek számától, az asszociációs fázis számításigényes.

#### A YOLOv8-Pose előnyei és architektúrája
A Jocher et al. (Ultralytics, 2023) által bemutatott YOLOv8-Pose az úgynevezett **egymenetes, horgonypont-mentes (anchor-free, single-stage)** architektúrára épül. Nem igényel külön körbevágást, hanem a detekciós fejjel párhuzamosan közvetlenül prediktálja a kulcspontokat.

* **Gerinchálózat (Backbone):** Módosított CSPDarknet53, amely Cross-Stage Partial kapcsolatokkal biztosítja a gazdag többméretű jellemzőkinyerést alacsony számítási overhead mellett.
* **Nyak (Neck):** Path Aggregation Network (PANet), amely egyesíti a felülről-lefelé és alulról-felfelé haladó jellemzőpiramisokat, elősegítve a kisméretű és nagyméretű személyek egyidejű pontos detektálását.
* **Fej (Pose Head):** Szétválasztott (Decoupled) fej-architektúra, amely független konvolúciós ágakon számítja az osztályozási valószínűséget, a befoglaló téglalap koordinátáit, valamint a kulcspontok koordinátáit és láthatósági faktorait:
  $$\hat{K}_i = (x_i, y_i, conf_i), \quad i \in \{1, \dots, 17\}$$

#### Az Object Keypoint Similarity (OKS) Veszteségfüggvény
A pózbecslés tanítása a standard hiba helyett az OKS-re épülő veszteségfüggvénnyel történik. Az OKS az IoU (Intersection over Union) koncepcionális megfelelője kulcspontokra:
$$OKS = \frac{\sum_{i} \exp\left(-\frac{d_i^2}{2 s^2 \sigma_i^2}\right) \delta(v_i > 0)}{\sum_{i} \delta(v_i > 0)}$$
Ahol:
* $d_i$ a becsült és a valós kulcspont közötti euklideszi távolság a képsíkon.
* $s$ a személy skálaparamétere (a befoglaló téglalap területének négyzetgyöke: $s = \sqrt{w \cdot h}$).
* $\sigma_i$ az adott ízülettípusra jellemző szórási konstans (a COCO standard szerint pl. a szemre vagy orra kisebb tolerancia vonatkozik, mint a csípőre vagy vállra).
* $v_i$ a láthatósági jelző ($v_i=0$: nincs annotálva, $v_i=1$: takarásban van, $v_i=2$: tisztán látható).
* $\delta(\cdot)$ a Dirac-delta függvény (csak a létező pontokat veszi figyelembe).

#### A COCO-17 Topológia
A YOLOv8-Pose a standard COCO formátum 17 kulcspontját szolgáltatja:
* **Fej:** 0: Orr, 1: Bal szem, 2: Jobb szem, 3: Bal fül, 4: Jobb fül
* **Felsőtest:** 5: Bal váll, 6: Jobb váll, 7: Bal könyök, 8: Jobb könyök, 9: Bal csukló, 10: Jobb csukló
* **Alsótest:** 11: Bal csípő, 12: Jobb csípő, 13: Bal térd, 14: Jobb térd, 15: Bal boka, 16: Jobb boka

A verekedés és agresszió szempontjából a leginformatívabb pontok a felsőtesthez tartoznak (5-10: vállak, könyökök, csuklók) az ütések és lökések dinamikája miatt, valamint a csípőpontok (11-12) a test súlypontjának mozgása miatt.

### 3.3 Többszemélyes Objektumkövetés (Multi-Object Tracking - MOT)
Egy szórakozóhelyi jelenetben egyszerre sok személy mozog. Ahhoz, hogy egy személy mozgásmintázatát időben elemezni lehessen, a képkockák között folyamatosan fenn kell tartani a személyazonosságot (Tracklet). Erre a legkorszerűbb két követőt vizsgáljuk:

#### ByteTrack
A Zhang et al. (2022) által publikált ByteTrack alapvető innovációja, hogy nem dobja el az alacsony detekciós konfidenciájú dobozokat. A legtöbb követő csak a magas megbízhatóságú detekciókat ($conf > 0.6$) veszi figyelembe, így takarás vagy rossz fény esetén a pálya azonnal megszakad. A ByteTrack kétlépcsős asszociációt használ:
1. Első lépésben a magas konfidenciájú detekciókat rendeli a meglévő pályákhoz Kalman-szűrő és IoU távolság alapján a Magyar algoritmus (Hungarian algorithm) segítségével.
2. A párosítatlanul maradt pályákat megpróbálja hozzárendelni az **alacsony konfidenciájú** ($0.1 < conf < 0.6$) detekciókhoz. Mivel a szórakozóhelyen a takarások és a fényváltozások miatt az emberek detekciója gyakran beesik alacsony értékekre, a ByteTrack drasztikusan csökkenti a pálya-szétesések (ID Switches) számát.

#### BoT-SORT
Az Aharon et al. (2022) által bemutatott BoT-SORT (Boosted Track and Camera Motion Compensation) továbbfejleszti a ByteTrack-et:
* Kamera-mozgás kompenzáció (CMC): Globális mozgásbecslést végez képi jellemzők alapján, így ha a felügyeleti kamera remeg vagy pásztáz, a Kalman-szűrő belső állapota korrigálódik.
* Re-ID (Újra-azonosítási) vektorok integrálása: Mély jellemzővektorokat fűz az IoU távolsághoz, ami segít, ha két személy keresztezi egymás útját és a dobozaik teljesen átfedik egymást.

### 3.4 Tér-Időbeli Gráfkonvolúciós Hálózatok (ST-GCN)
A Yan et al. (2018) által bevezetett ST-GCN az emberi testet egy tér-időbeli irányítatlan gráfként modellezi:
$$G = (V, E)$$
Ahol a csúcsok halmaza $V = \{v_{ti} \mid t = 1, \dots, T; \, i = 1, \dots, N\}$ reprezentálja az összes ízületet az időablakban ($N=17$ ízület, $T$ időbeli lépés).
Az élek halmaza $E$ két részből áll:
1. **Térbeli élek ($E_S$):** Az emberi test anatómiai csontjai, amelyek összekötik a szomszédos ízületeket egy adott $t$ időpillanatban (pl. csukló-könyök, könyök-váll).
2. **Időbeli élek ($E_T$):** Ugyanazon ízületi pont egymást követő képkockák közötti összeköttetései: $(v_{ti}, v_{(t+1)i})$.

#### A Térbeli Gráfkonvolúció Matematikai Formulája
A klasszikus 2D képi konvolúcióban a konvolúciós maszk egy szabályos $3 \times 3$-as rácson operál. Egy tetszőleges gráfcsúcson azonban a szomszédok száma változó, és nincs természetes sorrendjük. A térbeli gráfkonvolúció az alábbi egyenlettel definiálható:
$$f_{out}(v_i) = \sum_{v_j \in B(v_i)} \frac{1}{Z_{ij}} f_{in}(v_j) \cdot W(l_i(v_j))$$
Ahol:
* $B(v_i) = \{v_j \mid d(v_i, v_j) \le 1\}$ a $v_i$ csúcs 1-távolságú szomszédsága (önmagát is beleértve).
* $f_{in}(v_j)$ a bemeneti jellemzővektor (pl. $x, y$ koordináták és $conf$ konfidencia).
* $W$ a tanulható súlymátrix.
* $l_i(v_j)$ a partíciós címkéző függvény, amely a szomszédokat véges számú csoportba osztja.
* $Z_{ij}$ a normalizáló faktor (az adott csoport elemszáma), amely megakadályozza a gradiens felrobbanását.

#### Partíciós Stratégiák
Az ST-GCN-ben a partíciós stratégia határozza meg, hogyan tanul a hálózat:
1. **Uni-label partitioning:** Minden szomszéd azonos súlyt kap ($K=1$). Túl egyszerű, nem tudja megtanulni az irányokat.
2. **Distance partitioning:** Két részre osztja a szomszédokat: maga a gyökércsúcs ($d=0$), és a szomszédos csúcsok ($d=1$).
3. **Spatial Configuration partitioning (Térbeli konfigurációs stratégia):** Három részre osztja a szomszédokat a test globális súlypontjához (Gravity Center) viszonyítva:
   * 1. csoport: Maga a gyökércsúcs.
   * 2. csoport (Centripetális): Azok a szomszédos ízületek, amelyek közelebb vannak a test súlypontjához, mint a gyökérpont.
   * 3. csoport (Centrifugális): Azok a szomszédos ízületek, amelyek távolabb vannak a test súlypontjától.
Ez a stratégia kiválóan modellezi a végtagok kinyúlását és összehúzódását, ami verekedésnél (ütés, rúgás) kulcsfontosságú.

Mátrixos formában a térbeli gráfkonvolúció a szomszédsági mátrix felbontásával valósul meg:
$$f_{out} = \sum_{k=1}^K \Lambda_k^{-\frac{1}{2}} A_k \Lambda_k^{-\frac{1}{2}} f_{in} W_k$$
Ahol $A_k$ a $k$-adik partíciós csoport szomszédsági mátrixa, $\Lambda_k^{ii} = \sum_j A_k^{ij} + \alpha$ pedig a normalizáló diagonális mátrix.

#### Időbeli Konvolúció (Temporal Convolution)
Miután a térbeli gráfkonvolúció minden egyes képkockán integrálta a test anatómiai összefüggéseit, az időbeli dimenzió mentén egy standard 1D konvolúció fut le $K_t \times 1$ méretű maszkkal (jellemzően $K_t = 9$). Ez közvetlenül a csúcsok időbeli trajektóriáját szűri.

#### Kétáramú (Two-Stream) ST-GCN Kiterjesztés
Shi et al. (2019) és Duan et al. (PYSKL, 2022) megmutatták, hogy a csontok (Bone Stream) közvetlen modellezése jelentősen javítja a pontosságot:
* **Ízületi ág (Joint Stream):** Bemenete az ízületek abszolút normalizált koordinátái: $v = (x, y)$.
* **Csont ág (Bone Stream):** Bemenete a két összekapcsolt ízület közötti irányvektor:
  $$e_{u, v} = v - u = (x_v - x_u, y_v - y_u)$$
A csont-vektor közvetlenül hordozza a végtagok hosszát és térbeli orientációját, ami szögelfordulás-invariánssá teszi a modellt. A két ág kimeneti softmax valószinűségeit súlyozottan összegezzük (Late Fusion).
"""

print("Part 1 defined successfully.")
