# 1. Bevezetés és a kutatás háttere

## 1.1 A szórakozóhelyi biztonságvédelem gyakorlati és társadalmi kontextusa

Az éjszakai szórakoztatóipari létesítmények – klubok, zenés szórakozóhelyek, tánctermek és zárt terű rendezvényközpontok – a modern nagyvárosi társadalom szerves részét képezik, miközben biztonsági szempontból az egyik legkockázatosabb és legnehezebben kontrollálható működési környezetet jelentik. A zárt terekben egyidejűleg tartózkodó nagy létszámú embertömeg, a pszichoaktív szerek (különösen az alkohol) fogyasztásából eredő gátláscsökkenés, a magas hangerővel párosuló szenzoros túlterheltség, valamint a szociális interakciók magas frekvenciája együttesen olyan közeget teremtenek, amelyben a konfliktusok kialakulásának és gyors eszkalációjának esélye nagyságrendekkel magasabb az átlagos közterületi környezetekhez képest.

A kriminológiai és biztonságtechnikai vizsgálatok egyöntetűen rámutatnak arra, hogy a szórakozóhelyi agresszió ritkán jelenik meg előzmények nélküli, pillanatszerű eseményként. Az incidensek túlnyomó többsége egy jól definiálható dinamikai ívet követ, amely a következő diszkrét fázisokra bontható:
1. **Verbális és geszturális feszültségkeltési szakasz:** A konfliktusban érintett felek közötti intim zóna drasztikusan lecsökken, heves, aszimmetrikus mutogatás, fenyegető testtartás és verbális inzultusok jelennek meg.
2. **Pre-fizikai és alacsony intenzitású fizikai konfrontáció (pre-eszkaláció):** A felek közötti első fizikai kontaktusok formájában nyilvánul meg, mint a mellkasnak feszülés, megragadás, ruházat rángatása, illetve a kétkezes taszítás és lökdösődés (*shoving*).
3. **Akut fizikai erőszak és verekedés:** Nyílt testi támadások: célzott ütések, rúgások, birkózás, földre vitel, segédeszközök (például poharak, üvegek) fegyverként történő használata, valamint a konfliktus többszemélyes tömegverekedéssé alakulása.

A szórakozóhelyi erőszak legsúlyosabb következményei – mint a maradandó testi sérülések, koponyatraumák, orvosi beavatkozást igénylő zúzódások és a létesítmény üzemeltetőjét terhelő kártérítési és büntetőjogi felelősség – szinte kizárólag a harmadik, akut fázisban realizálódnak. Ebből fakadóan a védelmi stratégia kulcsa nem a már kibontakozott verekedések utólagos észlelése és elfojtása, hanem a második, úgynevezett pre-eszkalációs ablakban történő korai detekció és a biztonsági személyzet azonnali, preventív helyszíni jelenlétének biztosítása.

---

## 1.2 Az emberi megfigyelés kognitív korlátai és a felügyeleti infrastruktúra anomáliái

A szórakozóhelyeken ma alkalmazott védelmi rendszerek gerincét az emberi személyzet képezi: a helyszínen mozgó rendészek (biztonsági őrök, portások), valamint a zárt láncú kamerarendszert (CCTV) felügyelő operátorok. Bár az emberi szituációfelismerés és helyzetértékelés rugalmas, hatékonyságát fundamentális fiziológiai és pszichológiai korlátok determinálják.

A kognitív ergonómia területén jól dokumentált jelenség az **éberségcsökkenés** (*vigilance decrement*). Empirikus kísérletek bizonyítják, hogy egy megfigyelő mindössze 20–25 percnyi folyamatos videomonitorozás után a látóterében lezajló releváns biztonsági események közel 45%-át nem veszi észre. Negyven perc elteltével a figyelem-fáradás mértéke olyan szintre emelkedik, ahol a hibázási és tévesztési arány meghaladhatja a 75%-ot. 

Ezt a sérülékenységet megsokszorozza a **többkamerás felügyeleti paradoxon**. Egy korszerű szórakozóhelyen a terület nagyságától és tagoltságától függően 16–64 IP kamera közvetíti a képfolyamot a monitorfalra. Az operátornak meg kellene osztania a figyelmét a tánctér, a bárpultok előtere, a mosdókhoz vezető folyosók és a dohányzó zónák között. Az emberi szem pásztázó mozgása (szakkádok) és a látóideg feldolgozási korlátai miatt fizikai képtelenség másodpercenként 25–30 képkockás dinamikával több tucatnyi kameraképet párhuzamosan elemezni. 

Ennek közvetlen következménye a **késedelmes beavatkozás**: mire az operátor észreveszi az incidenst a mátrixban, vagy mire a járőröző személyzet a helyszínre érkezik, az összetűzés már túljutott a lökdösődés fázisán, a felek súlyos sérüléseket szenvedtek el, és a konfliktusba beavatkozó harmadik felek miatt a helyzet kezelése jelentős sérülési kockázatot ró magára a biztonsági személyzetre is.

---

## 1.3 Az automatizált képi felügyelet evolúciója és az RGB-megközelítés korlátai szórakozóhelyeken

Az emberi korlátok áthidalására az elmúlt évtizedben a számítógépes látás (*Computer Vision*) és a mélytanulás (*Deep Learning*) rohamos fejlődése kínált technológiai alternatívát. Az automatikus erőszakfelismerés (*Violence Detection*) szakirodalmában számos módszertan született, amelyek kezdetben kézzel tervezett vizuális jellemzőkre (például optikai áramlás, HOG, HOF), később mély konvolúciós hálózatokra, 3D konvolúciókra (C3D, I3D, SlowFast), valamint a közelmúltban videótranszformerekre (TimeSformer, Video Swin) épültek.

Bár ezek a rendszerek kiváló detekciós arányokat mutattak be nyilvános kutatási adathalmazokon (például jól megvilágított utcai felvételeken vagy laboratóriumi körülmények között), **valós szórakozóhelyi körülmények között szinte kivétel nélkül működésképtelenné válnak**. Ennek okai a szórakozóhelyi domain sajátos fizikai jellemzőiben gyökereznek:

1. **Extrém és dinamikus megvilágítási anomáliák:**  
   Az éjszakai klubokban a képpontok intenzitása nem állandó. A félhomályt 10–20 Hz-es frekvenciájú stroboszkópos villanások, forgó fénycsóvák és monokróm (vörös, zöld, kék) reflektorok pásztázzák. Az RGB-alapú mozgásbecslő algoritmusok alapját képező fényerő-állandósági feltétel (*Brightness Constancy Assumption*):
   $$I(x, y, t) \approx I(x + \Delta x, y + \Delta y, t + \Delta t)$$
   teljesen összeomlik. A villanó stroboszkóp hatására a számítógép a pixelek hirtelen megváltozását hatalmas virtuális mozgásként (optikai áramlási lökéshullámként) értelmezi, ami folyamatos, kezelhetetlen téves riasztáscunamit eredményez.

2. **Sűrű tömeg és súlyos testtakarák (Crowd Occlusion):**  
   A tánctéren az emberek rendkívül szorosan állnak. Az egymást részben vagy teljesen fedő testek megzavarják a pixel-szintű szegmentációt, az RGB detektorok elveszítik a kontúrokat, vagy két egymás mellett táncoló embert egyetlen amorf objektumként fuzionálnak.

3. **Nem standard kameraállások és perspektivikus torzítás:**  
   A szórakozóhelyeken a kamerákat vandalizmusvédelmi és rálátási okokból magasra (3–5 méter), a falak sarkára vagy a mennyezetre szerelik, ahonnan meredeken, ferdén lefelé tekintenek (*high-angle oblique perspective*). Ez a geometria drasztikusan összenyomja a függőleges testméreteket (*foreshortening*), amit az utcai felvételekre előtanított hagyományos RGB modellek nem tudnak megfelelően kezelni.

4. **Kritikus számítási kapacitásigény (Compute Bottleneck):**  
   A 3D konvolúciók és videótranszformerek számítási műveletigénye (több száz GFLOPs / másodperc) olyan magas, hogy egyetlen videóstream valós idejű futtatása is csúcskategóriás szerver-GPU-kat (pl. Nvidia A100) igényelne. Egy tucatnyi kamerával felszerelt szórakozóhelyen egy ilyen architektúra költsége gazdaságilag fenntarthatatlan.

---

## 1.4 A váz-alapú (skeleton-based) megközelítés és a Privacy-by-Design elv

A fenti akadályok feloldására a kutatás egy merőben új paradigmát, a **váz-alapú akciófelismerést** (*Skeleton-Based Action Recognition*) állítja a középpontba. E megközelítés lényege a radikális dimenziócsökkentés és geometriai absztrakció:
Ahelyett, hogy a videófolyam másodpercenként több millió színes képpontját próbálnánk közvetlenül elemezni – amely információ 99%-ban a feladat szempontjából irreleváns háttér, ruhaminta vagy világítási zaj –, a beérkező képkockákból kizárólag az emberi test biomechanikai kulcspontjait (ízületeit) nyerjük ki.

Egy embert a modern COCO topológia szerint mindössze **17 darab kétdimenziós koordináta** ($x_i, y_i$) és a hozzájuk tartozó detekciós megbízhatóság ($conf_i$) ír le:
$$v_i = (x_i, y_i, conf_i), \quad i \in \{1, \dots, 17\}$$

Ez a reprezentáció három felbecsülhetetlen értékű előnyt biztosít a szórakozóhelyi alkalmazásban:

* **Tökéletes környezet- és megvilágítás-invariancia:**  
  Miután az ízületi koordináták kinyerésre kerültek, az őket feldolgozó Tér-Időbeli Gráfkonvolúciós Hálózat (ST-GCN) számára a háttér színe, a ruha mintázata és a villódzó fény teljesen láthatatlanná válik. Az osztályozó kizárólag a csontváz anatómiai kapcsolatainak és időbeli mozgásdinamikájának tiszta fizikáját vizsgálja.
* **Extrém alacsony számítási overhead:**  
  A gráfkonvolúciós modell nem gigabájtos képmátrixokon, hanem mindössze néhány kilobájtos topológiai gráfokon operál, így a következtetési idő (*inference latency*) pár ezredmásodpercre csökken, lehetővé téve a valós idejű, többkamerás futtatást olcsóbb, lokális hardvereken is.
* **Beépített adatvédelem (Privacy-by-Design és GDPR megfelelőség):**  
  Az Európai Unió Általános Adatvédelmi Rendelete (GDPR 9. cikk) szigorúan védi a biometrikus és képi személyes adatokat. A váz-alapú feldolgozási láncban az RGB képkockák azonnal eldobásra és törlésre kerülnek a memóriából a kulcspontok kinyerése után. A megmaradó absztrakt koordinátákból az egyén arca, neme, etnikuma vagy identitása **matematikailag visszafejthetetlen**, így a rendszer nem minősül arcfelismerő vagy személyazonosító megfigyelésnek.

---

## 1.5 A korai jelzés és a pre-eszkalációs fázis jelentősége

A szakirodalomban fellelhető publikációk többsége a feladatot leegyszerűsíti egy bináris osztályozási problémára: a videóklipeket "Verekedés" (*Fight*) vagy "Nem verekedés" (*Non-Fight*) címkével látja el. A gyakorlati biztonságvédelem szempontjából azonban a már tomboló verekedés észlelése csupán kármentés, nem pedig valódi védelem. Mire a hálózat detektálja az ütésváltást vagy a földre vitelt, a testi sérülések már bekövetkeztek.

Jelen diplomamunka központi tézise, hogy a felismerési időablakot a **második fázisra, a pre-eszkalációs állapotra kell fókuszálni**. A lökdösődés (*shoving*), a mellkasnak feszülés és a heves, rángatózó gesztusok jól definiálható kinetikai lenyomatot hagynak a vázak térbeli és időbeli kapcsolataiban:
* A résztvevők közötti euklideszi távolság gyorsan lecsökken a kritikus kontaktzónába.
* A felsőtesti ízületek (csuklók, könyökök, vállak) gyorsulása és relatív elmozdulása hirtelen megnő, miközben a súlypont hátrafelé billen.
* A mozgás aszimmetrikus: az egyik fél aktívan taszít, míg a másik passzívan hátrál vagy egyensúlyát veszíti.

Ha az algoritmus képes ezt a pre-eszkalációs állapotot megbízhatóan felismerni, és a biztonsági személyzet kijelzőjén egy **sárga figyelmeztetést** (*Warning*) generálni, a személyzet átlagosan 5–15 másodperccel a tényleges ütések elcsattanása előtt beavatkozhat. Ez a néhány másodperc a különbség a békés szétválasztás és a mentőt igénylő súlyos testi sértés között.

A rendszer ezen filozófiája szigorúan illeszkedik az **Ember-a-hurokban (Human-in-the-Loop)** elvhez: a modell nem hoz autonóm ítéletet, nem indít retorziót, hanem a fáradó emberi operátor intelligens kiterjesztéseként, fókuszirányító döntéstámogató eszközként működik.

---

## 1.6 A kutatás célkitűzései és a diplomamunka hatóköre (Scoping)

### 1.6.1 A kutatás konkrét mérnöki és tudományos céljai
A szakdolgozat célja egy működő, valós idejű váz-alapú agresszió-felismerő prototípus megtervezése, kifejlesztése és empirikus kiértékelése szórakozóhelyi környezetre optimalizálva. A projekt konkrét feladatai:
1. **Adatfeldolgozó pipeline építése:** Olyan szoftveres architektúra létrehozása, amely a beérkező videófolyamból az Ultralytics YOLOv8-Pose modellel kinyeri a 17 kulcspontot, a ByteTrack / BoT-SORT algoritmusokkal folyamatosan fenntartja a személy-azonosítókat, és normalizált csúszóablak-tenzorokat képez.
2. **ST-GCN mélytanulási modell fejlesztése:** Tér-Időbeli Gráfkonvolúciós Hálózat betanítása a COCO-17 anatómiai topológián, Focal Loss veszteségfüggvénnyel, kétáramú (ízület és csont-vektor) fúzióval.
3. **Hard Negative diszkrimináció megoldása:** A ritmikus tánc és a kaotikus agresszió szétválasztásának vizsgálata mozgásharmonika és megfelelő időablakhossz ($T=48$) segítségével.
4. **Valós idejű benchmarking:** A futási idők, képkockasebesség (FPS) és késleltetések profilozása elérhető fogyasztói hardveren (Nvidia GPU), biztosítva a $\ge 25$ FPS sebességet.
5. **Operátori demonstrációs felület:** Interaktív demó szoftver megvalósítása hiszterézis-alapú riasztáskezeléssel és telemetriai kijelzővel.

### 1.6.2 Tudatos lehatárolások (mit NEM tartalmaz a dolgozat)
A BSc képzés időkereteinek és az etikai-jogi normáknak a betartása érdekében a kutatás határait szigorúan meghúzzuk:
* **Arcfelismerés és személyazonosítás teljes kizárása:** A rendszer semmilyen biometrikus arcmodellt nem futtat; az emberek a feldolgozás során csupán ideiglenes numerikus indexként (`track_id`) léteznek.
* **Akusztikus hanganalízis elhagyása:** Bár az intelligens megfigyelésben létezik sikoly- és hangdetekció, egy szórakozóhelyen a 100+ decibeles zene és mélynyomók miatt az audio-csatorna teljesen telített és alkalmatlan megbízható klasszifikációra.
* **Saját pózbecslő nulláról való tanításának mellőzése:** Nem célunk egy új 2D objektumdetektor kifejlesztése; az ipari szabványnak számító YOLOv8-Pose előtanított súlyait használjuk transzfer tanulással.
* **Éles éjszakai klubbeli üzemeltetés kizárása:** Jogi felelősségbiztosítási, üzleti titoktartási és személyiségi jogi akadályok miatt a tesztelés nyilvános felügyeleti benchmarkokon (RWF-2000, CCTV-Fights), valamint kontrollált, önkéntesekkel készített, szimulált szórakozóhelyi felvételeken zajlik.

---

## 1.7 A szakdolgozat szerkezeti felépítése

A szakdolgozat a logikai és mérnöki megvalósítás lépéseit követve a következő fejezetekre tagolódik:

* **2. Szakirodalmi áttekintés és elméleti háttér:**  
  Részletesen bemutatja az emberi pózbecslés fejlődését, a YOLOv8-Pose architektúráját és OKS veszteségfüggvényét, a modern többszemélyes követőket (ByteTrack, BoT-SORT), valamint a Tér-Időbeli Gráfkonvolúciós Hálózatok (ST-GCN) matematikai alapjait és partíciós stratégiáit.
* **3. Szórakozóhely-specifikus kihívások és rendszertervezés:**  
  Elemzi a tánc és verekedés közötti kinematikai eltéréseket, a sűrű tömeg takaráskezelését, a stroboszkóp- és világításfüggetlenséget, valamint specifikálja a moduláris szoftverarchitektúrát, a csípőközép-alapú koordináta-normalizálást és a kétküszöbös hiszterézis-szűrőt.
* **4. Adathalmazok és kísérleti módszertan:**  
  Ismerteti az RWF-2000 és CCTV-Fights referencia-adatbázisokat, a saját szimulált szórakozóhelyi felvételek rögzítési forgatókönyveit, a váz-alapú adatbővítési eljárásokat, valamint felépíti a baseline modelleket (Random Forest, LSTM) és a 9-blokkos ST-GCN hálózatot Focal Loss alkalmazásával.
* **5. Kísérleti eredmények és kiértékelés:**  
  Számszerűsíti a klasszifikációs metrikákat (Accuracy, Precision, Recall, Macro F1, ROC-AUC), elemzi a konfúziós mátrixokat, megválaszolja az RQ1–RQ4 kutatási kérdéseket, igazolja a hipotéziseket, és bemutatja a futásidejű profilozási adatokat.
* **6. Prototípus implementáció és demonstráció:**  
  Bemutatja a többszálú (Capture, Inference, Display) aszinkron adatfolyam-motort, a kódkönyvtár felépítését és az operátori riasztási felület működését.
* **7. Adatvédelmi és etikai megfontolások:**  
  Tárgyalja a GDPR 9. cikk szerinti megfelelést, a Privacy-by-Design elvet és a Human-in-the-Loop felügyeleti paradigmát.
* **8. Összegzés és kitekintés:**  
  Összefoglalja a kutatás fő elméleti és mérnöki hozzájárulásait, számba veszi a modell korlátait, és felvázolja a 3D váz-rekonstrukció és a beágyazott Edge AI irányába mutató továbbfejlesztési lehetőségeket.
