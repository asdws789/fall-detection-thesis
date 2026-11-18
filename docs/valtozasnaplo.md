# Változásnapló (valtozasnaplo.md)

**Dokumentum:** Szakdolgozat 1 – Kutatási és Rendszertervezési Terv (v3 verzió)  
**Téma:** Gráf alapú modellek detektálása vizuális információn, különös tekintettel a viselkedéselemzésre  
**Készült:** 2026. november 17.  
**Alapul szolgáló értékelés:** Konzulensi értékelés: Szakdolgozat 1, frissített kutatási terv  

---

## 1. Feladatonkénti Változáskövetés és Státusz (1–22. feladatok)

| Feladat sorszáma és megnevezése | Státusz | Elvégzett módosítások és mérnöki indoklás |
| :--- | :---: | :--- |
| **1. Cím visszaállítása** | **Elvégezve** | A címlapon, fejlécben és a teljes dokumentumban visszaállításra került a hivatalos témakiírás szerinti cím: *„Gráf alapú modellek detektálása vizuális információn, különös tekintettel a viselkedéselemzésre”* (az *„alkalmazása ... feldolgozására”* helyett). Az alcím és a kivonat bevezető mondata változatlan maradt. |
| **2a. Dupla felsorolásjelek tisztítása** | **Elvégezve** | A bekezdésekből eltávolításra kerültek a stílussal ütköző, kézzel beírt dupla felsorolásjelek. A szövegközi felsorolások egységes, bal margóhoz igazított függő behúzást (hanging indent) és tiszta bekezdéstördelést kaptak (nincs `\n` anomália a sorkizárt szövegben). Érintett bekezdések száma: 42 db. |
| **2b. Tartalomjegyzék automatizálása** | **Elvégezve** | A korábbi kézzel gépelt, statikus oldalszámos tartalomjegyzék helyére beépített dinamikus Word mezőkód (`w:fldChar` begin / separate / end, `TOC \o "1-3" \h \z \u`) került, helyettesítő instrukciós szöveggel. A `settings.xml` állományban bekapcsolásra került a `<w:updateFields w:val="true"/>` direktíva. A Kivonat és Tartalomjegyzék címsorok nincsenek Heading 1-re állítva, így nem kerülnek önmagukba. |
| **3a. Hibrid architektúra státusza (1.4)** | **Elvégezve** | Az 1.4 fejezet 2. pontjában a cím kiegészült a `(tervezett)` jelöléssel, a bekezdés végére pedig bekerült a pontosítás: *„Az FSM-réteg prototípus-szinten megvalósult; az ST-GCN és a hibrid fúzió a Szakdolgozat 2 feladata.”* |
| **3b. Komponensek megvalósítási státusza (3.2)** | **Elvégezve** | A 3.2 fejezet végére (a 3.1. ábra után) beillesztésre került a bevezető mondat és az új **3.4. táblázat: A komponensek megvalósítási státusza** 8 tétellel (VideoSource, YOLOv8s-Pose, Kinematika+FSM, Tkinter GUI, STGCNClassifier, HybridDecisionEngine, AlertDispatcher, ONNX/INT8/Pi5), benne a szerzői megerősítést kérő sárga `[TODO]` jelölésekkel. |
| **3c. FSM kód/terv konzisztencia TODO (3.4)** | **Elvégezve** | A 3.4 fejezet első bekezdésének végére sárga kiemeléssel bekerült a konzulens által kért TODO az ötállapotú automata és az első 4 állapotú prototípus eltérésének tisztázására. |
| **4. Kutatási kérdések és hipotézisek (1.5)** | **Elvégezve** | Az RQ1–RQ4 kérdések megmaradtak. H1–H4 a konzulens által előírt mérhető, tesztelhető sikerkritériumokkal újraírásra került (McNemar-próba, maszkolt szekvenciák, távoli szintmodell, headless p95 ciklusidő). Bekerült az új **RQ5** és **H5** (ST-GCN vs. nem gráf alapú LSTM/MLP baseline, bootstrap CI). A fejezet végére bekerült a módszertani rögzítésről szóló záró bekezdés. |
| **5. Hatókör és ismert korlátok (új 1.6)** | **Elvégezve** | Új Heading 2 alfejezetként beillesztésre került az **1.6 Hatókör és ismert korlátok** 5 pontos listával (Egyszemélyes jelenet TODO, Rögzített kameranézet, Megvilágítás/IR korlát, Színészi laboradatok korlátja, Soft-biometrikus GDPR adatvédelmi hatály). |
| **6a-e. Orvosi és demográfiai állítások (1.1, 1.2)** | **Elvégezve** | 6a: Eurostat 30% előrejelzéshez sárga forrás-TODO. 6b: WHO [5] hivatkozás és 80 év feletti arány ellenőrzési TODO. 6c: „Egyértelműen bizonyítja” helyett *„megfigyeléses vizsgálatok következetesen azt mutatják”*. 6d: Kiegészítés, hogy a fekvési idő kockázati marker, nem önálló ok. 6e: Golden Hour analógia jelzése és Cowley hivatkozási TODO. |
| **7a-d. Kinematika és paramétertáblázat (2.2)** | **Elvégezve** | 7a: $v_y(t)$ képlet formális bevezetése $1/\text{s}$ mértékegységgel és szerzői ellenőrzési TODO-val. 7b: A 2.2. táblázatban minden `frame^-1` és `frame⁻¹` cserélve `1/s`-ra. 7c: N_mem sorhoz zuhanási memória időablak ellenőrzési TODO fűzve. 7d: A táblázat után beillesztésre került az időalapú küszöbölés indoklása (FPS-függetlenség). |
| **8a-e. Related Work táblázat és szöveg (2.5)** | **Elvégezve** | 8a: Szerzők neve mellé szögletes zárójeles hivatkozások ([10], [11], [3], [12], [1]). 8b: Cao et al. sora pontosítva (pózbecslő, nem esésdetektáló, nincs esési metrikája). 8c: Yan et al. eredeti NTU-RGB+D számai beírva (~81,5% X-Sub, ~88,3% X-View) ellenőrzési TODO-val. 8d: Saját sor eredmény cellája átírva: *„Tervezett értékelés: lásd 7.4. (publikált eredményekkel csak mérés után összevethető)”*. 8e: Táblázat utáni sárga TODO a metrikák ellenőrzésére, és új bekezdés a csontváz alapú versenytársakról (Keskes & Noumeir TODO). |
| **9a-e. Nem-funkcionális követelmények (3.2)** | **Elvégezve** | 9a: NFR-01 headless mérés kiegészítés. 9b: NFR-03 Wilson 95% CI kritérium (kb. 73 független esésminta). 9c: NFR-04 klipenkénti és óránkénti FPR definíció (kb. 60–75 negatív minta). 9d: NFR-05 fájlrendszer/hálózati forgalomelemzés kiegészítés. 9e: Új sor: **NFR-08: Beágyazott futási sebesség (opcionális)** (Raspberry Pi 5: ≥ 15 FPS TODO). |
| **10a-b. FSM állapotgép pontosítások (3.4)** | **Elvégezve** | 10a: A 3.3. táblázatba új sor került: `UNSTABLE / FALLING` $\to$ `FALLEN` detekcióvesztés kezelése ($N_{kpts} = 0$, belső képtartomány, zuhanási előzmény) azonnali átmenettel és kód-TODO-val. 10b: A FALLING $\to$ NORMAL sorban a `rest_ratio` definícióhiányát jelző sárga TODO elhelyezve. |
| **11a-c. Hibrid arbitráció és reprezentáció (3.5)** | **Elvégezve** | 11a: Átdolgozott döntési fúziós szöveg $P_{FSM}$ leképezéssel, adaptív $\alpha$ súlyozással és hangolási tervvel. 11b: Három új bekezdés félkövér címkével: *Koordináta-normalizálás és pozíciócsatornák* (bbox vs. képkeret relatív), *Kulcsponthiány kezelése* (zéró koordináta, $c=0$, DropGraph maszkolás), *Időalapú ablak* ($1,2\text{ s}$, 25 FPS újramintavételezés). 11c: Csatornaszám bővülési megjegyzés $X_{window}$ tenzornál. |
| **12a-d. Peremesetek szövegpontosítása (4.3, 4.4)** | **Elvégezve** | 12a: 4.3 lezárása átírva (ST-GCN pozíciócsatornákkal kiegészítve, távoli esések kísérleti feladata). 12b: 4.4 lezárása átírva (ST-GCN szerepe teljes detekcióvesztésnél, kiesés előtti dinamika és maszkolás, összevetés FSM-mel és LSTM/MLP-vel). 12c: Hivatkozás a 3.3. táblázat új detekcióvesztés átmenetére. 12d: Sárga TODO a szabály egyetlen videóból történő általánosításának korlátairól és a szükséges negatív tesztekről. |
| **13a-d. Belső mérési konzisztencia (5.1, 5.2)** | **Elvégezve** | 13a: Az 5.1. táblázat alá sárga TODO elhelyezve a járókeretes $T_{impact}$ (15,48 s vs. 15,72 s) ellentmondásról és újraannotálásáról. **A táblázat mért számai a 0.3 szabály szerint változatlanok maradtak!** 13b: 5.2.1-ben a késleltetési verifikáció átírva (0,48 s-nál kisebb értékek oka, egységes annotálási TODO). 13c: $T_{impact}$ szemrevételezéses annotációs nehézsége TODO. 13d: Külön fejlesztői és teszthalmaz képzésének TODO-ja. |
| **14. Wilson-CI javítása (5.2. táblázat)** | **Elvégezve** | Az 5.2. táblázat *Pontosság (Accuracy)* sorában a 10/10 esethez tartozó 95%-os Wilson konfidenciaintervallum alsó határa javításra került: **`[72,2%; 100,0%]`** (a korábbi hibás `67,9%` helyett, az egzakt $n/(n+z^2) = 10/(10+1,96^2) = 10/13,8416 = 72,246\%$ képlet alapján). A dokumentum teljes szövegében minden más `67,9` előfordulás ellenőrizve és javítva. A többi mért intervallum változatlan maradt. |
| **15a-c. Profilozás és H4 értékelés (5.3)** | **Elvégezve** | 15a: 5.3.1-be bekerült a megjegyzés, hogy a mérés GUI-renderelést tartalmaz (1,05 ms); a headless mérés SZD2 feladat. 15b: Az 5.3. táblázat alá sárga TODO került a nyers logok csatolásáról és a komponens-szintű összegek (35,10 és 46,60 ms) mért vs. számolt jelöléséről. **A táblázat mért számai változatlanok maradtak!** 15c: 5.3.3-ban kiegészült a H4 formális kritériuma (átlag $\le 40\text{ ms}$, p95 megadásával). |
| **16. GUI fejezet pontosítása (5.4)** | **Elvégezve** | Az 5.4 fejezet elejére bekerült az új bekezdés, miszerint a Tkinter GUI fejlesztői/demonstrációs eszköz (nyers képet mutat), adatvédelmi éles üzemben nem futtatható, kiegészítve a csak csontvázat mutató adatvédelmi nézet megtervezésére vonatkozó sárga TODO-val. |
| **17. Új 5.5 Előzetes ST-GCN kísérlet fejezet** | **Elvégezve** | Új Heading 2 alfejezetként beillesztésre került az **5.5 Előzetes ST-GCN és baseline kísérlet**, alatta a konzulens által kért sárga kitöltési TODO-val, valamint az **5.4. táblázat: Előzetes eredmények (nincs mérés)** üres eredménycellákkal (—) az FSM, LSTM/MLP baseline, ST-GCN és Hibrid modellekre. |
| **18a-j. Raspberry Pi fejezet korrekciói (6.)** | **Elvégezve** | 18a: Stretch goal (opcionális célkitűzés) jelölés a bevezetőben. 18b: [2, 8, 15] hivatkozások törölve a 6.2.2-ből, szerzői becslésként jelölve, Ultralytics benchmark TODO-val. 18c: A 6.1. táblázat Pi-oszlopaiban az *„(Irodalmi becslés)”* cserélve *„(szerzői becslés, nem mért)”* szövegre. 18d: LPDDR4 sávszélesség ellenőrzési TODO (12,8 GB/s). 18e: YOLOv8 mAP és GFLOPs egyeztetési TODO, és a törzsi pontok hipotézisének pontosítása. 18f: NEON regiszterek javítva: AArch64 módban 32 db 128 bites regiszter (V0–V31). 18g: 6.1-ből a *„visszavonhatatlanul”* törölve, Python fizikai memóriafelülírási korlát rögzítve. 18h: UPS üzemidő mérendőként jelölve, mikroszekundumos késleltetés törölve, sziréna tervezettként jelölve. 18i: JSON adatcsomag előtt jelölve: *„Illusztratív példa; az értékek nem mérési eredmények.”* 18j: Frame skipping időalapú ablakkezelési feltétele rögzítve a 6.3 végén. |
| **19a-d. Kísérleti terv és ütemterv (7.)** | **Elvégezve** | 19a: Hat célkitűzésre bővítve, beillesztve a **2. Nem gráf alapú tanult baseline (LSTM/MLP)** pont, Leave-one-scene-out (LOSO) 4-helyszínes Le2i és cross-dataset URFD protokoll, ablációs mátrix kiegészítés, Raspberry Pi opcionálissá tétele. 19b: 7.2-ben bevezető bekezdés az M0 előzetes feladatokról, a **7.1. táblázat** 14 hetes ütemterve maradéktalanul lecserélve a konzulens által kért heti bontásra (tartalékhéttel). 19c: A **7.2. táblázat** kockázati mátrixába bekerült a K2 frame skipping kiegészítés, az új **K6 (kevés ADL tanítóminta)** és **K7 (határidő-csúszás)** sorok B-tervekkel. 19d: A 7.4 fejezet kiegészült a 7 db részletes módszertani ponttal (Felosztás, Képkockasebesség, Kiértékelési szint, Mintaméret Rule of Three $N \ge 60\text{--}75$, Független segédeszközös halmaz TODO, Statisztika McNemar, Baseline-ok). |
| **20a-d. Hivatkozások és irodalomjegyzék** | **Elvégezve** | 20a: A szövegközi hivatkozások egységesen számozott alakra lettek hozva (pl. WHO [5], Wild [6], Tinetti [7], OpenPose [12], GDPR [13], COCO [14], YOLOv8-Pose [2], ST-GCN [1], URFD [3], Le2i [4]). 20b: Az irodalomjegyzék végére felvételre került a három új sárga TODO tétel: **[16]** Eurostat/KSH forrás, **[17]** Cowley golden hour forrás, **[18]** Keskes & Noumeir (2021) ST-GCN esésdetektálás. 20c-d: Szövegben nem hivatkozott tételek vizsgálata dokumentálva (lásd 3. fejezet). |
| **21. Kivonat kiegészítése** | **Elvégezve** | A Kivonat utolsó előtti mondata elé beillesztésre került az új baseline-összehasonlító mondat, és a kulcsszavak listája kiegészült az *„LSTM baseline”* kifejezéssel. |
| **22. Tartalom és sorszámozás összehangolása** | **Elvégezve** | A beszúrt táblázatok sorszámozása harmonizálásra került: a 3.2-ben beszúrt táblázat a **3.4. táblázat** azonosítót kapta (elkerülve a meglévő 3.1., 3.2., 3.3. átnevezési zavarát), az 5.5-ben lévő táblázat az **5.4. táblázat** sorszámot kapta. A szövegközi kereszthivatkozások ellenőrizve lettek. |

---

## 2. A dokumentumba beillesztett sárga `[TODO]` bejegyzések teljes listája

A konzulensi értékelés és a 0.2-es alapszabály szigorú betartásával minden olyan adat, amely szerzői döntést, kód-egyeztetést vagy eredeti forrásadatot igényel, sárga kiemeléssel (`<w:highlight w:val="yellow"/>`) került beillesztésre. A szerző feladata a szakdolgozat véglegesítése előtt ezek kitöltése vagy törlése:

| # | Hely / Fejezet | Pontos [TODO] szöveg | Szerzői teendő |
| :---: | :--- | :--- | :--- |
| **1.** | 1.1 Társadalmi kontextus | `[TODO: pontos érték és forrás (Eurostat előrejelzési tábla) megadandó, hivatkozással.]` | Megkeresni az Eurostat hivatalos demográfiai előrejelzési táblázatát a 65+ arányra 2050-re, és beírni az [16] tételbe. |
| **2.** | 1.1 Társadalmi kontextus | `[TODO: a 80 év felettiekre vonatkozó arány ellenőrzendő a WHO [5] kiadványban, oldalszámmal.]` | Ellenőrizni a WHO Step Safely (2021) jelentésben a 80+ évesek 40%-os elesési arányának oldalszámát. |
| **3.** | 1.2 Orvosi kontextus | `[TODO: hivatkozás]` | Megadni R. Adams Cowley eredeti Golden Hour publikációjának bibliográfiai adatait az [17] tételhez. |
| **4.** | 1.5 Hipotézisek (H2) | `[TODO: a 10 százalékpontos célérték a konzulenssel egyeztetendő.]` | Konzulensi megerősítés kérése, hogy maszkolt szekvenciákon a 10 százalékpontos Recall-előny reális-e. |
| **5.** | 1.5 Hipotézisek (H3) | `[TODO: a küszöbök egyeztetendők. Megjegyzés: a prototípus szintmodelljének ismert hamis negatív kockázata a 4.3. fejezetben dokumentált.]` | Konzulensi jóváhagyás a 2 százalékpontos FPR és a szintmodell távoli FN hibájának elfogadására. |
| **6.** | 1.5 Hipotézisek (H5) | `[TODO: célérték egyeztetendő.]` | Konzulensi egyeztetés az ST-GCN vs. Bi-LSTM 3 százalékpontos F1 különbségének elvárásáról. |
| **7.** | 1.6 Hatókör és korlátok | `[TODO: szerző: erősítse meg, hogy a prototípus egy személyt feltételez; többszemélyes jelenetnél a személykövetés (track ID) és a kiválasztás nincs megoldva.]` | Szerzői megerősítés, hogy a jelenlegi pipeline single-person feltételezéssel fut. |
| **8.** | 2.2 Kinematika ($v_y$) | `[TODO: szerző: ellenőrizd a kóddal az y_CoM definícióját és a küszöbök mértékegységét.]` | Összevetni a `simple_fall_detector.py` és a telemetriai script képletét a szövegbeli definícióval. |
| **9.** | 2.2. táblázat ($N_{mem}$) | `[TODO: az első prototípus 1,5 s-os zuhanási memóriát használt; ellenőrizendő, hogy 12 képkocka (0,48 s) a jelenlegi érték.]` | Tisztázni a kódban, hogy a drop memory időablaka pontosan hány képkocka (12 frame = 0,48 s). |
| **10.** | 2.3. táblázat (Yan et al.) | `[TODO: ellenőrizendő az eredeti cikkben]` | Megerősíteni Yan et al. (2018) cikkében a 81,5% CS és 88,3% CV NTU-RGB+D pontosságot. |
| **11.** | 2.5 fejezet (Related Work) | `[TODO: a táblázat többi eredménymutatóját (Rougier, Foroughi, Kwolek) az eredeti cikkekből ellenőrizni; az adatbázis és a protokoll eltérhet.]` | Eredeti publikációkból ellenőrizni a 2.3. táblázat régebbi sziluettalapú számait. |
| **12.** | 2.5 fejezet (Versenytársak) | `[TODO: legalább 3–5 ilyen munka felkutatása, összehasonlítása és a saját munka elhatárolása (pl. ST-GCN-es esésdetektálás: Keskes & Noumeir, IEEE Access, 2021 – a bibliográfiai adatok ellenőrizendők).]` | 3–5 korszerű csontvázalapú esésdetektáló cikk (köztük Keskes & Noumeir 2021) beemelése a szövegbe. |
| **13.** | 3.2 fejezet (3.4. táblázat) | `[TODO: szerző: erősítse meg, hogy a 3.4. fejezet automatája megegyezik-e a kóddal]` | Tisztázni a témavezető felé, hogy az 5 állapotú FSM megegyezik-e a repóban lévő kóddal. |
| **14.** | 3.2 fejezet (3.4. táblázat) | `[TODO: szerző: megvalósítva vagy tervezett?]` | AlertDispatcher státuszának rögzítése (jelenleg a HUD rajzol ki és konzolra ír, nincs MQTT daemon). |
| **15.** | 3.4 fejezet (FSM leírás) | `[TODO: szerző: az itt leírt öt állapotú automata (NORMAL/UNSTABLE/FALLING/FALLEN/RECOVERED) a megvalósított kód vagy az átdolgozott terv? Az első prototípus állapotai NORMAL/WARNING/DROP_DETECTED/FALLEN voltak, 1,5 s zuhanási memóriával. Az eltérést indokolni vagy megszüntetni kell.]` | A konzulensi kérdés hivatalos megválaszolása a dolgozat szövegében. |
| **16.** | 3.3. táblázat (FSM tranzíciók) | `[TODO: a rest_ratio változó definíciója hiányzik]` | Beírni a képletet: $\text{rest\_ratio} = (H_{\text{torso}} / W_{\text{torso}}) < 1,1$. |
| **17.** | 3.3. táblázat (Detekcióvesztés) | `[TODO: kóddal egyeztetni]` | Ellenőrizni, hogy a kód azonnal FALLEN-be vált-e, vagy vár 8–10 képkocka kiesést. |
| **18.** | 3.5 fejezet (Hibrid fúzió) | `[TODO: szerző: a leképezés megerősítendő vagy kalibrálandó]` | Megerősíteni a diszkrét FSM szintek (1,0 / 0,5 / 0,0) vagy a folytonos szigmoid leképezés alkalmazását. |
| **19.** | 4.4 fejezet (Járókeret takarás) | `[TODO: egyetlen videó alapján a szabály általánosítása nem igazolt; negatív esetek (a képből gyorsan kilépő vagy takarás mögé leülő személy) tesztelendők.]` | Jelezni a SZD2 kísérleti tervben a gyors kilépések és takarásos leülések tesztelését. |
| **20.** | 5.1 fejezet (Kalibráció) | `[TODO: a Szakdolgozat 2-ben külön fejlesztői és teszthalmaz szükséges: a küszöbhangolás a fejlesztői szeleten történik, a teszt-szeletet egyszer értékeljük ki.]` | Rögzíteni a kísérleti protokoll szigorú adatszétválasztását. |
| **21.** | 5.1 fejezet (5.1. táblázat alatt) | `[TODO: Independent-02: a T_impact (15,48 s) ellentmond a 4.1. táblázatnak (stabil járás 15,60 s-nál, zuhanás 15,68 s-tól, becsapódás a 393. képkockán = 15,72 s). A T_impact újraannotálandó, és a hozzá tartozó T_latency, valamint az 5.2.1 statisztikái ennek megfelelően frissítendők.]` | Újraannotálni a járókeretes videó földet érési pillanatát (15,72 s), és átszámolni az 5.1–5.2 statisztikákat. |
| **22.** | 5.2.1 fejezet (Késleltetés) | `[TODO: ez szemmel nehezen annotálható; operacionális definíció (pl. első talajérintés képkockája) szükséges.]` | Formális definíció rögzítése a videók földet érési képkockájának kijelölésére. |
| **23.** | 5.2.1 fejezet (Késleltetés) | `[TODO: a T_impact annotálását egységesíteni kell (Le2i: annotációs fájlok fall start/end; URFD: szenzor- és mélységadat), és dokumentálni, ki és hogyan annotálta.]` | Leírni a két benchmark adatbázis hivatalos földet érési időbélyegeinek kinyerési módját. |
| **24.** | 5.3 fejezet (5.3. táblázat alatt) | `[TODO: a nyers mérési napló és a mérőscript csatolandó (reprodukálhatóság). Az összesített min/max értékek pontosan megegyeznek a komponensek min/max értékeinek összegével (35,10 ms; 46,60 ms); ellenőrizendő, hogy ezek mért vagy számolt értékek. Utóbbi esetben jelölni kell.]` | Mellékelni a profilozó Python scriptet és a nyers 1500 képkockás CSV időmérési logot. |
| **25.** | 5.4 fejezet (GUI) | `[TODO: szerző: tervezz adatvédelmi nézetet, amely csak a csontvázat jeleníti meg.]` | Tervezni egy Privacy HUD módot, ahol fekete háttéren csak a 2D vonalas csontváz látható. |
| **26.** | 5.5 fejezet (Előzetes kísérlet) | `[TODO: szerző: tölts ki eredménnyel, ha a Szakdolgozat 1 hátralévő idejében elkészül a kulcspontkinyerés és egy előzetes ST-GCN/LSTM futás. Adatkészlet, felosztás (videó szerint!), modell, metrikák leírandók. Ha nem készül el, ez a fejezet törlendő.]` | Beírni az 5.4. táblázatba a repóban meglévő `train_stgcn_fall.ipynb` modell előzetes teszteredményeit. |
| **27.** | 6.2.1 fejezet (LPDDR4) | `[TODO: ellenőrizendő; a 32 bites LPDDR4-3200 elméleti sávszélessége ~12,8 GB/s]` | Ellenőrizni a BCM2711 LPDDR4 memóriavezérlő elméleti busz-sávszélességét. |
| **28.** | 6.2.2 fejezet (Becslések) | `[TODO: az Ultralytics Raspberry Pi benchmarkja [2] alapján ellenőrizni, és csak a ténylegesen megadott értéket idézni]` | Megkeresni az Ultralytics hivatalos Pi 4B/5 benchmark táblázatát, és csak a publikált FPS-t hivatkozni. |
| **29.** | 6.3.1 fejezet (mAP értékek) | `[TODO: a számokat az Ultralytics hivatalos táblázatával egyeztetni (a v8s-pose mAP-ja és GFLOPs értéke eltérhet)]` | Ellenőrizni a COCO Pose hivatalos mAP50-95 számait (v8s: 60,0 mAP, v8n: 50,4 mAP). |
| **30.** | 7.1 fejezet (Focal Loss) | `[TODO: a választás indoklása; osztályarányok megadandók]` | Leírni az esés/ADL ablakok aszimmetriáját (pl. 1:10 arány) és emiatt a Focal Loss $\gamma$ paraméterét. |
| **31.** | 7.4 fejezet (Képkockasebesség) | `[TODO: ellenőrizendő]` | Ellenőrizni a Le2i (25 FPS) és az URFD (30 FPS RGB, 30 FPS depth) natív mintavételi frekvenciáit. |
| **32.** | 7.4 fejezet (Segédeszköz halmaz) | `[TODO: a 15 járókeretes/mankós videó forrása, licence és annotációja megadandó. Jelenleg egyetlen ilyen felvétel áll rendelkezésre.]` | Rögzíteni a SZD2-ben rögzítendő 15 fős etikai/GDPR protokollos segédeszközös adatbázis tervét. |
| **33.** | Irodalomjegyzék [16] | `[TODO: Eurostat / KSH forrás a 65 év feletti arányhoz]` | Pontos statisztikai hivatkozás beillesztése. |
| **34.** | Irodalomjegyzék [17] | `[TODO: Cowley, golden hour – forrás]` | Pontos orvosi traumatológiai hivatkozás beillesztése. |
| **35.** | Irodalomjegyzék [18] | `[TODO: Keskes & Noumeir, ST-GCN-es esésdetektálás – ellenőrzött bibliográfiai adatok]` | Teljes IEEE Access bibliográfiai tétel beillesztése. |

---

## 3. Hivatkozási Audit és Szövegközi Elemzés (20c–d feladatok)

Az irodalomjegyzék és a folyószöveg közötti konzisztenciavizsgálat eredményei:

- **Hivatkozott és egyeztetett források a szövegben:**  
  `[1]` Yan et al. (ST-GCN, 2.3, 7.1)  
  `[2]` Ultralytics YOLOv8 (2.1.1, 6.2.2)  
  `[3]` Kwolek & Kepski (URFD, 1.1, 2.5, 5.2.1)  
  `[4]` Charfi et al. (Le2i, 1.1, 2.5, 5.2.1)  
  `[5]` WHO jelentés (1.1)  
  `[6]` Wild et al. (1.2)  
  `[7]` Tinetti et al. (1.2)  
  `[9]` ONNX Runtime (3.1.2, 7.1)  
  `[10]` Rougier et al. (2.5)  
  `[11]` Foroughi et al. (2.5)  
  `[12]` Cao et al. / OpenPose (2.1.1, 2.5)  
  `[13]` GDPR 2016/679 (2.4)  
  `[14]` Lin et al. / MS COCO (2.1.2)  

- **Szövegben nem hivatkozott tételek vizsgálata (20c feladat):**  
  - **`[8]` Intel OpenVINO:** A korábbi változatban a 6.2.2-ben szerepelt a `[2, 8, 15]` csoportban. A 18b feladat törölte ezt a hibás hivatkozási csoportot, mivel az OpenVINO x86-specifikus eszköz és nem Raspberry Pi benchmark. Jelenleg a szövegben **nem hivatkozott**. *Javaslat a szerzőnek: törlendő az irodalomjegyzékből, vagy a 6.3 fejezetben az x86 asztali optimalizációknál hivatkozandó.*  
  - **`[15]` ARM Cortex-A Programmer's Guide:** A 6.3.3-ban a NEON SIMD leírásnál szerepel a technológia, de a közvetlen `[15]` számozott hivatkozás kikerült a 18b pontosítás során. *Javaslat a szerzőnek: a 6.3.3 bekezdésben expliciten hivatkozandó a NEON architektúra leírásánál.*  

---

## 4. Ellenőrzési és Minőségbiztosítási Eredmények (23. feladat)

1. **Formátum és Margók:** A4 formátum, szabályzat szerinti margók (bal: 3,5 cm, jobb: 2,5 cm, fent: 2,5 cm, lent: 2,5 cm). Hasznos szövegszélesség: 5,91 inch (~15,0 cm). Minden táblázat maximális szélessége 5,85 inch (0 túlcsordulás).  
2. **Tipográfia:** Times New Roman alapszöveg, 11 pt, 1,35 sorköz, sorkizárt igazítás.  
3. **Dupla felsorolásjelek:** Megszűntek; a listák tiszta függő behúzással és egyedi bullet szimbólummal rendelkeznek.  
4. **Wilson konfidenciaintervallum:** A javított `[72,2%; 100,0%]` érték szerepel az 5.2. táblázatban, a szövegben hibás `67,9%` nem található.  
5. **Mért számok integritása:** A mérési táblázatokban (4.1, 5.1, 5.3) szereplő empirikus adatok a 0.3 szabálynak megfelelően érintetlenek maradtak; az ellentmondásokat és reprodukálhatósági kérdéseket sárga TODO tételek jelzik.  
6. **Beágyazott ábrák:** Mind a 8 db nagyfelbontású (300 DPI) szakmai ábra hiánytalanul beágyazva található a dokumentumban.  
