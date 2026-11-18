# Változásnapló: Szakdolgozat 1 – v4 Dokumentum Javítások

**Dátum:** 2026. november 17.
**Bemeneti forrás (v2):** `szakdolgozati_kutatasi_terv_frissitett.docx`
**Szerkesztendő kiindulás (v3):** `szakdolgozati_kutatasi_terv_v3.docx`
**Kimeneti javított dokumentum (v4):** `szakdolgozati_kutatasi_terv_v4.docx`

---

## 1. Feladatonkénti állapot és módosítások összefoglalója (F0 – F19)

| Feladat | Státusz | Változás leírása |
| :--- | :---: | :--- |
| **F0: Előellenőrzés** | **Elvégezve** | A v2 és v3 összehasonlítva: mindkettőben pontosan 8 db kép van (`image1`..`image8`), a fejléc (`Szakdolgozat 1 – Kutatási és Rendszertervezési Terv / Széchenyi István Egyetem`) és lábléc (`- PAGE -`) azonos. A margók és stílusok ellenőrizve. |
| **F1: Címlap visszaállítása** | **Elvégezve** | Hivatalos főcím megtartva; típus javítva (`SZAKDOLGOZAT 1 – KUTATÁSI ÉS FEJLESZTÉSI TERV`); aláírótábla bal cellájából törölve a „Nappali tagozat”, jobb cellájából törölve a „Konzulens Oktató”, „mesteroktató”, „Informatika Tanszék” (v2 állapot). |
| **F2: Kivonat** | **Elvégezve** | A 3. bekezdésben az „és indokolja az ST-GCN hálózatok szükségességét” kicserélve erre: „és felveti az ST-GCN hálózatok alkalmazásának szükségességét”. Az LSTM baseline kulcsszó megtartva. |
| **F3: 1.1 Fejezet** | **Elvégezve** | A három demográfiai felsorolás-pont visszaállítva a v2-ből a kért javításokkal (WHO [5] és forrás TODO-kkal); a nem forrásolt „Sérülési súlyosság” és „Pszichológiai trauma” pontok törölve; Eurostat TODO végére fűzve: `→ hivatkozás: [16]`. |
| **F4: 1.2 Fejezet** | **Elvégezve** | Teljes újraépítés a v2 alapján: Cowley Golden Hour [17] analógiás kontextusban, Wild [6] és Tinetti [7] megfigyeléses kockázati markerként; 3 pont: Hipotermia, Rhabdomyolysis, Dekubitusz; kamrafibrilláció és 6–12 órás irreverzibilitás törölve. |
| **F5: 1.5 Fejezet (RQ2, RQ3)** | **Elvégezve** | Az RQ2 és RQ3 szövege szinkronizálva a hipotézisekkel: RQ2 említi a szabályalapú memóriát és ST-GCN-t; RQ3 említi a pozíció- és skálacsatornákkal kiegészített ST-GCN-t. H2 és H3 TODO-k tiszta, nem félkövér sárga kiemelést kaptak. |
| **F6: 2.1 és 2.1.1 Fejezet** | **Elvégezve** | 2.1 bevezető bekezdése visszaállítva a v2-ből; 2.1.1-be beszúrva az osztályozó mondat; az 1. Top-down (AlphaPose, HRNet) és 2. Bottom-up (OpenPose PAF [12]) pontok szövege szigorúan a v2 szerint visszaállítva. |
| **F7: 2.4 Fejezet** | **Elvégezve** | 2.4 fejezet teljes visszaállítása a v2 alapján: GDPR 25. cikk szerinti Privacy-by-Design [13], Python GC korlátai és 3 bullet: Memóriareziduumok, Puha-biometria, Hardveres védelem (memset_s, C++/Rust). |
| **F8: 3.1 Fejezet (FR-tábla)** | **Elvégezve** | Nem kért bevezető bekezdés törölve; 3.1.1 bevezető mondat javítva; 3.1. táblázat felirata és FR-01..FR-07 sorai visszaállítva a v2 szövegére; NFR-08 verifikáció átírva „opcionális 6. célkitűzés”-re. |
| **F9: 3. Fejezet táblázatszámozás** | **Elvégezve** | Táblázatok sorba rendezve: Komponens-státusz = 3.3. táblázat, FSM-tranzíció = 3.4. táblázat. Kereszthivatkozások javítva a 3.2, 3.4 és 4.4 fejezetekben; a 3.3. ábra és 3.4. ábra hivatkozások érintetlenek maradtak. |
| **F10: FSM-táblázat javítása** | **Elvégezve** | A 3.4. táblázat utolsó sorának feltétele logikailag javítva (zuhanási memóriás UNSTABLE vagy FALLING állapot); időzítéshez beszúrva a prototípus időkorlát TODO-ja; táblázat után beszúrva a 25 FPS-es képkocka–másodperc átszámítási bekezdés. |
| **F11: 3.5 Fejezet pontosítása** | **Elvégezve** | Kitakarás definíciója egyetlen képkockára korlátozva (c > 0,3 és N < 12) + hangolási TODO; DropGraph maszkolásnál az első 4 képkocka érvényes marad + hangolási TODO. |
| **F12: 5. Fejezet visszaállítása** | **Elvégezve** | 5. bevezető bekezdése cserélve; 5.1 visszaállítva a v2-ből (1. Fejlesztői kalibrációs halmaz + járókeretes felvétel TODO, 2. Módszertani korlát, 3. Mintanagyság); 5.2 elé beszúrva a 3 baseline bemutatása; „YouTube” szó sehol sem szerepel; 5.1. tábla mért értékei sértetlenek; Wilson CI 72,2%. |
| **F13: 6. Fejezet visszaállítása** | **Elvégezve** | 6.2.2 6.1. táblázat sorai pontosítva (szerzői becslés címkék); utána Pi 4B vs Pi 5 összehasonlító bekezdés beszúrva; 6.3 és 6.4 teljes egészében visszaállítva a v2-ből (11.6M→3.3M paraméter, 56.0% vs 50.4% mAP, PTQ képletek Z=0, NEON [15], ONNX Runtime [9], MQTT JSON „privacy_verified” nélkül). |
| **F14: 7. Fejezet** | **Elvégezve** | 7.1 3. pontjában kezdeti α értékek és validációs hangolás rögzítve; 7.4 bevezető mondat cserélve; felsorolás elejére beszúrva a 3 új pont (Adatbázisok és megoszlásuk, Osztályozási és megbízhatósági metrikák, Hardveres metrikák); duplikált pont törölve. |
| **F15: Hivatkozások auditja** | **Elvégezve** | Ellenőrizve az első említések: URFD [3], Le2i [4], NEON [15], ONNX Runtime [9], Eurostat [16], Cowley [17], Keskes [18]. Az [8] OpenVINO nem hivatkozott tételként feljegyezve. |
| **F16: Formai javítások** | **Elvégezve** | Minden [TODO: ...] mélységszámlálóval (bracket-depth) egyetlen sárga, NEM félkövér futásként jelenik meg (kezelve az [5]-öt és [2]-t); üres záró elemek törölve; felsorolásjelek egységesek; Word TOC mező és updateFields beágyazva; Kivonat és Tartalomjegyzék stílusa Normal (nincs outlineLvl, nem kerül a TOC-ba). |
| **F17: Fogalmak összehangolása** | **Elvégezve** | „Visszavonhatatlanul” enyhítve („azonnal felszabadítja (lásd 2.4.)”); „garantálja” helyett „biztosítja” a mért átlagoknál; „lásd 2.4.” hivatkozások érvényesek. |
| **F18: Nem kért változtatások** | **Elvégezve** | Pandoc összevetés alapján a v2-höz képest kizárólag a konzulens által jóváhagyott változtatások maradtak a v4-ben. |
| **F19: Ellenőrzés és verifikáció** | **Elvégezve** | Mind a 17 tiltott kifejezés 0 találattal zárt; mind a 11 kötelező kifejezés jelen van; pontosan 8 db kép van beágyazva; a táblázatok margókon belül (<= 5.85'') maradnak. |

---

## 2. Előellenőrzési és formázási eredmények (F0.1 – F0.3)

- **F0.1 Ábrák ellenőrzése:** Mind a forrás v2 (`szakdolgozati_kutatasi_terv_frissitett.docx`), mind az új v4 dokumentum pontosan 8 darab beágyazott képet tartalmaz a `word/media/` mappában:
  * `image1.png` – 2.1. ábra: COCO-17 kulcspont-topológia
  * `image2.png` – 3.1. ábra: Rétegzett szoftverarchitektúra blokkdiagramja
  * `image3.png` – 3.2. ábra: Részletes UML osztálydiagram
  * `image4.png` – 3.3. ábra: UML szekvenciadiagram esési ciklusról
  * `image5.png` – 3.4. ábra: Véges állapotgép (FSM) tranzíciós diagramja
  * `image6.png` – 4.1. ábra: Kép szélén belépő személy peremszűrése
  * `image7.png` – 4.2. ábra: Konyhapult mögötti előrehajolás szűrése
  * `image8.png` – 5.1. ábra: Interaktív operátori és tesztelő GUI felület
- **F0.2 Formázási ellenőrzés:** A margók szigorúan szabályzat-konSearchisek: Bal margó: 3,5 cm (1,38''), Jobb, felső, alsó margók: 2,5 cm (0,98''). Hasznos szövegszélesség: 5,91'' (15,0 cm). Minden táblázat maximális szélessége 5,85'' vagy kisebb, így egyetlen táblázat sem lóg ki az oldalról.
- **F0.3 Fejléc és lábléc ellenőrzése:** A fejléc szövege pontosan megegyezik a v2 dokumentuméval: `Szakdolgozat 1 – Kutatási és Rendszertervezési Terv | Széchenyi István Egyetem`. A lábléc a szabályos `- PAGE -` dinamikus oldalszámozást tartalmazza.

---

## 3. Hivatkozások auditja és szövegbeli ellenőrzése (F15)

### 3.1 Első szövegbeli említések ellenőrzése
- **URFD [3]:** 5.1. fejezet, 1. pontban beillesztve és ellenőrizve.
- **Le2i [4]:** 5.1. fejezet, 1. pontban és 7.4. fejezetben ellenőrizve.
- **NEON [15]:** 6.3.3. fejezet bevezetésében beillesztve és ellenőrizve.
- **ONNX Runtime [9]:** 6.3.3. fejezet 1. pontjában és 7.1. fejezet 6. pontjában ellenőrizve.
- **Eurostat [16]:** 1.1. fejezet végén a demográfiai TODO-ban rögzítve (`[TODO: ... → hivatkozás: [16]]`).
- **Cowley [17]:** 1.2. fejezet elején az Arany Óra TODO-ban rögzítve (`[TODO: hivatkozás → [17]]`).
- **Keskes & Noumeir [18]:** 2.5. fejezet záró bekezdésében rögzítve (`[TODO: ... → hivatkozás: [18]]`).

### 3.2 Nem hivatkozott tételek az irodalomjegyzékben
- **[8] Intel Corporation (OpenVINO Toolkit):** A szövegtörzs jelenleg nem hivatkozik közvetlenül az OpenVINO-ra (mivel a beágyazott platform ARM-alapú, nem Intel). **Megjegyzés a szerzőnek:** a szerző döntse el a Szakdolgozat 2-ben: hivatkozás beszúrása (pl. x86_64 összehasonlításként) vagy a tétel törlése az irodalomjegyzékből.

---

## 4. Nem kért változtatások és diff-ellenőrzés (F18)

A pandoc és diff összevetés alapján minden szövegrész besorolásra került:
1. **Jóváhagyott módosítások:** Hivatalos főcím, kivonat kiegészítései és LSTM baseline kulcsszó, 1.4 státuszmondat, 1.5 új RQ/H pontok, 1.6 korlátok fejezet, 2.2 v_y definíció és másodperc-alapú határok, 2.5 related work táblázat és kiegészítések, 3.1 FR táblázat és NFR-08 javítás, 3.3 komponens-státusztábla, 3.4 FSM logika és timing TODO, 3.5 hibrid fúzió és DropGraph leírás, 4.3 és 4.4 esettanulmányi zárások, 5.1/5.2 baseline fejezet, 5.5 előzetes kísérlet fejezet, 6.1 és 6.2.2 szerzői becslés címkék és Pi 4B/5 összehasonlítás, 7.1–7.4 kiegészítések és 14 hetes ütemterv, [16]–[18] irodalomjegyzék tételek, automatikus Word TOC mező és updateFields beállítás.
2. **Visszaállított részek:** Címlap teljes szövege (Nappali tagozat, mesteroktató, stb. törölve), 1.1 demográfiai pontok (v2-re), 1.2 orvosi fejezet (v2-re), 2.1/2.1.1 pózbecslés bevezető és pontok (v2-re), 2.4 adatvédelem (v2-re), 3.1 nem kért bevezető törölve és FR sorok (v2-re), 6.3 és 6.4 architektúra és IoT fejezetek (v2-re, privacy_verified nélkül).
3. **Ellenőrizendő lista a szerző számára:**
   - *Ellenőrizendő 1:* Az URFD és Le2i videók letöltési és annotálási protokolljának véglegesítése az M1 mérföldkőre.
   - *Ellenőrizendő 2:* A távoli háttérbeli esések felismerési korlátjának empirikus vizsgálata a 4.3. fejezetben jelzett szintmodell kapcsán.
   - *Ellenőrizendő 3:* A Raspberry Pi 5 hardveres mérési programjának véglegesítése (opcionális célkitűzésként kezelve).

---

## 5. Beillesztett sárga [TODO: ...] elemek teljes nyilvántartása

Minden TODO elem szigorúan a megadott előírások szerint készült: egyetlen szövegfutás (single run), sárga háttérszínnel (`<w:highlight w:val="yellow"/>`), **nem félkövér** és **nem dőlt** betűstílussal.

| Sorszám | Fejezet / Hely | TODO szövege | Magyarázat / Szerzői teendő |
| :---: | :--- | :--- | :--- |
| 1 | 1.1 Társadalmi és egészségügyi kontextus | `[TODO: pontos hivatkozás és évszám szükséges az Eurostat demográfiai jelentéséből → hivatkozás: [16]]` | Pontos Eurostat demográfiai forrás és évszám megadása a 65 év feletti népesség arányához ([16]). |
| 2 | 1.1 Társadalmi és egészségügyi kontextus | `[TODO: a 80 év felettiekre vonatkozó arány ellenőrzendő a WHO [5] kiadványban, oldalszámmal.]` | A 80 év feletti lakosság esési arányának ellenőrzése a WHO [5] kiadványban, pontos oldalszámmal. |
| 3 | 1.1 Társadalmi és egészségügyi kontextus | `[TODO: forrás megadandó.]` | Traumatológiai forrás megadása a combnyak- és medencetörések esési arányához. |
| 4 | 1.2 Az elhúzódó földön fekvés orvosi szövődményei és a beavatkozási időablak | `[TODO: hivatkozás → [17]]` | Szerzői adatpótlás vagy konzulensi egyeztetés szükséges a Szakdolgozat 2-ben. |
| 5 | 1.5 Kutatási kérdések és hipotézisek | `[TODO: a 10 százalékpontos célérték a konzulenssel egyeztetendő.]` | A kitakarás melletti ST-GCN pontosságnövekedési célértékének konzulensi egyeztetése. |
| 6 | 1.5 Kutatási kérdések és hipotézisek | `[TODO: a küszöbök egyeztetendők. Megjegyzés: a prototípus szintmodelljének ismert hamis negatív kockázata a 4.3. fejezetben dokumentált.]` | A kanapén fekvés és háttéri esés szintmodell-küszöbeinek egyeztetése a konzulenssel. |
| 7 | 2.2 Kinematikai mozgásjellemzők és paraméterhierarchia | `[TODO: kóddal egyeztetni; az első prototípus 1,5 s-os zuhanási és 1,2 s-os figyelmeztetési időkorlátot használt.]` | Az állapotgép kódbeli időzítéseinek (drop_timer, warn_timer) és küszöbeinek ellenőrzése. |
| 8 | 2.5 Kapcsolódó munkák és szakirodalmi összehasonlítás (Related Work) | `[TODO: Keskes & Noumeir pontos hivatkozás és publikációs adatok hozzáadandók → hivatkozás: [18]]` | Keskes & Noumeir publikáció pontos adatainak megadása az irodalomjegyzék [18] tételéhez. |
| 9 | 3.4 A döntési állapotgép (Finite State Machine - FSM) működése | `[TODO: rest_ratio ellenőrzendő]` | Szerzői adatpótlás vagy konzulensi egyeztetés szükséges a Szakdolgozat 2-ben. |
| 10 | 3.4 A döntési állapotgép (Finite State Machine - FSM) működése | `[TODO: kóddal egyeztetni; az első prototípus 1,5 s-os zuhanási és 1,2 s-os figyelmeztetési időkorlátot használt.]` | Az állapotgép kódbeli időzítéseinek (drop_timer, warn_timer) és küszöbeinek ellenőrzése. |
| 11 | 3.5 Hibrid döntési mechanizmus: A Kinematikai FSM és az ST-GCN integrációja | `[TODO: a 0,3 és a 12 kezdeti érték, hangolandó.]` | A látható kulcspontok konfidencia- és darabszám-küszöbének hangolása a validációs halmazon. |
| 12 | 3.5 Hibrid döntési mechanizmus: A Kinematikai FSM és az ST-GCN integrációja | `[TODO: a 4 értéke hangolandó]` | A DropGraph maszkolásnál az érvényes kezdeti képkockák számának kísérleti hangolása. |
| 13 | 4.3 Peremeset 3: Kanapén elterülés és a szintmodell biztonsági korlátai | `[TODO: a távoli esések hamis negatív kockázatát részletesen validálni kell a Le2i és URFD háttéri esési szekvenciáin a Szakdolgozat 2-ben.]` | A szintmodell távoli esésekre vonatkozó korlátjának mérése Le2i és URFD videókon. |
| 14 | 5.1 Módszertani keretek és a fejlesztői teszthalmaz korlátai | `[TODO: szerző: a járókeretes felvétel forrása, licence és hozzáférhetősége.]` | A járókeretes saját tesztvideó pontos forrásának, licencének és elérhetőségének megadása. |
| 15 | 5.1 Módszertani keretek és a fejlesztői teszthalmaz korlátai | `[TODO: a Szakdolgozat 2-ben külön fejlesztői és teszthalmaz szükséges; az 5.1. táblázat jelenleg fejlesztői kalibrációs eredményeket mutat, nem független tesztet.]` | A Szakdolgozat 2-ben megvalósuló független Leave-One-Scene-Out teszthalmaz kialakítása. |
| 16 | 5.1 Módszertani keretek és a fejlesztői teszthalmaz korlátai | `[TODO: az Independent-02 felvétel pontos leírása és metaadatai pótolandók a jegyzőkönyv alapján.]` | A belépési tesztvideó metaadatainak és mérési jegyzőkönyvének pótlása. |
| 17 | 5.5 Előzetes ST-GCN és baseline kísérlet | `[TODO: az előzetes ST-GCN modell tanítási jegyzőkönyve, validációs pontossága és konvergenciagörbéje a szerző által beillesztendő az M1 mérföldkő lezárásakor.]` | Az előzetes ST-GCN kísérlet tanítási görbéjének és validációs pontosságának rögzítése. |
| 18 | 6.2 Hardverplatform-elemzés és összehasonlítás | `[TODO: a táblázat Pi-adatai szerzői becslések, mérés a Szakdolgozat 2-ben.]` | A Raspberry Pi 5 és Pi 4B becsült értékeinek felváltása fizikai mérési eredményekkel. |
| 19 | 6.3 Modelloptimalizációs technikák beágyazott környezetben | `[TODO: a számokat az Ultralytics hivatalos táblázatával egyeztetni (a GFLOPs értékek eltérhetnek).]` | A YOLOv8s és YOLOv8n paraméterszámának, GFLOPs-ának és mAP-jának egyeztetése az Ultralytics táblázattal. |
| 20 | 6.3 Modelloptimalizációs technikák beágyazott környezetben | `[TODO: a mAP-értékeket az Ultralytics hivatalos táblázatával egyeztetni (a v8s-pose mAP-ja eltérhet).]` | A YOLOv8s és YOLOv8n paraméterszámának, GFLOPs-ának és mAP-jának egyeztetése az Ultralytics táblázattal. |
| 21 | 7.4 Nagymintás kísérleti és validációs protokoll | `[TODO: a segédeszközös videók forrása, licence és annotációja megadandó; jelenleg egyetlen ilyen felvétel áll rendelkezésre.]` | Szerzői adatpótlás vagy konzulensi egyeztetés szükséges a Szakdolgozat 2-ben. |
| 22 | Irodalomjegyzék | `[TODO: Eurostat / KSH forrás a 65 év feletti arányhoz]` | Pontos Eurostat demográfiai forrás és évszám megadása a 65 év feletti népesség arányához ([16]). |
| 23 | Irodalomjegyzék | `[TODO: Cowley, golden hour – forrás]` | Cowley traumatológiai Arany Óra publikációjának bibliográfiai hivatkozása ([17]). |
| 24 | Irodalomjegyzék | `[TODO: Keskes & Noumeir, ST-GCN-es esésdetektálás – ellenőrzött bibliográfiai adatok]` | Keskes & Noumeir publikáció pontos adatainak megadása az irodalomjegyzék [18] tételéhez. |

---

## 6. Verifikációs ellenőrzőlista (F19)

- [x] **F19.1 Séma- és XML-validáció:** A Word dokumentum struktúrája és XML elemei hibátlanok.
- [x] **F19.2 Táblázatok és tördelés:** Valamennyi táblázat maximális szélessége <= 5,85'' (a margók közötti hasznos tér 5,91''). Egyetlen oszlop sem csúszik ki az oldalról. A sorok cantSplit védelemmel vannak ellátva, így oldalhatáron nem törnek meg hibásan. A fejléc minden oldalon ismétlődik (tblHeader).
- [x] **F19.3 Képek száma:** Pontosan 8 darab beágyazott ábra található a dokumentumban (2.1., 3.1., 3.2., 3.3., 3.4., 4.1., 4.2., 5.1. ábra).
- [x] **F19.4 Tiltott kifejezések ellenőrzése:** Mind a 17 tiltott kifejezés („YouTube”, „kamrafibrill”, „Kiszáradás”, „poszt-esési”, „6–12 órán”, „11,2 millió”, „24 MB”, „privacy_verified”, „Nappali tagozat”, „mesteroktató”, „RENDSZERTERVEZÉSI”, „67,9”, „frame^-1”, „frame⁻¹”, „opcionális 5. célkitűzés”, „Képkivágás”, „Konzulens Oktató”) ellenőrizve, előfordulásuk száma: **0**.
- [x] **F19.5 Kötelező kifejezések ellenőrzése:** Valamennyi kötelező kifejezés jelen van a szövegben:
  * `SZAKDOLGOZAT 1 – KUTATÁSI ÉS FEJLESZTÉSI TERV`
  * `Gráf alapú modellek detektálása vizuális információn`
  * `Egyetemi Adjunktus / Konzulens`
  * `72,2%` (Wilson konfidencia-intervallum)
  * `szerzői becslés, nem mért`
  * `RQ5` és `H5`
  * `1.6 Hatókör és ismert korlátok`
  * `5.5 Előzetes ST-GCN és baseline kísérlet`
  * `Naiv kinematikai baseline`
  * `Adatbázisok és megoszlásuk`
- [x] **F19.6 Tartalomjegyzék mező:** Word TOC mező (`TOC \o "1-3" \h \z \u`) beágyazva, `<w:updateFields w:val="true"/>` beállítva. A TOC-t Wordben megnyitáskor frissíteni kell.