# -*- coding: utf-8 -*-
"""
Szakdolgozati Beszámoló és Részletes Kutatási Terv (Esésdetektálás + Raspberry Pi Edge AI)
1. RÉSZ (Átdolgozott, 7 javítás beépítve):
- Címlap, Absztrakt
- 1. Fejezet (Bevezetés, Egészségügyi háttér, Edge AI & RPi motiváció, M=1 korlát)
- 2. Fejezet (Célok, RQ1-RQ4, Finomhangolt H1-H4 hipotézisek)
"""

PART1_MD = r"""# Szakdolgozati Részletes Kutatási és Rendszer-megvalósítási Terv

**Hivatalos Témacím:** Gráf alapú modellek alkalmazása vizuális információ feldolgozására, különös tekintettel a viselkedéselemzésre  
**Kutatási fókusz és szakdolgozati alcím:** Beágyazott és peremhálózati (Edge AI) valós idejű esésdetektálás Raspberry Pi mikroszámítógépen emberi pózbecsléssel és tér-időbeli gráfkonvolúciós hálózatokkal (YOLOv8-Pose, ST-GCN, ONNX INT8)  
**Angol cím:** Embedded Edge AI Real-Time Fall Detection on Raspberry Pi using Human Pose Estimation and Spatial Temporal Graph Convolutional Networks (YOLOv8-Pose, ST-GCN, ONNX INT8)  
**Képzés:** Mérnökinformatikus / Programtervező Informatikus BSc  
**Készítés tanéve és féléve:** 2026/2027. tanév, Őszi félév (Szakdolgozat 1 / Tervezési félév)  
**Készítette:** Szakdolgozó Hallgató  
**Konzulensek:** Belső konzulens (Egyetemi Adjunktus), Külső konzulens (Számítógépes Látás és Beágyazott Rendszerek Szakértő)  
**Számítási infrastruktúra és hardverkörnyezet:**  
* *Neurális modell tanítási platform (Cloud GPU):* Google Colab / Kaggle felhő alapú hardveres gyorsítás (Nvidia Tesla T4 / P100 GPU, 16 GB VRAM, PyTorch), amely biztosítja az ST-GCN hálózat gyors és skálázható konvergenciáját.  
* *Helyi fejlesztői munkaállomás (Host PC):* AMD Ryzen 5 5500 CPU (6 mag / 12 szál @ 3.6–4.2 GHz), 16 GB DDR4 RAM, Windows 11 / Linux (adatelőkészítés, vázkinyerés, baseline tesztek).  
* *Beágyazott célhardver (Edge Device):* Raspberry Pi 5 (4GB/8GB, 4x ARM Cortex-A76 @ 2.4 GHz) / Raspberry Pi 4B (4x Cortex-A72 @ 1.5 GHz), Raspberry Pi Camera Module 3 (Sony IMX708, széles látószögű 120° FOV) / UVC USB kamera, Linux Debian ARM64 (Bookworm), ONNX Runtime ARM NEON INT8.  
**Kulcsszavak:** Számítógépes látás, Emberi pózbecslés, YOLOv8-Pose, Gráf Neurális Hálózatok (GNN), Tér-Időbeli Gráfkonvolúció (ST-GCN), Beágyazott rendszerek, Edge AI, Raspberry Pi, Modell-kvantálás (INT8), Privacy-by-Design (GDPR), Idősgondozás, Esésdetektálás, Egészségügyi távfelügyelet.

---

## Vezetői összefoglaló és absztrakt

### Magyar nyelvű absztrakt
A számítógépes látás és az intelligens viselkedéselemzés egyik legkritikusabb, életvédelmi alkalmazási területe az emberi esések, egyensúlyvesztések és hirtelen mozgásképtelenségek valós idejű, automatizált felismerése. A demográfiai öregedés következtében az egyedül élő idős emberek körében bekövetkező esések száma folyamatosan emelkedik. Az esések kimenetelét döntően a földön töltött idő határozza meg, mivel az elhúzódó fekvés órákon belül kihűléshez, izomelhaláshoz és végzetes szövődményekhez vezet. A piacon elérhető hagyományos megoldások – mint a hordható vészhívó órák vagy a padlószenzorok – csődöt mondanak, ha a felhasználó elfelejti felvenni az eszközt, vagy eszméletvesztés miatt képtelen manuálisan riasztani. A hagyományos felhő-alapú videomegfigyelő rendszerek pedig súlyos adatvédelmi (GDPR) ellenállásba ütköznek a magánszférát sértő képtovábbítás miatt, miközben folyamatos internetkapcsolatot és drága szerverkapacitást igényelnek.

Jelen szakdolgozati kutatás és megvalósítás célja egy olyan autonóm, peremhálózati (Edge AI) esésdetektáló és viselkedéselemző beágyazott rendszer kifejlesztése, amely egy alacsony fogyasztású, kompakt mikroszámítógépen (Raspberry Pi 4 / 5) valós időben fut. A feldolgozási lánc a legmodernebb egyfokozatú 2D pózbecslő modellt (YOLOv8-Pose) kombinálja Tér-Időbeli Gráfkonvolúciós Hálózattal (ST-GCN). A rendszer szigorúan érvényesíti a „Privacy-by-Design” elvet: az RGB videókockák a memóriában mindössze egyetlen ezredmásodpercre léteznek, a kulcspontok kinyerése után azonnal megsemmisülnek; a döntéshozatal kizárólag a 17 kulcspont koordináta-gráfján történik, így képi információ soha nem hagyja el az eszközt. A modell tanítása felhő alapú GPU környezetben (Google Colab T4) történik, míg a beágyazott ARM architektúra korlátozott erőforrásainak maximális kihasználása érdekében a neurális hálózatokat INT8 poszt-tanítási kvantálással (Post-Training Quantization) optimalizáljuk az ONNX Runtime motorban, kihasználva az ARM NEON SIMD vektoros utasításkészletét. A kutatás kitér a mindennapi természetes mozgások (gyors leülés, lefekvés, hajolás – ún. „Hard Negative” minták) és a valós esések szétválasztására, valamint a veszélyhelyzeti riasztások intelligens IoT integrációjára (MQTT, Webhook, helyi vészjelző).

### English Abstract
A life-critical domain in computer vision and intelligent human behavior analysis is the automated, real-time recognition of human falls, loss of balance, and sudden incapacitation. Driven by demographic aging, domestic falls among elderly individuals living alone are escalating rapidly. Clinical prognosis is largely governed by the "time-on-floor": unassisted immobilization for extended periods induces hypothermia, rhabdomyolysis, and severe mortality risks. Conventional wearable alert pendants and smartwatches exhibit notoriously poor user compliance (frequently uncharged or forgotten during bathing/sleep), whereas cloud-based video surveillance encounters massive data privacy (GDPR) rejection and imposes prohibitive network bandwidth dependencies.

This bachelor's thesis presents the research, design, implementation, and empirical evaluation of an autonomous, privacy-preserving Embedded Edge AI fall detection system running on low-power single-board computers (Raspberry Pi 4 / 5). The processing pipeline extracts 2D anatomical keypoints via a lightweight YOLOv8-Pose estimator and constructs spatiotemporal topological graphs processed by a Spatial Temporal Graph Convolutional Network (ST-GCN). Strictly complying with "Privacy-by-Design" regulations, raw video frames are purged from volatile memory immediately after keypoint regression; the decision logic operates exclusively on abstract 17-point coordinate topologies, preventing visual surveillance leakage. Model training is accelerated on cloud GPUs (Google Colab T4), while edge deployment on resource-constrained ARM Cortex-A processors is achieved via INT8 Post-Training Quantization (PTQ) executed through ONNX Runtime with ARM NEON SIMD acceleration. The research rigorously focuses on discriminating genuine falls from complex Activities of Daily Living (ADLs like rapid sitting, tying shoes, lying down), and integrates automated local IoT emergency notifications (MQTT, Webhooks, local buzzers).

---

## 1. Bevezetés és a kutatás háttere

### 1.1 Társadalmi, demográfiai és egészségügyi kontextus: Az esések epidemiológiája
A 21. század fejlett társadalmainak egyik legjelentősebb civilizációs és szociálpolitikai kihívása a népesség korfájának drasztikus elöregedése. Az Európai Unió statisztikai hivatala (Eurostat, 2023) [9] és az Egészségügyi Világszervezet (WHO, 2021) [5] előrejelzései alapján 2050-re az Európai Unió lakosságának több mint 30%-a 65 év feletti lesz, miközben az egyedül élő (*single-person household*) idős személyek aránya rekordmagasságot ér el. 

Ebben a demográfiai csoportban a mobilitás elvesztésének, az önálló életvitel megszűnésének és a traumatológiai mortalitásnak a vezető oka az **elesés**:
* A 65 év feletti lakosság mintegy 30-35%-a esik el legalább egyszer évente [5].
* A 80 év feletti populációban ez a prevalencia meghaladja az 50%-ot [5].
* Az elesések felelősek a 65 év felettiek traumatológiai kórházi felvételeinek több mint 65%-áért (combnyaktörés, medencetörés, koponyasérülések) [5, 15].
* Az orvosi ellátási költségek globálisan több tízmilliárd eurót emésztenek fel évente, miközben az intézményi idősotthoni kapacitások világszerte szűkösek.

Az esések megelőzése mellett az informatikai rendszerek legfontosabb feladata az incidensek bekövetkeztekor a **másodperceken belüli, automatizált detektálás és segítségkérés** [15].

### 1.2 Az „aranyóra” és a földön töltött idő orvosi szövődményei
A traumatológiai és gerontológiai orvostudomány konszenzusa szerint az esést követő kimenetelt nem csupán a becsapódás ereje, hanem a **földön töltött idő** (*time-on-floor*) határozza meg [3, 15]:
1. **Az első óra („Golden Hour”):** Amennyiben az elesett személy 60 percen belül szakszerű orvosi vagy gondozói ellátásban részesül, a maradandó szövődmények aránya minimális, a combnyaktörések sebészeti rehabilitációja sikeres, és a 72 órán belüli túlélési ráta meghaladja a 85%-ot.
2. **Elhúzódó földön fekvés (> 1 óra):** Ha az egyedül élő bajbajutott órákon keresztül mozgásképtelenül fekszik a hideg padlón, súlyos, életveszélyes kaszkádfolyamatok indulnak be:
   * *Hipotermia (kihűlés):* Még szobahőmérsékleten is a talajjal való hosszas érintkezés és a mozdulatlanság a maghőmérséklet végzetes zuhanását okozza.
   * *Rhabdomyolysis (akut izomszövet-szétesés):* A saját testsúly okozta tartós nyomás alatt az izomsejtek vérellátása megszűnik, elhalnak, és a véráramba kerülő mioglobin akut tubuláris nekrózist, azaz visszafordíthatatlan veseelégtelenséget vált ki.
   * *Hiposztatikus tüdőgyulladás és dekubitusz (felfekvés):* A sokkos, fekvő helyzetben a légutak folyadékfelhalmozódása órák alatt letális bakteriális felülfertőződéshez vezet.

A statisztikák szerint amennyiben a földön fekvés meghaladja a 6 órát, a halálozási ráta 6 hónapon belül eléri az 50%-ot [15], még akkor is, ha közvetlen törés nem történt. Ezért alapvető műszaki követelmény, hogy a rendszer emberi segítségkérés nélkül, passzív módon generáljon riasztást.

### 1.3 Meglévő technológiai megközelítések és azok korlátai
Az elesések detektálására a technológia történetében három fő műszaki irányvonal alakult ki, amelyek mindegyike komoly akadályokba ütközik [15]:

| Kategória | Megoldások | Előnyök | Döntő Hátrányok és Bukási Okok |
| :--- | :--- | :--- | :--- |
| **Hordható eszközök (Wearables)** | Okosórák, medálok, IMU gyorsulásmérők, övcsipeszek | Olcsó, bárhol működhet | **Felhasználói elutasítás és feledékenység:** Az idősek fürdéskor és alváskor leveszik (miközben a fürdőszoba a legfőbb esési helyszín). Eszméletvesztés vagy bénulás esetén a pánikgomb benyomhatatlan. |
| **Környezeti és padlószenzorok (Ambient)** | Nyomásérzékeny szőnyegek, padló-piezo, radarok | Érintésmentes, nem kell viselni | **Horribilis költség és holtterek:** A teljes lakás padlójának átalakítása gazdaságtalan; nem lát a bútorok alá. Leeső tárgyakat nem tud megkülönböztetni embertől (téves riasztások). |
| **Hagyományos videomegfigyelés (RGB Cloud)** | Felhőbe streamelő biztonsági IP kamerák, 3D CNN-ek | Gazdag vizuális információ | **Súlyos GDPR és adatvédelmi aggályok:** A magánszférába (háló, fürdő) senki sem enged videokamerát. Óriási hálózati sávszélesség- és felhőszerver-költség. |

### 1.4 A peremhálózati intelligencia (Edge AI) és a Raspberry Pi mikroszámítógép szerepe
A fenti korlátok és a gyakorlati megvalósíthatóság metszéspontjában a modern beágyazott mesterséges intelligencia (**Embedded Edge AI**) áll. A felhőbe történő képtovábbítás és a nagyméretű, drága, zúgó asztali munkaállomások lakossági környezetben történő elhelyezése helyett a teljes feldolgozási és döntési láncot egy kisméretű, diszkrét mikroszámítógépre – kiemelten a **Raspberry Pi 4 és Raspberry Pi 5** [11] platformra – optimalizáljuk.

A Raspberry Pi Edge AI koncepció négy döntő mérnöki előnnyel rendelkezik:
1. **Fizikai diszkréció és lakossági elfogadás:** A mikroszámítógép egy kompakt falra vagy mennyezetre rögzíthető dobozban elhelyezhető a hozzá csatlakozó kameramodullal (pl. Raspberry Pi Camera Module 3). Csendes, észrevétlen, nem kelti megfigyeltség vagy kórházi jelleg érzetét.
2. **Költséghatékonyság:** A beágyazott egykártyás mikroszámítógép ára a töredéke egy dedikált szervernek vagy asztali munkaállomásnak, így az önkormányzati vagy családi idősgondozásban széles körben skálázható.
3. **Minimális energiafogyasztás:** A rendszer tipikus áramfelvétele 5–10 Watt között alakul, szemben egy asztali PC 150–300 Wattos fogyasztásával, ami a nap 24 órájában futó biztonsági felügyeletnél alapvető üzemeltetési szempont.
4. **Hálózat- és felhőfüggetlenség:** A detektálás és a helyi riasztás internetkapcsolat nélkül, offline üzemben is megbízhatóan lefut; hálózati kimaradás esetén is védi a felügyelt személyt.

### 1.5 A váz-alapú gráfkonvolúciós paradigma (YOLOv8-Pose + ST-GCN) és a Privacy-by-Design elv
Jelen kutatás egy modern, a számítógépes látás és a gépi tanulás legújabb eredményeire támaszkodó megközelítést alkalmaz: a **váz-alapú akciófelismerést** (*Skeleton-Based Human Action Recognition*) [1, 8, 17].

A megközelítés filozófiai és technikai alapja a **geometriai absztrakció és a dimenziócsökkentés**:
Ahelyett, hogy a videófolyam gigabájtos képmátrixait próbálnánk meg elemezni – amely információ 99%-ban a döntés szempontjából irreleváns hátteret, szobabútort, falszínt és ruházati textúrát tartalmaz –, a beérkező képekből egy könnyűsúlyú, előre tanított mély neurális hálózattal (**YOLOv8-Pose**) [2] kinyerjük az emberi test anatómiai kulcspontjait.

Egy embert a COCO-17 topológia szerint mindössze **17 darab kétdimenziós koordináta** ($x_i, y_i$) és a hozzájuk tartozó láthatósági megbízhatóság ($conf_i$) ír le:
$$v_i = (x_i, y_i, conf_i), \quad i \in \{0, \dots, 16\}$$

Ezt az absztrakciót egy **Tér-Időbeli Gráfkonvolúciós Hálózat** (ST-GCN) [1] dolgozza fel, amely az emberi vázat egy tér-időbeli irányítatlan gráfként értelmezi. A térbeli élek a test valódi csontjait, az időbeli élek pedig az ízületek egymást követő képkockák közötti folytonos trajektóriáját reprezentálják.

#### A paradigma két döntő előnye:
1. **Beépített adatvédelem (Privacy-by-Design / GDPR megfelelőség):**  
   Az RGB videókockák a mikroszámítógép memóriájában mindössze egyetlen ezredmásodpercig léteznek, amíg a pózbecslő kiolvassa a csúcsokat; ezután a képpontok azonnal megsemmisülnek. A megmaradó számpárokból az egyén arca, neme, etnikuma vagy meztelensége **matematikailag rekonstruálhatatlan**. A rendszer nem képi megfigyelést végez, hanem egy absztrakt geometriai pálcikaember mozgásfizikáját elemzi, így maradéktalanul megfelel az Európai Unió GDPR 9. cikkének [9].
2. **Kiváló erőforrás-hatékonyság (Edge AI és ARM INT8 megvalósíthatóság):**  
   Mivel a gráfkonvolúció nem hatalmas képmátrixokon, hanem mindössze 17 pontból álló kompakt tenzorokon operál, a következtetési idő pár ezredmásodpercre csökken. A poszt-tanítási INT8 kvantálás [6] és az ARM NEON utasításkészlet révén a teljes rendszer képes stabil, **$\ge 25$ FPS valós idejű sebességgel futni egy Raspberry Pi mikroszámítógépen**, drága és nagy fogyasztású videokártya nélkül.

### 1.6 A kutatás célkitűzései és a diplomamunka hatóköre (Scoping)

#### 1.6.1 A hivatalos feladatkiírás teljesítése
A diplomamunka célja a tanszéki feladatkiírással összhangban:
1. **Architektúrák vizsgálata:** A korszerű valós idejű pózbecslő eljárások (kiemelten az Ultralytics YOLOv8-Pose) [2], valamint a gráf neurális hálózatok (GNN, ST-GCN) [1, 7] matematikai és strukturális elemzése.
2. **Adatfolyam és modelltervezés:** Olyan szoftveres folyamat megtervezése, amely a beágyazott kameraszenzortól a normalizált ízület-csont gráfokig vezet, és felépíti az ST-GCN tér-időbeli rétegeit.
3. **Beágyazott optimalizáció:** A modellek átalakítása és poszt-tanítási INT8 kvantálása az ONNX Runtime [10] motorban a Raspberry Pi ARM NEON architektúrájára.
4. **Szoftveres megvalósítás és kiértékelés:** A modell implementálása PyTorch környezetben, betanítása és tesztelése nyilvános referencia-adathalmazokon (UR Fall Detection [3], Le2i Fall [4]), a pontosság mérése szabványos metrikákkal (Recall, Precision, F1, ROC-AUC), valamint a zajos és takart adatokkal szembeni robusztusság számszerűsítése.
5. **Valós idejű prototípus és IoT integráció:** Egy stabilan működő, élő webkamerás és mikroszámítógépes demonstrációs szoftver létrehozása, amely hiszterézis-alapú döntési logikával, helyi hangjelzéssel és MQTT/Webhook alapú vészjelzéssel azonnal értesíti a környezetet.

#### 1.6.2 Tudatos lehatárolások (mit NEM tartalmaz a dolgozat)
* **Egyetlen személyre optimalizált fókusz ($M=1$):** A jelenlegi kutatási fázis célja az egyedül élő idős személyek felügyelete. Amennyiben a látótérben átmenetileg több személy tartózkodik (pl. látogató, gondozó), a csővezeték a legmagasabb detekciós konfidenciájú személy vázát követi ($M=1$). A több személy párhuzamos térbeli követése és interakciós gráf-fúziója a továbbfejlesztési lehetőségek (8. fejezet) között kerül megjelölésre.
* **Arcfelismerés és személyazonosítás teljes kizárása:** A rendszer semmilyen biometrikus azonosítót nem használ; célja kizárólag a mozgás típusának megállapítása.
* **Saját pózbecslő nulláról való betanítása:** A pózbecslésre előre tanított COCO súlyokat alkalmazunk transzfer tanulással, mivel a feladatkiírás szerint a hangsúly a gráfalapú elemző modellen és a beágyazott optimalizáción van.
* **Egészségügyi diagnosztika:** A rendszer nem állít fel orvosi kórképet, feladata kizárólag a mechanikai esés/zuhanás és a földön maradás tényének megbízható észlelése és jelzése.

---

## 2. Kutatási célok, kérdések és formális hipotézisek

### 2.1 A kutatás fő és részcéljai
A munkafolyamat három fő pillérre épül:
1. **Elméleti és modelltervezési pillér:** A 2D pózbecslés és a tér-időbeli gráfkonvolúció matematikai formalizmusának tisztázása, a COCO-17 topológia gráfpartícióinak kidolgozása, és az esési kinematika modellezése.
2. **Beágyazott mérnöki és optimalizációs pillér:** A mély tanulási modellek transzformálása korlátozott erőforrású ARM Cortex-A környezetre. Az FP32 lebegőpontos tenzorok INT8 poszt-tanítási kvantálása, valamint az aszinkron többfolyamatos adatfeldolgozás megtervezése.
3. **Empirikus és validációs pillér:** Nemzetközi referencia-adathalmazokon (UR Fall, Le2i) és saját szobai tesztvideókon végzett összehasonlító mérések elvégzése a klasszikus baseline modellekkel (kinematikai szabályrendszer, Bi-LSTM) szemben.

### 2.2 Kutatási kérdések (Research Questions)
* **RQ1 (Diszkriminációs képesség a „Hard Negative” mintákkal szemben):**  
  *Kérdés:* Képes-e az ST-GCN hálózat legalább $95\%$-os Recall mellett szignifikánsan alacsonyabb téves riasztási arányt (FPR $\le 5\%$) elérni a hétköznapi, esésre emlékeztető gyors mozgásokkal (gyors leülés, fotelbe huppanás, cipőkötés, ágyba dőlés) szemben, mint a hagyományos kinematikai baseline modellek?
* **RQ2 (A gráfalapú topológia többlete a szekvenciális modellekhez képest):**  
  *Kérdés:* Mekkora mértékű pontosságnövekedést (F1-score és ROC-AUC) biztosít a test anatómiai csontjait explicit módon modellező térbeli gráfkonvolúció a pontokat lapos vektorként kezelő szekvenciális hálózatokhoz (pl. Bi-LSTM) képest?
* **RQ3 (Valós idejű megvalósíthatóság beágyazott ARM célhardveren):**  
  *Kérdés:* Elérhető-e a folyamatos, akadásmentes valós idejű működés ($\ge 25$ FPS bemeneti feldolgozás) egy Raspberry Pi 5 mikroszámítógépen dedikált NPU nélkül, kizárólag a CPU ARM NEON utasításkészletére támaszkodó INT8 ONNX kvantálás révén?
* **RQ4 (Robusztusság részleges takarással és zajjal szemben):**  
  *Kérdés:* Hogyan befolyásolja az esésfelismerés megbízhatóságát, ha a lakás bútorai miatt az alsótesti kulcspontok (térdek, bokák) átmenetileg takarásba kerülnek, és képes-e a modell a láthatósági megbízhatósági faktorok ($conf_i$) integrálásával fenntartani a stabil működést?

### 2.3 Formális hipotézisek (Hypotheses)
* **H1 Hipotézis:** Az ST-GCN gráfmodell a térbeli csont-kapcsolatok és az időbeli gyorsulási mintázatok együttes tanulása révén **legalább 8-12 százalékponttal magasabb F1-értéket** ér el a nehéz negatív mintákon (leülés, hajolás), mint a kézzel skálázott kinematikai heurisztikus döntési algoritmus.
* **H2 Hipotézis:** A normál napi leülés és a valódi esés közötti elválasztáshoz egy $T=32$ képkockás (~1.0 másodperces) tér-időbeli csúszóablak elegendő információt szolgáltat arra, hogy a modell **96% feletti Szenzitivitást (Recall)** érjen el az UR Fall Detection tesztkészleten.
* **H3 Hipotézis:** A YOLOv8n-pose és az ST-GCN modellek INT8 poszt-tanítási kvantálásával a memóriafoglalás legalább $60\%$-kal csökken, míg a végrehajtási idő Raspberry Pi 5 eszközön a 40 ms/képkocka határérték alá szorítható, biztosítva a stabil **25 FPS sebességet**.
* **H4 Hipotézis:** Az adaptív háromfázisú hiszterézis döntési mechanizmus (amely a zuhanási fázist követően minimálisan 0.6 másodperces horizontális inaktivitást követel meg) a felkelési, leülési és átmeneti mozgásokból származó téves riasztási arányt (False Positive Rate – FPR) **statisztikailag szignifikáns módon $2.0\%$ alá szorítja** az ADL tesztkészleten.
"""

print("[OK] Part 1 (revised) written successfully.")
