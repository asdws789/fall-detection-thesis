# 1. Bevezetés és a kutatás háttere

## 1.1 Társadalmi és egészségügyi kontextus: A demográfiai öregedés és az esések epidemiológiája

A 21. század fejlett társadalmainak egyik legjelentősebb demográfiai folyamata a népesség korfájának elöregedése. Az Európai Unió statisztikai hivatala (Eurostat) és az Egészségügyi Világszervezet (WHO) előrejelzései szerint 2050-re a 65 év felettiek aránya a teljes népességen belül meg fogja haladni a 30%-ot. Ezzel párhuzamosan a szociális és egészségügyi ellátórendszerekre nehezedő nyomás exponenciálisan növekszik, különösen az egyedül élő (*single-person household*), önálló életvitelt folytató idős emberek biztonságának fenntartása terén.

Ebben a populációban a mobilitás elvesztésének, a hirtelen egészségromlásnak és az intézményi elhelyezésre való rászorulásnak a vezető oka az **esések és háztartási balesetek** előfordulása. A statisztikai adatok riasztóak:
* A 65 év feletti népesség mintegy egyharmada esik el legalább egyszer évente.
* A 80 év feletti korosztályban ez az arány eléri az 50%-ot.
* Az esések képezik a nem szándékos sérülésből eredő halálozások első számú okát az idősek körében, és a traumatológiai kórházi felvételek több mint 60%-áért felelősek (leggyakrabban combnyaktörés, koponyasérülések és súlyos lágyrész-zúzódások formájában).

Az esések azonban nem csupán az idősgondozásban jelentenek kockázatot: az ipari munkavédelemben (építkezések, raktárbázisok, veszélyes üzemek egyedül dolgozó műszakos munkatársai), valamint a neurológiai megbetegedésekben (epilepszia, Parkinson-kór, hirtelen ájulással – szinkópéval járó szívritmuszavarok) szenvedő betegek mindennapjaiban is kritikus vészhelyzetet jelentenek.

---

## 1.2 Az "aranyóra" és a földön töltött idő kritikus következményei

Az orvosi szakirodalomban régóta ismert alapvetés, hogy egy esés kimenetelét, a maradandó egészségkárosodás mértékét és a túlélési esélyeket döntően a **segítségnyújtás megérkezéséig eltelt idő** (*time-to-help*), illetve a **földön töltött idő** (*time-on-floor*) határozza meg:

* **Az első óra ("Golden Hour"):**  
  Amennyiben a földre került személy az incidenst követő 60 percen belül orvosi vagy gondozói ellátásban részesül, a szövődmények kockázata minimális, a combnyaktörések műtéti rehabilitációs esélye jó, és a túlélési arány 85% feletti.
* **Elhúzódó földön fekvés (> 1 óra):**  
  Ha a bajbajutott órákon keresztül segítség nélkül fekszik a padlón – ami egyedül élő idős embereknél a segítségkérés képtelensége miatt gyakran 6–24 órás időtartamot is elér –, rendkívül súlyos, életveszélyes másodlagos patológiás folyamatok indulnak be:
  1. *Hipotermia (kihűlés):* Még fűtött szobában is a hideg padlóval való hosszas érintkezés a testhőmérséklet drasztikus zuhanásához vezet.
  2. *Rhabdomyolysis (izomszövet-szétesés):* A saját testsúly okozta tartós nyomás hatására az izomsejtek elhalnak, és a véráramba kerülő mioglobin akut veseelégtelenséget idéz elő.
  3. *Tüdőgyulladás és felfekvések:* A mozdulatlan, sokkos állapotban fekvő betegeknél órák alatt hiposztatikus pneumonia alakul ki.

Az elhúzódó földön fekvés esetén a mortalitási ráta 72 órán belül meghaladja az 50%-ot. Ebből fakadóan a védelmi rendszerekkel szemben támasztott legfőbb követelmény az **azonnali, emberi beavatkozást nem igénylő, automatikus riasztásgenerálás**.

---

## 1.3 Meglévő technológiai megoldások és azok alapvető korlátai

Az esések észlelésére kifejlesztett korábbi műszaki megoldások alapvetően három kategóriába sorolhatók, amelyek mindegyike komoly korlátokkal küzd a mindennapi gyakorlatban:

### 1. Hordható eszközök (Wearable Sensors)
Okosórák, csuklópántok, nyakba akasztható pánikgombok, övre rögzített gyorsulásmérők (IMU szenzorok).
* *A korlátok oka:* Az emberi tényező és a szituációs korlátok. Az idős felhasználók rendkívül alacsony hajlandóságot mutatnak a folyamatos viselésre: fürdés előtt leveszik (miközben a csúszós fürdőszoba a legfőbb esési gócpont), éjszakára töltőre teszik, vagy egyszerűen elfelejtik felvenni. A manuális vészhívó gombok pedig teljesen hatástalanok, ha a személy az esés során elveszíti az eszméletét, beveri a fejét, vagy a sokk és mozgásképtelenség miatt képtelen elérni a gombot.

### 2. Környezeti és padlószenzorok (Ambient & Floor Sensors)
Nyomásérzékeny szőnyegek, padló alá épített piezoelektromos érzékelők, ultrahangos vagy mikrohullámú radaros mozgásérzékelők.
* *A korlátok oka:* Telepítési költség és alacsony információtartalom. Egy lakás teljes padlózatának szenzorozása hatalmas beruházási költséggel jár, a bútorok alatti holttereket nem fedi le, és képtelen megkülönböztetni egy földre eső nehéz tárgyat (pl. könyvespolcról leeső táskát) egy embertől, ami gyakori téves riasztáshoz vezet.

### 3. Hagyományos RGB videomegfigyelő rendszerek
Kamerák képeit közvetlenül feldolgozó 2D és 3D mély konvolúciós hálózatok, optikai áramlás alapú módszerek.
* *A korlátok oka:* Adatvédelem és hardverigény. A lakásban – különösen a privát zónákban, mint hálószoba vagy fürdőszoba – elhelyezett, nyers videót rögzítő kamerák a személyiségi jogok (GDPR) és a személyes intimitás brutális megsértését jelentik. Emellett a több millió képpontot elemző 3D CNN-ek számítási kapacitásigénye olyan magas, hogy gazdaságosan nem üzemeltethetők kisméretű helyi eszközökön.

---

---

## 1.4 A peremhálózati intelligencia (Edge AI) és a Raspberry Pi mikroszámítógép szerepe

A fenti korlátok és a gyakorlati megvalósíthatóság metszéspontjában a modern beágyazott mesterséges intelligencia (**Embedded Edge AI**) áll. A felhőbe történő képtovábbítás és a nagyméretű, drága, zúgó asztali munkaállomások lakossági környezetben történő elhelyezése helyett a teljes feldolgozási és döntési láncot egy kisméretű, diszkrét mikroszámítógépre – kiemelten a **Raspberry Pi 4 és Raspberry Pi 5** platformra – optimalizáljuk.

A Raspberry Pi Edge AI koncepció négy döntő mérnöki előnnyel rendelkezik:
1. **Fizikai diszkréció és lakossági elfogadás:** A mikroszámítógép egy kompakt falra vagy mennyezetre rögzíthető dobozban elhelyezhető a hozzá csatlakozó kameramodullal (pl. Raspberry Pi Camera Module 3). Csendes, észrevétlen, nem kelti megfigyeltség vagy kórházi jelleg érzetét.
2. **Költséghatékonyság:** A beágyazott egykártyás mikroszámítógép ára a töredéke egy dedikált szervernek vagy asztali munkaállomásnak, így az önkormányzati vagy családi idősgondozásban széles körben skálázható.
3. **Minimális energiafogyasztás:** A rendszer tipikus áramfelvétele 5–10 Watt között alakul, szemben egy asztali PC 150–300 Wattos fogyasztásával, ami a nap 24 órájában futó biztonsági felügyeletnél alapvető üzemeltetési szempont.
4. **Hálózat- és felhőfüggetlenség:** A detektálás és a helyi riasztás internetkapcsolat nélkül, offline üzemben is megbízhatóan lefut; hálózati kimaradás esetén is védi a felügyelt személyt.

---

## 1.5 A váz-alapú gráfkonvolúciós paradigma (YOLOv8-Pose + ST-GCN) és a Privacy-by-Design elv

Jelen kutatás egy modern, a számítógépes látás és a gépi tanulás legújabb eredményeire támaszkodó megközelítést alkalmaz: a **váz-alapú akciófelismerést** (*Skeleton-Based Human Action Recognition*).

A megközelítés filozófiai és technikai alapja a **geometriai absztrakció és a dimenziócsökkentés**:
Ahelyett, hogy a videófolyam gigabájtos képmátrixait próbálnánk meg elemezni – amely információ 99%-ban a döntés szempontjából irreleváns hátteret, szobabútort, falszínt és ruházati textúrát tartalmaz –, a beérkező képekből egy könnyűsúlyú, előre tanított mély neurális hálózattal (**YOLOv8-Pose**) kinyerjük az emberi test anatómiai kulcspontjait.

Egy embert a COCO-17 topológia szerint mindössze **17 darab kétdimenziós koordináta** ($x_i, y_i$) és a hozzájuk tartozó láthatósági megbízhatóság ($conf_i$) ír le:
$$v_i = (x_i, y_i, conf_i), \quad i \in \{0, \dots, 16\}$$

Ezt az absztrakciót egy **Tér-Időbeli Gráfkonvolúciós Hálózat** (ST-GCN) dolgozza fel, amely az emberi vázat egy tér-időbeli irányítatlan gráfként értelmezi. A térbeli élek a test valódi csontjait, az időbeli élek pedig az ízületek egymást követő képkockák közötti folytonos trajektóriáját reprezentálják.

### A paradigma két döntő előnye:
1. **Beépített adatvédelem (Privacy-by-Design / GDPR megfelelőség):**  
   Az RGB videókockák a mikroszámítógép memóriájában mindössze egyetlen ezredmásodpercig léteznek, amíg a pózbecslő kiolvassa a csúcsokat; ezután a képpontok azonnal megsemmisülnek. A megmaradó számpárokból az egyén arca, neme, etnikuma vagy meztelensége **matematikailag rekonstruálhatatlan**. A rendszer nem képi megfigyelést végez, hanem egy absztrakt geometriai pálcikaember mozgásfizikáját elemzi, így maradéktalanul megfelel az Európai Unió GDPR 9. cikkének.
2. **Kiváló erőforrás-hatékonyság (Edge AI és ARM INT8 megvalósíthatóság):**  
   Mivel a gráfkonvolúció nem hatalmas képmátrixokon, hanem mindössze 17 pontból álló kompakt tenzorokon operál, a következtetési idő pár ezredmásodpercre csökken. A poszt-tanítási INT8 kvantálás és az ARM NEON utasításkészlet révén a teljes rendszer képes stabil, **$\ge 25$ FPS valós idejű sebességgel futni egy Raspberry Pi mikroszámítógépen**, drága és nagy fogyasztású videokártya nélkül.

---

## 1.6 A kutatás célkitűzései és a diplomamunka hatóköre (Scoping)

### 1.6.1 A hivatalos feladatkiírás teljesítése
A diplomamunka célja a tanszéki feladatkiírással összhangban:
1. **Architektúrák vizsgálata:** A korszerű valós idejű pózbecslő eljárások (kiemelten az Ultralytics YOLOv8-Pose), valamint a gráf neurális hálózatok (GNN, ST-GCN) matematikai és strukturális elemzése.
2. **Adatfolyam és modelltervezés:** Olyan szoftveres folyamat megtervezése, amely a beágyazott kameraszenzortól a normalizált ízület-csont gráfokig vezet, és felépíti az ST-GCN tér-időbeli rétegeit.
3. **Beágyazott optimalizáció:** A modellek átalakítása és poszt-tanítási INT8 kvantálása az ONNX Runtime motorban a Raspberry Pi ARM NEON architektúrájára.
4. **Szoftveres megvalósítás és kiértékelés:** A modell implementálása PyTorch környezetben, betanítása és tesztelése nyilvános referencia-adathalmazokon (UR Fall Detection, Le2i Fall), a pontosság mérése szabványos metrikákkal (Recall, Precision, F1, ROC-AUC), valamint a zajos és takart adatokkal szembeni robusztusság számszerűsítése.
5. **Valós idejű prototípus és IoT integráció:** Egy stabilan működő, élő webkamerás és mikroszámítógépes demonstrációs szoftver létrehozása, amely hiszterézis-alapú döntési logikával, helyi hangjelzéssel és MQTT/Webhook alapú vészjelzéssel azonnal értesíti a környezetet.

### 1.6.2 Tudatos lehatárolások (mit NEM tartalmaz a dolgozat)
* **Arcfelismerés és személyazonosítás teljes kizárása:** A rendszer semmilyen biometrikus azonosítót nem használ; célja kizárólag a mozgás típusának megállapítása.
* **Saját pózbecslő nulláról való betanítása:** A pózbecslésre előre tanított COCO súlyokat alkalmazunk transzfer tanulással, mivel a feladatkiírás szerint a hangsúly a gráfalapú elemző modellen és a beágyazott optimalizáción van.
* **Egészségügyi diagnosztika:** A rendszer nem állít fel orvosi kórképet, feladata kizárólag a mechanikai esés/zuhanás és a földön maradás tényének megbízható észlelése és jelzése.

---

## 1.7 A szakdolgozat szerkezeti felépítése

A dolgozat a mérnöki kutatás és fejlesztés logikai lépéseit követve a következő fejezetekre tagolódik:

* **2. Szakirodalmi áttekintés és elméleti háttér:**  
  Részletesen tárgyalja az esésdetektálás történetét, a YOLOv8-Pose belső felépítését (CSPDarknet, PANet, OKS veszteség), az ST-GCN térbeli és időbeli gráfkonvolúciós rétegeinek matematikai levezetését és partíciós stratégiáit, valamint az INT8 poszt-tanítási kvantálás és az ARM NEON elméletét.
* **3. Rendszertervezés és szoftverspecifikáció (UML):**  
  Bemutatja az end-to-end adatfolyamot, a Raspberry Pi 4/5 és kamera hardverspecifikációt, az UML komponens-, szekvencia- és állapotgép-diagramokat, a csípőközép-alapú normalizálást, a háromfázisú döntési állapotgépet, valamint az IoT vészjelző alrendszert (MQTT, Webhook, Buzzer).
* **4. Empirikus esettanulmány (A naiv kinematika és a törpe-osztó anomália):**  
  Részletesen elemzi a korai heurisztikus kísérletekben tapasztalt felkelési hamis riasztást, levezeti a nevező-összeomlás matematikai okát, bemutatja a skálainvariáns $\max(W, H)$ normát, és tudományosan igazolja az ST-GCN gráfmodell szükségességét.
* **5. Adathalmazok és kísérleti módszertan:**  
  Ismerteti az UR Fall Detection és Le2i Fall benchmark adatbázisokat, a saját kontrollált tesztvideók forgatókönyveit, felépíti a baseline modelleket (Random Forest, Bi-LSTM) és az ST-GCN hálózatot, rögzítve a tanítási hiperparamétereket.
* **6. Kísérleti eredmények és kiértékelés:**  
  Összehasonlítja a modellek teljesítményét (külön fókuszálva a gyors leülés vs. esés hibaelemzésére), megválaszolja az RQ1–RQ4 kutatási kérdéseket, igazolja a hipotéziseket, és bemutatja a részletes Edge teljesítmény-profilozást (PC Ryzen 5 vs. Raspberry Pi 4 és 5: FPS, késleltetés, RAM, CPU %, fogyasztás).
* **7. Prototípus implementáció és demonstráció:**  
  Ismerteti a többszálú valós idejű webkamerás és beágyazott szoftvermodulokat, a grafikus visszajelzést (színkódolt vázrajzolás, esésriasztás, FPS számláló).
* **8. Adatvédelmi, jogi és etikai megfontolások:**  
  Elemzi a GDPR 9. cikk szerinti megfelelést, a Privacy-by-Design alapelvet és az idősotthoni/otthoni etikai normákat.
* **9. Összegzés és kitekintés:**  
  Összefoglalja a kutatás fő eredményeit, számba veszi a korlátokat, és felvázolja a többkamerás fúzió és a hardveres NPU gyorsítók (pl. Hailo-8L) távlatait.
