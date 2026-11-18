Szakdolgozati kutatási vázlat (BSc)

Verekedés-megelőzés szórakozóhelyeken váz-alapú viselkedéselemzéssel (YOLOv8-Pose, ST-GCN, PyTorch)

A téma lényege

Probléma: a biztonsági őrök nem tudnak egyszerre minden kamerát figyelni, és a verekedést gyakran csak utólag veszik észre. A cél a korai figyelmeztetés: jelezni, ha egy jelenet verekedéssé fajulhat vagy már az.

Megoldási ötlet: a kamerakép helyett csak az emberek vázát (ízületi pontjait) elemezzük. Ez gyorsabb, és adatvédelmi szempontból is előnyösebb, mert nem kell arcokat tárolni.

Pipeline: videó → YOLOv8-Pose (kulcspontok) → követés (ki kicsoda a képkockák között) → ST-GCN (mozgásosztályozás) → riasztás a biztonsági őrnek.

Osztályok (javaslat): 1) normál viselkedés (beleértve a táncot), 2) feszült helyzet (lökdösődés, vita), 3) verekedés. Ha szűkös az idő, elég a kétosztályos változat (verekedés / nem verekedés).

Kutatási kérdések

1. Mennyire megbízhatóan különíti el az ST-GCN a verekedést a normál mozgástól és a tánctól?

2. Jobb-e az ST-GCN egy egyszerűbb módszernél (például ízületi szögek + Random Forest)?

3. Elég gyors-e a teljes rendszer valós idejű működéshez, és mennyi a téves riasztás?

Mi tartozik bele, mi nem

Benne van: meglévő YOLOv8-Pose modell használata, ST-GCN betanítása, kiértékelés, egyszerű valós idejű demó.

Nincs benne: arcfelismerés, hanganalízis, saját pózbecslő tanítása, éles üzemi telepítés.

1. Kutatandó altémák és technológiák

1.1 Altémák (ebben a sorrendben érdemes haladni)

Verekedés-/erőszakfelismerés áttekintése: milyen módszerek léteznek (RGB-alapú, váz-alapú), milyen adathalmazokkal és milyen pontossággal.

Pózbecslés YOLOv8-Pose-zal: mit ad vissza (17 kulcspont, pozíció + megbízhatóság), hogyan menthető videóból, mik a hibaforrásai (takarás, rossz fény).

Többszemélyes követés: az Ultralytics beépített követője (BoT-SORT, ByteTrack) azonosítót ad minden embernek, így egy személy vázsorozata összefűzhető.

Gráfok és ST-GCN alapok: a váz mint gráf (ízület = csúcs, csont = él), a térbeli és időbeli konvolúció alapötlete, a szomszédsági mátrix.

Adat-előkészítés: koordináták normalizálása, fix hosszúságú időablakok (pl. 32–64 képkocka), hiányzó pontok kezelése, adatbővítés.

Tanítás és kiértékelés: train/validation/test felosztás, pontosság, precision, recall, F1, konfúziós mátrix, téves riasztás óránként, riasztási késleltetés.

1.2 Szórakozóhely-specifikus nehézségek (a dolgozat egyik fő témája)

Tánc és verekedés összekeverése: a gyors, nagy mozdulatok mindkettőben megjelennek, ezért a tánc „nehéz negatív példa”.

Tömeg és takarás: sok ember van közel egymáshoz, a pózbecslő pontjai elcsúsznak vagy eltűnnek.

Gyenge, villogó fény: rontja a pózbecslést, ezt külön tesztelni kell.

Kamerahelyzet: magasról, ferdén néző kamerák torzítják a vázat (egy friss vizsgálatban ez volt a legnehezebb eset).

Korai jelzés: a lökdösődés gyakran a verekedés előjele, ezért érdemes külön osztályként kezelni.

1.3 Eszközök

Eszköz

Mire használjuk

Python, PyTorch

ST-GCN modell és tanítás

Ultralytics (YOLOv8-Pose)

kulcspont-kinyerés és követés videóból

OpenCV

videó beolvasása, megjelenítés, demó

PYSKL vagy MMAction2

kész ST-GCN referencia-implementáció összehasonlításhoz

PyTorch Geometric (opcionális)

saját gráfréteg, ha marad idő

Google Colab / Kaggle

ingyenes GPU a tanításhoz

Zotero, Git

irodalomjegyzék és verziókezelés

1.4 Adatvédelem és etika (rövid fejezet a dolgozatban)

A videófelvétel személyes adat (GDPR), ezért a dolgozathoz nyilvános adathalmazokat vagy hozzájárulással készített, megrendezett felvételeket használunk.

A rendszer csak a vázat tárolja és csak figyelmeztet; a döntést mindig ember hozza meg (téves riasztás kockázata).

A jogi részleteket (szórakozóhelyi kamerázás szabályai) elég röviden bemutatni, és egyeztetni a témavezetővel.

2. Javasolt haladási irány (félévi ütemterv)

14 hetes félévre tervezve. Mivel a félév már folyamatban van, a hetek számozását a hátralévő időhöz kell igazítani; az első két hét anyaga összevonható.

Hét

Fókusz

Teendők

Kimenet

1–2

Alapozás

ST-GCN cikk és 2–3 verekedés-cikk elolvasása

Python / PyTorch gyakorlás

Osztályok és kutatási kérdések rögzítése

1 oldalas témaleírás

3

YOLOv8-Pose kipróbálása

Telepítés, kulcspontok kinyerése egy videóból

Követés bekapcsolása, adatok mentése (.npy)

Működő kinyerő szkript

4

Adatok

RWF-2000 (és ha elérhető, CCTV-Fights) letöltése

Vázkinyerés, minőségellenőrzés

Vázas adathalmaz

5

Előfeldolgozás

Normalizálás, időablakok, felosztás (train/val/test)

DataLoader

Betölthető adatok

6

Baseline

Egyszerű modell (ízületi szögek + Random Forest vagy LSTM)

Első eredmények

7–8

ST-GCN

COCO-17 gráf felépítése

Saját vagy PYSKL-es ST-GCN betanítása

Tanuló modell

9

Kiértékelés

F1, konfúziós mátrix, adatbővítés, hiperparaméterek

Eredménytáblázat

10

Szórakozóhelyi tesztek

Saját megrendezett jelenetek: tánc, lökdösődés, verekedés

Gyenge fény, tömeg; hibaelemzés

Hibaelemzés

11

Valós idejű demó

Videó → váz → ST-GCN → riasztás

FPS és késleltetés mérése

Demó, mérések

12

Összegzés

Ábrák, korlátok, továbbfejlesztési ötletek

Fejezetvázlatok

13

Írás

Teljes szöveg összeállítása

Első változat

14

Finomítás

Témavezetői visszajelzés, hiányok pótlása

Beadható dolgozat

Mérföldkövek és kockázatok

Mérföldkövek: M1 – működő kulcspont-kinyerés (3. hét); M2 – betanított baseline (6. hét); M3 – betanított ST-GCN (8. hét); M4 – demó (11. hét).

Kevés szórakozóhelyi adat: a kereséseim során nem találtam kifejezetten szórakozóhelyi, nyilvános verekedés-adathalmazt, ezért nyilvános verekedés-adatokat és saját, megrendezett felvételeket érdemes kombinálni.

Zajos váz: takarás és rossz fény rontja az eredményt; ezt a dolgozatban mérni és bemutatni kell, nem elrejteni.

Téves riasztás tánc miatt: tánc-felvételeket külön negatív osztályként kell a tanításba és a tesztbe is bevenni.

Szűkítés, ha elcsúszik az idő: kétosztályos feladat (verekedés / nem), a PYSKL-es ST-GCN használata saját implementáció helyett, a PyG-s változat elhagyása.

3. Források, cikkek és adathalmazok

Minden itt szereplő művet online források alapján ellenőriztem (cím, szerzők, megjelenési hely). A végső irodalomjegyzékben a pontos adatokat (oldalszámok, DOI) érdemes a kiadói oldalról átvenni.

3.1 Alapművek (ezekkel kezdd)

Yan, S., Xiong, Y., Lin, D.: Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition. AAAI 2018. arXiv:1801.07455. – az ST-GCN alapcikk.

Maji, D., Nagori, S., Mathew, M., Poddar, D.: YOLO-Pose: Enhancing YOLO for Multi Person Pose Estimation Using Object Keypoint Similarity Loss. CVPR Workshops 2022, pp. 2637–2646. arXiv:2204.06806. – a YOLO-alapú pózbecslés alapja (YOLOv5-re épül; a YOLOv8-Pose-nak nincs saját cikke).

Jocher, G., Chaurasia, A., Qiu, J.: Ultralytics YOLOv8 (v8.0.0), 2023. Szoftver. Dokumentáció: docs.ultralytics.com/datasets/pose (17 kulcspont) és docs.ultralytics.com/modes/track (követés: BoT-SORT alapértelmezett, ByteTrack). A használt verziót rögzítsd a dolgozatban.

Duan, H., Wang, J., Chen, K., Lin, D.: PYSKL: Towards Good Practices for Skeleton Action Recognition. ACM Multimedia 2022, pp. 7351–7354. arXiv:2205.09443. – kész PyTorch-eszköztár ST-GCN-hez, referenciának.

Kipf, T. N., Welling, M.: Semi-Supervised Classification with Graph Convolutional Networks. ICLR 2017. arXiv:1609.02907. – a gráfkonvolúció alapjaihoz (opcionális olvasmány).

3.2 Verekedés- és erőszakfelismerés váz-alapú módszerekkel (a témádhoz legközelebb)

Yang, H., Ren, Z., Yuan, H., Wei, W., Zhang, Q., Zhang, Z.: Multi-scale and attention enhanced graph convolution network for skeleton-based violence action recognition. Frontiers in Neurorobotics, 2022. DOI: 10.3389/fnbot.2022.1091361. – ST-GCN-alapú erőszakfelismerés; az NTU RGB+D 120-ból szűrt erőszakos akciókkal.

San Miguel, J. C., Garcia-Cobo, G.: Human skeletons and change detection for efficient violence detection in surveillance videos. Kód: github.com/atmguille/Violence-Detection-With-Human-Skeletons. – vázakra és mozgásváltozásra épülő módszer, RWF-2000-en tesztelve (a megjelenési helyet nem tudtam megerősíteni, ezért a hivatkozás előtt ellenőrizd).

Aung, S. T. Y., Kusakunniran, W., Hooi, Y. K.: Leveraging Fusion Methods of Human Pose and Motion Dynamics for Accurate Violence Detection in Video Surveillance. IEEE Access, 2025.

Aparicio Borjas, L. A., Nieto, V. E., Vasquez, J. I., Fernandez-Vazquez, A., Alvarez Hernandez, G. A.: Human Activity Recognition Method for Moderate Violence Detection. arXiv:2605.02659 (2026). – YOLO11-Pose és Random Forest a lökdösődés korai felismerésére; ez jó kiindulópont a baseline-hoz, és a magas, ferde kameraállásokat is vizsgálja.

3.3 Adathalmazok

Adathalmaz

Leírás és forrás

Mire jó a dolgozatban

RWF-2000

Cheng, Cai, Li: RWF-2000: An Open Large Scale Video Database for Violence Detection. ICPR 2020, pp. 4183–4190 (arXiv:1911.05913). 2000 megfigyelőkamerás klip, erőszakos / nem erőszakos.

Fő adathalmaz; a váz YOLOv8-Pose-zal kinyerhető belőle.

CCTV-Fights

Perez, Kot, Rocha: Detection of Real-world Fights in Surveillance Videos. ICASSP 2019. 1000 videó valódi verekedésről, ebből 280 CCTV-felvétel, időbeli annotációval.

Valósághűbb, nehezebb teszt; hozzáférés az NTU oldaláról kérhető.

UCF-Crime

Sultani, Chen, Shah: Real-World Anomaly Detection in Surveillance Videos. CVPR 2018 (arXiv:1801.04264). 1900 megfigyelőkamerás videó, 13 anomáliatípus (köztük verekedés).

Kiegészítő adat, főleg a verekedés-jelenetek.

NTU RGB+D 120

Liu et al., IEEE TPAMI 42(10), 2020 (arXiv:1905.04757). 120 akcióosztály; a Yang et al. (2022) erre építve állított össze erőszakos akcióknak szűrt változatot.

Kész 3D vázak; de 25 ízületes, nem a YOLO 17 pontos vázához illeszkedik.

Hockey Fight

Nievas et al.: 1000 rövid jégkorong-klip, verekedés / nem verekedés (a RWF-2000 cikk és áttekintő munkák is hivatkozzák).

Egyszerű, gyors első próbákhoz; a valós helyzetet kevéssé tükrözi.

Saját felvételek

Megrendezett jelenetek (tánc, lökdösődés, verekedés), a résztvevők írásos hozzájárulásával, a vázak mentésével.

Szórakozóhelyi jelleg tesztelése: tánc, gyenge fény, tömeg.

Teendő: minden adathalmaznál ellenőrizni a licencet és a letöltési feltételeket (egyes adathalmazokhoz hozzáférést kell kérni). A videó-alapú adathalmazoknál a vázkinyerés minőségét is mérni kell.

3.4 Következő lépések

Egyeztetni a témavezetővel az osztályokat (két vagy három) és a tesztelés módját.

Zotero felállítása, a 3.1–3.3 tételek bibliográfiai adatainak átvétele.

YOLOv8-Pose kipróbálása egy RWF-2000-es mintaklipen.