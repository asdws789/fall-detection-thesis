# -*- coding: utf-8 -*-
"""
Script to apply Chapter 7 and the final Bibliography to:
1. docs/szakdolgozat_dokumentum.md
2. docs/szakdolgozat.tex
3. scripts/generate_approved_docx.py
And regenerate the complete finalized DOCX.
"""

import os

MD_PATH = r"C:\uni_stuff\anti_thesis\docs\szakdolgozat_dokumentum.md"
TEX_PATH = r"C:\uni_stuff\anti_thesis\docs\szakdolgozat.tex"
GEN_PATH = r"C:\uni_stuff\anti_thesis\scripts\generate_approved_docx.py"

# =========================================================================
# 1. MARKDOWN CHAPTER 7 & BIBLIOGRAPHY
# =========================================================================
md_ch7 = """## 7. Kutatási és kísérleti terv a Szakdolgozat 2 félévre

A *Szakdolgozat 1* félév során elvégzett kutatási és feltáró munka eredményeként létrejött a rendszer átfogó követelményspecifikációja, szoftverarchitektúrája, a monokuláris pózbecslésre épülő kinematikai állapotelemző algoritmuscsalád, a leggyakoribb háztartási peremeseteket elhárító védelmi logikák, valamint a koncepció helyességét igazoló fejlesztői prototípus.

A *Szakdolgozat 2* félév feladata a tervezési dokumentumban lefektetett elméleti modellek teljes körű megvalósítása, az ST-GCN mélytanulási gráfhálózat betanítása és integrálása, a rendszer nagymintás független adatbázisokon történő szigorú benchmark validálása, valamint az optimalizált peremhálózati futtatás fizikai Raspberry Pi 5 hardveren történő mérése és verifikációja. Jelen fejezet részletezi a második félév kutatási célkitűzéseit, a 14 hetes ütemtervet, a kockázatelemzési mátrixot a tervezett alternatív ("B") mérnöki stratégiákkal, valamint a nagymintás validációs protokollt.

### 7.1 A Szakdolgozat 2 félév fő kutatási és mérnöki célkitűzései

A második félév fejlesztési és kutatási programja öt egymásra épülő fő célkitűzés köré szerveződik:

#### 1. Az ST-GCN mélytanulási gráfmodell betanítása és finomhangolása
A 3. fejezetben megtervezett tér-időbeli gráfkonvolúciós hálózat (*Spatial Temporal Graph Convolutional Network – ST-GCN*) [1] implementálása PyTorch környezetben.
* **Bemeneti reprezentáció:** A pózbecslő réteg által kinyert 17 anatómiai kulcspont időbeli sorozatából képzett lebegőpontos tenzor: $\\mathbf{X} \\in \\mathbb{R}^{B \\times C \\times T \\times V \\times M}$, ahol a kötegméret $B$, a csatornaszám $C=3$ (normalizált koordináták és konfidencia), az időablak hossza $T=30$ képkocka (1,2 másodperc 25 FPS mellett), a csúcsok száma $V=17$ (COCO-17 topológia), a megfigyelt személyek száma pedig $M=1$.
* **Tanítási környezet:** Felhőalapú dedikált GPU infrastruktúra igénybevétele (Google Colab Pro / egyetemi számítási klaszter) a hálózat tanításához, AdamW optimalizálóval, koszinuszos tanulási ráta csökkentéssel (*Cosine Annealing*) és fókuszált keresztentrópia veszteségfüggvénnyel (*Focal Loss*), amely kompenzálja a negatív (ADL) és pozitív (esés) minták közötti osztályegyensúlytalanságot.

#### 2. A kinematikai FSM és az ST-GCN hibrid döntési fúziója
A determinisztikus véges állapotgép (FSM) és a neurális gráfmodell szinergikus összekapcsolása a 3.5. alfejezetben specifikált arbitrációs architektúra szerint:
$$P_{\\text{fall}} = \\alpha \\cdot P_{\\text{FSM}} + (1 - \\alpha) \\cdot P_{\\text{ST-GCN}}$$
* Tiszta optikai látómező és teljes kulcspont-láthatóság esetén a gyors kinematikai állapotgép dominál ($\\alpha = 0{,}6$).
* Részleges takarás, járókeret használata vagy bizonytalanság esetén a súlyozás automatikusan átbillen ($\\alpha = 0{,}2$), átadva a döntést a takarásokra robusztus ST-GCN hálózatnak.

#### 3. Nagymintás, szigorúan független benchmark validáció
A fejlesztői szeleten tapasztalt módszertani korlátok és a tanító–teszt szivárgás feloldására a teljes nemzetközi **URFD** (70 videó: 30 esés, 40 ADL) [3] és a teljes **Le2i** (191 videó: 130 esés, 61 ADL négy eltérő szobakörnyezetben) [4] benchmark adatbázisok bevonása.
* Szigorú **Subject-out** (alanyfüggetlen) és **Scene-out** (helyszínfüggetlen) keresztvalidációs protokoll alkalmazása, garantálva, hogy a tesztelésre használt személyek és szobák a tanítási fázisban semmilyen formában nem szerepeltek.

#### 4. Ablációs és érzékenységvizsgálatok
Szisztematikus kísérletsorozat lefolytatása a rendszer robusztusságának feltárására:
* A döntési küszöbértékek ($AR_{\\text{thresh}}$, $\\theta_{\\text{torso}}$, $v_{y,\\text{thresh}}$) változtatásának hatása a pontosságra és a téves riasztási arányra (ROC és PR görbék felvétele).
* Az időablak hosszának ($T \\in \\{15, 30, 45\\}$ frame) hatása a detektálási késleltetésre és az osztályozási stabilitásra.
* A kamerapozíció, magasság és dőlésszög hatásának vizsgálata szintetikus perspektivikus transzformációkkal.

#### 5. Beágyazott peremhálózati implementáció és fizikai Raspberry Pi 5 mérések
A betanított hibrid modell exportálása ONNX formátumba [9], INT8 poszt-tanítási kvantálás elvégzése, valamint a teljes futtatókörnyezet telepítése és empirikus profilozása fizikai **Raspberry Pi 5** mikroszámítógépen, MIPI CSI-2 kamerával, mérve a tényleges ciklusidőt, FPS-t, memóriahasználatot és a processzor termikus viselkedését.

### 7.2 14 hetes szemeszteri ütemterv

A Szakdolgozat 2 félév 14 hetes szorgalmi időszakának mérnöki feladatait, mérföldköveit és elvárt kimeneteit a 7.1. táblázat foglalja össze.

**7.1. táblázat: A Szakdolgozat 2 félév részletes heti kutatási és megvalósítási ütemterve.**

| Hét | Mérföldkő / Fázis | Tervezett mérnöki feladatok | Elvárt kimenetek és dokumentáció |
| :---: | :--- | :--- | :--- |
| **1–2.** | **M1: Adatelőkészítés és tenzorgenerálás** | • A teljes URFD (70 videó) és Le2i (191 videó) adatbázis letöltése és rendszerezése.<br>• Képkockánkénti csontváz-extrakció YOLOv8-Pose modellel.<br>• Tenzorok normalizálása és mentése NumPy/HDF5 formátumban.<br>• Szigorú tanító/validációs/teszt adatszeletek képzése (*Scene-out*). | Strukturált, előfeldolgozott csontváz-adatkészlet $(B, 3, 30, 17, 1)$ tenzorformátumban. |
| **3–5.** | **M2: ST-GCN modelltanítás** | • Az ST-GCN PyTorch gráfkonvolúciós architektúra felépítése.<br>• Adatbővítési eljárások (időbeli nyújtás, térbeli forgatás, kulcspont-zajongás) implementálása.<br>• Modelltanítás Colab Pro GPU-n, hiperparaméter-hangolás.<br>• Veszteséggörbék és validációs konvergencia monitorozása. | Betanított PyTorch modellsúlyok (`stgcn_best.pt`), tanítási naplófájlok és tanulási görbék. |
| **6–7.** | **M3: Hibrid döntési integráció** | • A betanított ST-GCN modell exportálása ONNX formátumba.<br>• A hibrid arbitrációs motor megvalósítása a pipeline-ban.<br>• Az állapotgép és a gráfmodell közötti súlyozási logika finomhangolása járókeretes és takart peremesetekre. | Működő hibrid szoftveres csővezeték (`HybridFallDetector`), integrációs tesztek. |
| **8–9.** | **M4: Nagymintás független validáció** | • A teljes független teszthalmaz kiértékelése a hibrid modellel.<br>• Konfúziós mátrixok felvétele, metrikák számítása (Recall, Precision, F1, FPR, ROC-AUC).<br>• Döntési késleltetés statisztikai elemzése.<br>• Hibaelemzés a téves pozitív és hamis negatív eseteken. | Teljes kiértékelési benchmark táblázatok, ROC/PR görbék és késleltetési hisztogramok. |
| **10.** | **M5: Ablációs vizsgálatok** | • Csúszóablak-méret ablácó ($T = 15, 30, 45$ frame).<br>• Kinematikai küszöbök érzékenységvizsgálata.<br>• Homográfia és kameraszög szimuláció. | Ablációs tanulmány fejezetábrái, érzékenységi mátrixok. |
| **11.** | **M6: Beágyazott Raspberry Pi 5 tesztek** | • ONNX Runtime INT8 PTQ kvantálás kalibrációval.<br>• Telepítés Raspberry Pi 5 hardverre (Raspberry Pi OS 64-bit).<br>• CSI kamera integráció, GPIO hardveres sziréna vezérlés.<br>• Tényleges hardveres ciklusidő-, FPS- és hőmérsékletmérés. | Beágyazott mérési jegyzőkönyv, profilozási adatsorok, demonstrációs fotók és videók. |
| **12–13.** | **M7: Szakdolgozat véglegesítése** | • A szakdolgozat fejezeteinek végleges szövegezése.<br>• Szakirodalmi hivatkozások lezárása, formai követelmények ellenőrzése.<br>• Forráskód refaktorálása, GitHub repository és dokumentáció rendezése. | Véglegesített, nyomtatásra kész Szakdolgozat dokumentum (PDF) és forráskód. |
| **14.** | **M8: Védési felkészülés** | • Védési prezentáció diasorának elkészítése.<br>• Demonstrációs videók és élő szoftveres bemutató előkészítése.<br>• Próbavédés és konzultáció a témavezetővel. | Védési prezentáció (.pptx / .pdf), videós demonstrációs anyagok. |

### 7.3 Kockázatelemzési mátrix és hibaelhárítási tervek (Risk Mitigation)

Egy komplex gépi tanulási és beágyazott hardveres fejlesztési projekt során számos előre nem látható műszaki és módszertani kockázat léphet fel. A kockázatok proaktív kezelésére a 7.2. táblázat összefoglalja a feltárt veszélyforrásokat, azok becsült valószínűségét, a projektre gyakorolt hatását, valamint a kidolgozott megelőzési és alternatív ("B-terv") stratégiákat.

**7.2. táblázat: A Szakdolgozat 2 projekt kockázatelemzési és hibaelhárítási mátrixa.**

| Kockázat megnevezése és leírása | Kategória | Valószínűség | Hatás | Megelőző mérnöki intézkedés | Kontingencia / B-terv |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **K1: ST-GCN túltanulás kis pozitív mintán**<br>A nyilvános esési adatbázisok korlátozott esési eseményt tartalmaznak a több ezer órányi hétköznapi mozgáshoz képest. | Algoritmikus / Adat | Közepes | Magas | Erőteljes geometriai és temporális adatbővítés (DropGraph, véletlenszerű csontváz-tükrözés, időbeli skálázás $\\pm 20\\%$). | DropBlock reguláció alkalmazása, vagy transzfertanulás indítása NTU-RGB+D nagyméretű cselekvésfelismerő súlyokból. |
| **K2: Valós idejű sebességvesztés Raspberry Pi-n**<br>A mély hálózat együttes futása miatt a képkockasebesség a célként kitűzött 20 FPS alá esik. | Hardver / Teljesítmény | Közepes | Közepes | INT8 poszt-tanítási kvantálás, NCNN C++ futtatókörnyezet használata ARM NEON SIMD optimalizációval. | Adaptív képkocka-átugrás (*Frame Skipping*): a pózbecslés minden 2. frame-en fut (12,5 FPS), közben egyszerű optikai mozgáskövetés tölti ki az átmenetet. |
| **K3: Kameraszög- és perspektíva-érzékenység**<br>Eltérő belmagasság vagy dőlésszög esetén a talajsík-határvonal és a vertikális sebesség torzul. | Módszertani | Magas | Közepes | Relatív, anatómiai méretekkel skálázott jellemzők prioritása a fix képpontos küszöbökkel szemben. | Felhasználói 2 pontos kalibrációs modul beépítése az üzembe helyezéskor, amely homográfiával transzformálja a padlósíkot. |
| **K4: Kulcspontvesztés tartós fizikai kitakaráskor**<br>A bútor vagy segédeszköz mögé eső alany testrészei tartósan nem láthatók a monokuláris kamerán. | Észlelési / Szenzor | Közepes | Magas | Zuhanási előzménymemória és hiszterézises állapotmegőrzés a detektálási kiesés idejére. | Az ST-GCN időbeli rekurziójának kiterjesztése LSTM / GRU cellával, amely a részleges felsőtest-trajektóriából rekonstruálja az esést. |
| **K5: Memóriaszivárgás tartós 24/7 futás során**<br>A hosszú idejű folyamatos megfigyelés alatt a Python szemétgyűjtője vagy az OpenCV pufferje telítődik. | Szoftver-architektúra | Alacsony | Magas | Profilozás `tracemalloc` és `valgrind` eszközökkel; explicit memóriafelszabadítás a csővezeték minden ciklusában. | Rendszerszintű `systemd` watchdog és automatikus izolált folyamat-újraindítás (restart on failure) hiba esetén. |

### 7.4 Nagymintás kísérleti és validációs protokoll

A szakdolgozati kutatás hitelességének sarokköve a mérési eredmények reprodukálhatósága és a statisztikai megalapozottság. A Szakdolgozat 2 félévben elvégzendő nagymintás validáció protokollja az alábbi szigorú előírásokat követi:

#### 7.4.1 Adatbázisok és eloszlásuk
1. **URFD (University of Rzeszow Fall Dataset):**
   * 30 valós esési felvétel és 40 összetett hétköznapi tevékenység (ADL – leülés, felállás, tárgyért lehajolás, lefekvés).
   * Monokuláris RGB és mélységi kameraállások.
2. **Le2i Fall Detection Dataset:**
   * 191 videó négy különböző helyiségben (Home, Coffee Room, Office, Lecture Room).
   * Változatos megvilágítási viszonyok, optikai reflexiók, részleges takarások bútorok által.
3. **Független segédeszközös teszthalmaz:**
   * 15 saját rögzítésű és internetes tesztvideó kifejezetten idősotthoni segédeszközökkel (járókeret, kerekesszék, mankó).

#### 7.4.2 Osztályozási és megbízhatósági metrikák
A rendszerteljesítmény számszerűsítésére a nemzetközi szakirodalomban szabványos metrikák szolgálnak:
* **Érzékenység / Szenzitivitás (Sensitivity / Recall / TPR):**
  $$\\text{TPR} = \\frac{\\text{TP}}{\\text{TP} + \\text{FN}}$$
* **Precízió (Precision / PPV):**
  $$\\text{PPV} = \\frac{\\text{TP}}{\\text{TP} + \\text{FP}}$$
* **Harmonikus átlag (F1-score):**
  $$\\text{F1} = 2 \\cdot \\frac{\\text{Precision} \\cdot \\text{Recall}}{\\text{Precision} + \\text{Recall}}$$
* **Téves Pozitív Ráta (False Positive Rate – FPR):**
  $$\\text{FPR} = \\frac{\\text{FP}}{\\text{FP} + \\text{TN}}$$
* **Görbe alatti terület (ROC-AUC és PR-AUC):** A döntési küszöbök függvényében a modell diszkriminációs képességének átfogó vizsgálata.
* **Döntési késleltetés ($T_{\\text{latency}}$):** Képkocka-szintű időbélyeg-összevetés a becsapódási pont ($T_{\\text{impact}}$) és a riasztás megerősítése ($T_{\\text{detect}}$) között.

#### 7.4.3 Hardveres és beágyazott mérési metrikák
A Raspberry Pi 5 hardveren futtatott tesztek során rögzítendő fizikai paraméterek:
* **Átviteli sebesség (FPS):** Átlag, szórás, minimum és p95 percentilis 30 perces folyamatos üzemben.
* **Komponensenkénti futásidő (ms):** Képbeolvasás, pózbecslés, ST-GCN inferencia, állapotgép és telemetria.
* **Erőforrás-kihasználtság:** Processzor-kihasználtság magonként (%), rezidens memóriafoglalás (RSS MB).
* **Termikus viselkedés:** SoC maghőmérséklet (°C) és dinamikus frekvenciaszabályozás monitorozása tartós terhelés alatt.

A fenti kutatási és kísérleti program maradéktalan végrehajtása garantálja, hogy a Szakdolgozat 2 félév végére egy tudományosan megalapozott, szigorúan validált és beágyazott környezetben is működőképes mérnöki diplomamunka szülessen meg.

---

## Irodalomjegyzék

1. **S. Yan, Y. Xiong, D. Lin:** *Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition*. In: Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 32, No. 1, 2018.
2. **G. Jocher, A. Chaurasia, J. Qiu:** *Ultralytics YOLOv8 Architecture and Pose Estimation*. Ultralytics Documentation, 2023. [Online: https://docs.ultralytics.com]
3. **B. Kwolek, M. Kepski:** *Human fall detection on embedded platform using depth maps and wireless accelerometer*. Computer Methods and Programs in Biomedicine, 117(3):489-501, 2014.
4. **I. Charfi, J. Miteran, J. Dubois, M. Atri, R. Tourki:** *Optimized Spatio-Temporal Descriptors for Real-Time Fall Detection: Comparison of Support Vector Machine and AdaBoost-Based Classification*. Journal of Electronic Imaging, 22(4):041106, 2013.
5. **World Health Organization:** *Step Safely: Strategies for preventing and managing falls across the life-course*. Geneva: WHO Guidelines Approved by the Guidelines Review Committee, 2021.
6. **D. Wild, U. S. Nayak, B. Isaacs:** *How dangerous are falls in old people at home?*. British Medical Journal (Clinical Research Ed.), 282(6260):266-268, 1981.
7. **M. E. Tinetti, W. L. Liu, E. B. Claus:** *Predictors and prognosis of inability to get up after falls among elderly persons*. JAMA: The Journal of the American Medical Association, 269(1):65-70, 1993.
8. **Intel Corporation:** *OpenVINO Toolkit: Deep Learning Deployment Framework and Action Recognition Models*. Intel Technical Documentation, 2022.
9. **Microsoft Corporation:** *ONNX Runtime: Cross-platform, high performance ML inferencing and training accelerator*. 2023. [Online: https://onnxruntime.ai]
10. **C. Rougier, J. Meunier, A. St-Arnaud, J. Rousseau:** *Robust Video Surveillance for Fall Detection Based on 3D Head Trajectory Analysis*. IEEE Transactions on Circuits and Systems for Video Technology, 21(9):1232-1241, 2011.
11. **H. Foroughi, A. Rezvanian, A. Paziraee:** *Robust fall detection using eigenspaces and upper bound shape features*. In: 2008 8th IEEE International Conference on Computer and Information Technology, pp. 721-726, 2008.
12. **Z. Cao, G. Hidalgo, T. Simon, S.-E. Wei, Y. Sheikh:** *OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields*. IEEE Transactions on Pattern Analysis and Machine Intelligence, 43(1):172-186, 2019.
13. **Európai Parlament és Tanács:** *Az Európai Parlament és a Tanács (EU) 2016/679 rendelete (Általános Adatvédelmi Rendelet - GDPR)*. Hivatalos Lapja az Európai Uniónak, L 119, 2016.
14. **T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollár, C. L. Zitnick:** *Microsoft COCO: Common Objects in Context*. In: European Conference on Computer Vision (ECCV), pp. 740-755, Springer, 2014.
15. **ARM Limited:** *Arm Cortex-A Programmer's Guide for ARMv8-A: NEON Technology and Advanced SIMD Architecture*. Arm Technical Reference Manual, 2020.
"""

# Update Markdown
with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

ch7_start_md = "## 7. Kutatási és fejlesztési terv a Szakdolgozat 2 félévre"
if ch7_start_md in md_content:
    p1 = md_content.split(ch7_start_md)[0]
    new_md = p1 + md_ch7
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(new_md)
    print("[OK] Chapter 7 and Bibliography updated in docs/szakdolgozat_dokumentum.md")
else:
    print("[ERROR] ch7_start_md not found in Markdown")

# =========================================================================
# 2. LATEX CHAPTER 7
# =========================================================================
tex_ch7 = r"""\chapter{Kutatási és kísérleti terv a Szakdolgozat 2 félévre}

A \textit{Szakdolgozat 1} félév során elvégzett kutatási és feltáró munka eredményeként létrejött a rendszer átfogó követelményspecifikációja, szoftverarchitektúrája, a monokuláris pózbecslésre épülő kinematikai állapotelemző algoritmuscsalád, a leggyakoribb háztartási peremeseteket elhárító védelmi logikák, valamint a koncepció helyességét igazoló fejlesztői prototípus.

A \textit{Szakdolgozat 2} félév feladata a tervezési dokumentumban lefektetett elméleti modellek teljes körű megvalósítása, az ST-GCN mélytanulási gráfhálózat betanítása és integrálása, a rendszer nagymintás független adatbázisokon történő szigorú benchmark validálása, valamint az optimalizált peremhálózati futtatás fizikai Raspberry Pi 5 hardveren történő mérése és verifikációja. Jelen fejezet részletezi a második félév kutatási célkitűzéseit, a 14 hetes ütemtervet, a kockázatelemzési mátrixot a tervezett alternatív ("B") mérnöki stratégiákkal, valamint a nagymintás validációs protokollt.

\section{A Szakdolgozat 2 félév fő kutatási és mérnöki célkitűzései}
A második félév fejlesztési és kutatási programja öt egymásra épülő fő célkitűzés köré szerveződik:

\subsection{Az ST-GCN mélytanulási gráfmodell betanítása és finomhangolása}
A 3. fejezetben megtervezett tér-időbeli gráfkonvolúciós hálózat (\textit{Spatial Temporal Graph Convolutional Network -- ST-GCN}) \cite{yan2018stgcn} implementálása PyTorch környezetben.
\begin{itemize}
    \item \textbf{Bemeneti reprezentáció:} A pózbecslő réteg által kinyert 17 anatómiai kulcspont időbeli sorozatából képzett lebegőpontos tenzor: $\mathbf{X} \in \mathbb{R}^{B \times C \times T \times V \times M}$, ahol a kötegméret $B$, a csatornaszám $C=3$ (normalizált koordináták és konfidencia), az időablak hossza $T=30$ képkocka (1,2 másodperc 25 FPS mellett), a csúcsok száma $V=17$ (COCO-17 topológia), a megfigyelt személyek száma pedig $M=1$.
    \item \textbf{Tanítási környezet:} Felhőalapú dedikált GPU infrastruktúra igénybevétele (Google Colab Pro / egyetemi számítási klaszter) a hálózat tanításához, AdamW optimalizálóval, koszinuszos tanulási ráta csökkentéssel (\textit{Cosine Annealing}) és fókuszált keresztentrópia veszteségfüggvénnyel (\textit{Focal Loss}), amely kompenzálja a negatív (ADL) és pozitív (esés) minták közötti osztályegyensúlytalanságot.
\end{itemize}

\subsection{A kinematikai FSM és az ST-GCN hibrid döntési fúziója}
A determinisztikus véges állapotgép (FSM) és a neurális gráfmodell szinergikus összekapcsolása a 3.5. alfejezetben specifikált arbitrációs architektúra szerint:
\begin{equation}
P_{\text{fall}} = \alpha \cdot P_{\text{FSM}} + (1 - \alpha) \cdot P_{\text{ST-GCN}}
\end{equation}
Tiszta optikai látómező és teljes kulcspont-láthatóság esetén a gyors kinematikai állapotgép dominál ($\alpha = 0{,}6$), míg részleges takarás vagy bizonytalanság esetén a súlyozás automatikusan átbillen ($\alpha = 0{,}2$), átadva a döntést a takarásokra robusztus ST-GCN hálózatnak.

\subsection{Nagymintás, szigorúan független benchmark validáció}
A fejlesztői szeleten tapasztalt módszertani korlátok és a tanító--teszt szivárgás feloldására a teljes nemzetközi \textbf{URFD} (70 videó: 30 esés, 40 ADL) \cite{urfd2014} és a teljes \textbf{Le2i} (191 videó: 130 esés, 61 ADL négy eltérő szobakörnyezetben) \cite{le2i2013} benchmark adatbázisok bevonása. Szigorú \textbf{Subject-out} (alanyfüggetlen) és \textbf{Scene-out} (helyszínfüggetlen) keresztvalidációs protokoll alkalmazása garantálja a független általánosító képesség mérését.

\subsection{Ablációs és érzékenységvizsgálatok}
Szisztematikus kísérletsorozat lefolytatása a rendszer robusztusságának feltárására: a döntési küszöbértékek ($AR_{\text{thresh}}$, $\theta_{\text{torso}}$, $v_{y,\text{thresh}}$), az időablak hossza ($T \in \{15, 30, 45\}$ frame) és a kameradőlésszög hatásának vizsgálata ROC és PR görbék mentén.

\subsection{Beágyazott peremhálózati implementáció és fizikai Raspberry Pi 5 mérések}
A betanított hibrid modell exportálása ONNX formátumba \cite{onnxruntime2023}, INT8 poszt-tanítási kvantálás elvégzése, valamint a teljes futtatókörnyezet telepítése és empirikus profilozása fizikai \textbf{Raspberry Pi 5} mikroszámítógépen, MIPI CSI-2 kamerával, mérve a tényleges ciklusidőt, FPS-t, memóriahasználatot és a processzor termikus viselkedését.

\section{14 hetes szemeszteri ütemterv}
A Szakdolgozat 2 félév 14 hetes szorgalmi időszakának mérnöki feladatait, mérföldköveit és elvárt kimeneteit a \ref{tab:schedule}. táblázat foglalja össze.

\begin{table}[H]
\centering
\small
\begin{tabularx}{\textwidth}{cp{4.2cm}X}
\toprule
\textbf{Hét} & \textbf{Mérföldkő / Fázis} & \textbf{Tervezett mérnöki feladatok és kimenetek} \\
\midrule
\textbf{1--2.} & \textbf{M1: Adatelőkészítés és tenzorgenerálás} & A teljes URFD (70 videó) és Le2i (191 videó) adatbázis csontváz-extrakciója YOLOv8 modellel. Tenzorok mentése NumPy/HDF5 formátumban. Szigorú \textit{Scene-out} tanító/teszt szeletek képzése. \\
\textbf{3--5.} & \textbf{M2: ST-GCN modelltanítás} & Az ST-GCN PyTorch gráfkonvolúciós architektúra felépítése. Adatbővítési eljárások (DropGraph, tükrözés, időskálázás). Modelltanítás Colab Pro GPU-n, hiperparaméter-hangolás. \\
\textbf{6--7.} & \textbf{M3: Hibrid döntési integráció} & Az ST-GCN exportálása ONNX formátumba. A hibrid arbitrációs motor megvalósítása a pipeline-ban. Állapotgép és gráfmodell fúziója peremesetekre. \\
\textbf{8--9.} & \textbf{M4: Nagymintás független validáció} & A teljes teszthalmaz kiértékelése. Konfúziós mátrixok, metrikák (Recall, Precision, F1, FPR, ROC-AUC), és döntési késleltetés statisztikai elemzése. \\
\textbf{10.} & \textbf{M5: Ablációs vizsgálatok} & Csúszóablak-méret abláció ($T = 15, 30, 45$ frame), kinematikai küszöbök érzékenységvizsgálata és hibaanalízis. \\
\textbf{11.} & \textbf{M6: Beágyazott Raspberry Pi 5 tesztek} & ONNX Runtime INT8 PTQ kvantálás kalibrációval. Telepítés Raspberry Pi 5 hardverre, CSI kamera és GPIO sziréna integráció, tényleges futásidőmérés. \\
\textbf{12--13.} & \textbf{M7: Szakdolgozat véglegesítése} & A szakdolgozat fejezeteinek végleges szövegezése, hivatkozások ellenőrzése, formai követelmények és kódrendezés. \\
\textbf{14.} & \textbf{M8: Védési felkészülés} & Védési prezentáció diasorának elkészítése, videós demonstrációk összeállítása, próbavédés. \\
\bottomrule
\end{tabularx}
\caption{A Szakdolgozat 2 félév részletes 14 hetes ütemterve és mérföldkövei.}
\label{tab:schedule}
\end{table}

\section{Kockázatelemzési mátrix és hibaelhárítási tervek}
A feltárt műszaki kockázatokat, azok valószínűségét, hatását és a kidolgozott megelőzési, valamint kontingencia (B-terv) intézkedéseket a \ref{tab:risks}. táblázat foglalja össze.

\begin{table}[H]
\centering
\small
\begin{tabularx}{\textwidth}{p{3.2cm}ccXX}
\toprule
\textbf{Kockázat leírása} & \textbf{Valósz.} & \textbf{Hatás} & \textbf{Megelőző intézkedés} & \textbf{Kontingencia / B-terv} \\
\midrule
\textbf{K1: ST-GCN túltanulás kis pozitív mintán} & Közepes & Magas & Erőteljes geometriai és temporális adatbővítés (DropGraph, időbeli skálázás $\pm 20\%$). & DropBlock reguláció vagy transzfertanulás NTU-RGB+D súlyokból. \\
\textbf{K2: Sebességvesztés Raspberry Pi-n} & Közepes & Közepes & INT8 poszt-tanítási kvantálás, NCNN C++ futtatókörnyezet ARM NEON SIMD optimalizációval. & Adaptív képkocka-átugrás (\textit{Frame Skipping}): pózbecslés minden 2. frame-en (12,5 FPS). \\
\textbf{K3: Kameraszög- és perspektíva torzulás} & Magas & Közepes & Relatív, anatómiai méretekkel skálázott jellemzők prioritása a fix képpontos küszöbökkel szemben. & Felhasználói 2 pontos kalibrációs modul beépítése az üzembe helyezéskor homográfia transzformációval. \\
\textbf{K4: Kulcspontvesztés tartós kitakaráskor} & Közepes & Magas & Zuhanási előzménymemória és hiszterézises állapotmegőrzés a kiesés idejére. & ST-GCN időbeli rekurziójának kiterjesztése LSTM/GRU réteggel a részleges felsőtest-trajektóriára. \\
\textbf{K5: Memóriaszivárgás 24/7 futás során} & Alacsony & Magas & Profilozás \texttt{tracemalloc}-kal, explicit memóriafelszabadítás minden ciklusban. & Rendszerszintű \texttt{systemd} watchdog és automatikus izolált folyamat-újraindítás. \\
\bottomrule
\end{tabularx}
\caption{A Szakdolgozat 2 projekt kockázatelemzési és hibaelhárítási mátrixa.}
\label{tab:risks}
\end{table}

\section{Nagymintás kísérleti és validációs protokoll}
A szakdolgozati kutatás hitelességének sarokköve a mérési eredmények reprodukálhatósága és a statisztikai megalapozottság.

\subsection{Adatbázisok és eloszlásuk}
\begin{itemize}
    \item \textbf{URFD (University of Rzeszow Fall Dataset):} 30 valós esési felvétel és 40 összetett hétköznapi tevékenység (ADL) monokuláris RGB és mélységi kameraállásokkal \cite{urfd2014}.
    \item \textbf{Le2i Fall Detection Dataset:} 191 videó négy különböző helyiségben (Home, Coffee Room, Office, Lecture Room) változatos megvilágítási viszonyok és optikai reflexiók mellett \cite{le2i2013}.
    \item \textbf{Független segédeszközös teszthalmaz:} 15 tesztvideó kifejezetten idősotthoni segédeszközökkel (járókeret, kerekesszék, mankó).
\end{itemize}

\subsection{Osztályozási és megbízhatósági metrikák}
A rendszerteljesítmény számszerűsítésére alkalmazott nemzetközi szabványos metrikák:
\begin{equation}
\text{TPR} = \frac{\text{TP}}{\text{TP} + \text{FN}}, \qquad \text{PPV} = \frac{\text{TP}}{\text{TP} + \text{FP}}, \qquad \text{F1} = 2 \cdot \frac{\text{PPV} \cdot \text{TPR}}{\text{PPV} + \text{TPR}}, \qquad \text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}}
\end{equation}
A metrikák kiegészülnek a ROC-AUC és PR-AUC görbék elemzésével, valamint a döntési késleltetés ($T_{\text{latency}} = T_{\text{detect}} - T_{\text{impact}}$) másodperc-alapú statisztikájával.

\subsection{Hardveres és beágyazott mérési metrikák}
A Raspberry Pi 5 hardveren futtatott tesztek során rögzítendő fizikai paraméterek: átviteli sebesség (FPS átlag, szórás, p95), komponensenkénti futásidő (ms), memóriafoglalás (RSS MB), processzorterhelés (\%) és a SoC maghőmérséklete (°C).
"""

with open(TEX_PATH, "r", encoding="utf-8") as f:
    tex_content = f.read()

ch7_start_tex = r"\chapter{Kutatási és fejlesztési terv a Szakdolgozat 2 félévre}"
bib_start_tex = r"\begin{thebibliography}{99}"

if ch7_start_tex in tex_content and bib_start_tex in tex_content:
    p1 = tex_content.split(ch7_start_tex)[0]
    p2 = tex_content.split(bib_start_tex)[1]
    new_tex = p1 + tex_ch7 + "\n\n% " + "="*73 + "\n% IRODALOMJEGYZÉK\n% " + "="*73 + "\n" + r"\begin{thebibliography}{99}" + p2
    with open(TEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_tex)
    print("[OK] Chapter 7 updated in docs/szakdolgozat.tex")
else:
    print("[ERROR] Split points not found in LaTeX")

# =========================================================================
# 3. DOCX GENERATOR CHAPTER 7 & BIBLIOGRAPHY CODE
# =========================================================================
ch7_docx_code = '''
    doc.add_page_break()

    # =========================================================================
    # 7. FEJEZET: KUTATÁSI ÉS KÍSÉRLETI TERV A SZAKDOLGOZAT 2 FÉLÉVRE
    # =========================================================================
    add_heading_1("7. Kutatási és kísérleti terv a Szakdolgozat 2 félévre")

    doc.add_paragraph(
        "A Szakdolgozat 1 félév során elvégzett kutatási és feltáró munka eredményeként létrejött a rendszer átfogó "
        "követelményspecifikációja, szoftverarchitektúrája, a monokuláris pózbecslésre épülő kinematikai állapotelemző "
        "algoritmuscsalád, a leggyakoribb háztartási peremeseteket elhárító védelmi logikák, valamint a koncepció helyességét "
        "igazoló fejlesztői prototípus.\\n\\n"
        "A Szakdolgozat 2 félév feladata a tervezési dokumentumban lefektetett elméleti modellek teljes körű megvalósítása, "
        "az ST-GCN mélytanulási gráfhálózat betanítása és integrálása, a rendszer nagymintás független adatbázisokon történő "
        "szigorú benchmark validálása, valamint az optimalizált peremhálózati futtatás fizikai Raspberry Pi 5 hardveren "
        "történő mérése és verifikációja. Jelen fejezet részletezi a második félév kutatási célkitűzéseit, a 14 hetes ütemtervet, "
        "a kockázatelemzési mátrixot a tervezett alternatív (\\"B\\") mérnöki stratégiákkal, valamint a nagymintás validációs protokollt."
    )

    add_heading_2("7.1 A Szakdolgozat 2 félév fő kutatási és mérnöki célkitűzései")
    doc.add_paragraph(
        "A második félév fejlesztési és kutatási programja öt egymásra épülő fő célkitűzés köré szerveződik:\\n\\n"
        "1. Az ST-GCN mélytanulási gráfmodell betanítása és finomhangolása: A 3. fejezetben megtervezett tér-időbeli "
        "gráfkonvolúciós hálózat (ST-GCN) [1] implementálása PyTorch környezetben. A bemenetet a 17 kulcspont 30 képkockás "
        "csúszóablakából képzett X ∈ R^(B × 3 × 30 × 17 × 1) tenzor képezi. A tanítás felhőalapú dedikált GPU klaszteren történik "
        "AdamW optimalizálóval, koszinuszos tanulási ráta csökkentéssel és fókuszált keresztentrópia veszteségfüggvénnyel (Focal Loss).\\n\\n"
        "2. A kinematikai FSM és az ST-GCN hibrid döntési fúziója: A determinisztikus véges állapotgép és a neurális gráfmodell "
        "szinergikus összekapcsolása a definiált arbitrációs architektúra szerint: P_fall = α · P_FSM + (1 - α) · P_ST-GCN. "
        "Tiszta optikai látómező esetén a gyors állapotgép dominál (α = 0,6), míg részleges takarás, járókeret vagy bizonytalanság esetén "
        "a súlyozás automatikusan átbillen (α = 0,2), átadva a döntést az ST-GCN hálózatnak.\\n\\n"
        "3. Nagymintás, szigorúan független benchmark validáció: A fejlesztői kalibrációs szeleten túllépve a teljes nemzetközi "
        "URFD (70 videó) [3] és a teljes Le2i (191 videó) [4] adatbázis bevonása. Szigorú Subject-out és Scene-out keresztvalidációs "
        "protokoll alkalmazása garantálja a független általánosító képesség mérését.\\n\\n"
        "4. Ablációs és érzékenységvizsgálatok: Szisztematikus kísérletsorozat a döntési küszöbök (AR, dőlésszög, vertikális sebesség), "
        "az időablak hossza (T = 15, 30, 45 frame) és a kameradőlésszög hatásának feltárására ROC és PR görbék mentén.\\n\\n"
        "5. Beágyazott peremhálózati implementáció és fizikai Raspberry Pi 5 mérések: A hibrid modell exportálása ONNX formátumba [9], "
        "INT8 poszt-tanítási kvantálás elvégzése, valamint a futtatókörnyezet telepítése és empirikus profilozása fizikai Raspberry Pi 5 "
        "hardveren MIPI CSI-2 kamerával, mérve a ciklusidőt, FPS-t, memóriahasználatot és a processzor termikus viselkedését."
    )

    add_heading_2("7.2 14 hetes szemeszteri ütemterv")
    doc.add_paragraph(
        "A Szakdolgozat 2 félév 14 hetes szorgalmi időszakának mérnöki feladatait, mérföldköveit és elvárt kimeneteit a 7.1. táblázat foglalja össze."
    )

    # 7.1. táblázat: Ütemterv
    table_sched = doc.add_table(rows=9, cols=3)
    table_sched.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sched.autofit = False

    s_headers = ["Hét", "Mérföldkő / Fázis", "Tervezett mérnöki feladatok és elvárt kimenetek"]
    s_widths = [Inches(1.0), Inches(2.2), Inches(3.9)]

    for j, h in enumerate(s_headers):
        cell = table_sched.rows[0].cells[j]
        cell.width = s_widths[j]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=80, bottom=80, left=60, right=60)

    s_data = [
        ("1–2.", "M1: Adatelőkészítés és tenzorgenerálás", "A teljes URFD (70 videó) és Le2i (191 videó) csontváz-extrakciója YOLOv8 modellel. Tenzorok normalizálása és mentése NumPy/HDF5 formátumban. Szigorú Scene-out adatszeletek képzése."),
        ("3–5.", "M2: ST-GCN modelltanítás", "Az ST-GCN PyTorch gráfkonvolúciós architektúra felépítése. Adatbővítési eljárások (DropGraph, tükrözés, időskálázás). Modelltanítás Colab Pro GPU-n, hiperparaméter-hangolás és konvergencia-elemzés."),
        ("6–7.", "M3: Hibrid döntési integráció", "Az ST-GCN exportálása ONNX formátumba. A hibrid arbitrációs motor megvalósítása a pipeline-ban. Állapotgép és gráfmodell fúziója peremesetekre és takarásokra."),
        ("8–9.", "M4: Nagymintás független validáció", "A teljes független teszthalmaz kiértékelése a hibrid modellel. Konfúziós mátrixok, metrikák (Recall, Precision, F1, FPR, ROC-AUC), és döntési késleltetés statisztikai elemzése."),
        ("10.", "M5: Ablációs vizsgálatok", "Csúszóablak-méret abláció (T = 15, 30, 45 frame), kinematikai küszöbök érzékenységvizsgálata és hibaanalízis."),
        ("11.", "M6: Beágyazott Raspberry Pi 5 tesztek", "ONNX Runtime INT8 PTQ kvantálás kalibrációval. Telepítés Raspberry Pi 5 hardverre, CSI kamera és GPIO sziréna integráció, tényleges hardveres ciklusidő- és FPS-mérés."),
        ("12–13.", "M7: Szakdolgozat véglegesítése", "A szakdolgozat fejezeteinek végleges szövegezése, hivatkozások ellenőrzése, formai követelmények és kódrendezés."),
        ("14.", "M8: Védési felkészülés", "Védési prezentáció diasorának elkészítése, videós demonstrációk összeállítása, próbavédés és konzultáció.")
    ]

    for i, row in enumerate(s_data):
        for j, val in enumerate(row):
            cell = table_sched.rows[i+1].cells[j]
            cell.width = s_widths[j]
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.bold = True
            elif j == 1:
                run.bold = True
            bg_color = "F8FAFC" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)

    p_cap_s = doc.add_paragraph()
    p_cap_s.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_s.paragraph_format.space_before = Pt(4)
    p_cap_s.paragraph_format.space_after = Pt(12)
    r_cap_s = p_cap_s.add_run("7.1. táblázat: A Szakdolgozat 2 félév részletes 14 hetes ütemterve és mérföldkövei.")
    r_cap_s.font.size = Pt(10)
    r_cap_s.font.italic = True
    r_cap_s.font.color.rgb = COLOR_MUTED

    add_heading_2("7.3 Kockázatelemzési mátrix és hibaelhárítási tervek")
    doc.add_paragraph(
        "A feltárt műszaki kockázatokat, azok valószínűségét, hatását és a kidolgozott megelőzési, valamint kontingencia "
        "(B-terv) intézkedéseket a 7.2. táblázat foglalja össze."
    )

    # 7.2. táblázat: Kockázatok
    table_rk = doc.add_table(rows=6, cols=5)
    table_rk.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_rk.autofit = False

    rk_headers = ["Kockázat leírása", "Kategória", "Valósz.", "Hatás", "Megelőző intézkedés és Kontingencia / B-terv"]
    rk_widths = [Inches(1.8), Inches(1.1), Inches(0.7), Inches(0.7), Inches(2.8)]

    for j, h in enumerate(rk_headers):
        cell = table_rk.rows[0].cells[j]
        cell.width = rk_widths[j]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    rk_data = [
        ("K1: ST-GCN túltanulás kis pozitív mintán", "Algoritmikus / Adat", "Közepes", "Magas", "Megelőzés: Erőteljes geometriai és temporális adatbővítés (DropGraph, tükrözés, időskálázás ±20%).\\nB-terv: DropBlock reguláció alkalmazása, vagy transzfertanulás NTU-RGB+D súlyokból."),
        ("K2: Sebességvesztés Raspberry Pi-n", "Hardver / Teljesítmény", "Közepes", "Közepes", "Megelőzés: INT8 poszt-tanítási kvantálás, NCNN C++ futtatókörnyezet ARM NEON SIMD optimalizációval.\\nB-terv: Adaptív képkocka-átugrás (Frame Skipping): pózbecslés minden 2. frame-en (12,5 FPS)."),
        ("K3: Kameraszög- és perspektíva torzulás", "Módszertani", "Magas", "Közepes", "Megelőzés: Relatív, anatómiai méretekkel skálázott jellemzők prioritása a fix képpontos küszöbökkel szemben.\\nB-terv: Felhasználói 2 pontos kalibrációs modul beépítése homográfia transzformációval."),
        ("K4: Kulcspontvesztés tartós kitakaráskor", "Észlelési / Szenzor", "Közepes", "Magas", "Megelőzés: Zuhanási előzménymemória és hiszterézises állapotmegőrzés a kiesés idejére.\\nB-terv: ST-GCN időbeli rekurziójának kiterjesztése LSTM/GRU réteggel a felsőtest-trajektóriára."),
        ("K5: Memóriaszivárgás 24/7 futás során", "Szoftverarchitektúra", "Alacsony", "Magas", "Megelőzés: Profilozás tracemalloc-kal, explicit memóriafelszabadítás minden ciklusban.\\nB-terv: Rendszerszintű systemd watchdog és automatikus izolált folyamat-újraindítás.")
    ]

    for i, row in enumerate(rk_data):
        for j, val in enumerate(row):
            cell = table_rk.rows[i+1].cells[j]
            cell.width = rk_widths[j]
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.0)
            if j == 0:
                run.bold = True
            elif j in (2, 3):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            bg_color = "F8FAFC" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)

    p_cap_rk = doc.add_paragraph()
    p_cap_rk.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_rk.paragraph_format.space_before = Pt(4)
    p_cap_rk.paragraph_format.space_after = Pt(12)
    r_cap_rk = p_cap_rk.add_run("7.2. táblázat: A Szakdolgozat 2 projekt kockázatelemzési és hibaelhárítási mátrixa.")
    r_cap_rk.font.size = Pt(10)
    r_cap_rk.font.italic = True
    r_cap_rk.font.color.rgb = COLOR_MUTED

    add_heading_2("7.4 Nagymintás kísérleti és validációs protokoll")
    doc.add_paragraph(
        "A szakdolgozati kutatás hitelességének sarokköve a mérési eredmények reprodukálhatósága és a statisztikai megalapozottság.\\n\\n"
        "1. Adatbázisok és eloszlásuk:\\n"
        "• URFD (University of Rzeszow Fall Dataset): 30 valós esési felvétel és 40 összetett hétköznapi tevékenység (ADL) monokuláris RGB és mélységi kameraállásokkal [3].\\n"
        "• Le2i Fall Detection Dataset: 191 videó négy különböző helyiségben (Home, Coffee Room, Office, Lecture Room) változatos megvilágítási viszonyok és optikai reflexiók mellett [4].\\n"
        "• Független segédeszközös teszthalmaz: 15 tesztvideó kifejezetten idősotthoni segédeszközökkel (járókeret, kerekesszék, mankó).\\n\\n"
        "2. Osztályozási és megbízhatósági metrikák:\\n"
        "A rendszerteljesítmény számszerűsítésére alkalmazott nemzetközi szabványos metrikák:\\n"
        "• Érzékenység / Szenzitivitás: TPR = TP / (TP + FN)\\n"
        "• Precízió: PPV = TP / (TP + FP)\\n"
        "• Harmonikus átlag: F1 = 2 · (PPV · TPR) / (PPV + TPR)\\n"
        "• Téves Pozitív Ráta: FPR = FP / (FP + TN)\\n"
        "• Görbe alatti terület: ROC-AUC és PR-AUC görbék felvétele a küszöbök mentén.\\n"
        "• Döntési késleltetés: T_latency = T_detect - T_impact másodperc-alapú statisztikája.\\n\\n"
        "3. Hardveres és beágyazott mérési metrikák:\\n"
        "A Raspberry Pi 5 hardveren futtatott tesztek során rögzítendő fizikai paraméterek: átviteli sebesség (FPS átlag, szórás, p95), "
        "komponensenkénti futásidő (ms), memóriafoglalás (RSS MB), processzorterhelés (%) és a SoC maghőmérséklete (°C)."
    )

    doc.add_page_break()

    # =========================================================================
    # IRODALOMJEGYZÉK
    # =========================================================================
    add_heading_1("Irodalomjegyzék")

    references = [
        "[1] S. Yan, Y. Xiong, D. Lin: Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition. In: Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 32, No. 1, 2018.",
        "[2] G. Jocher, A. Chaurasia, J. Qiu: Ultralytics YOLOv8 Architecture and Pose Estimation. Ultralytics Documentation, 2023. https://docs.ultralytics.com",
        "[3] B. Kwolek, M. Kepski: Human fall detection on embedded platform using depth maps and wireless accelerometer. Computer Methods and Programs in Biomedicine, 117(3):489-501, 2014.",
        "[4] I. Charfi, J. Miteran, J. Dubois, M. Atri, R. Tourki: Optimized Spatio-Temporal Descriptors for Real-Time Fall Detection: Comparison of Support Vector Machine and AdaBoost-Based Classification. Journal of Electronic Imaging, 22(4):041106, 2013.",
        "[5] World Health Organization: Step Safely: Strategies for preventing and managing falls across the life-course. Geneva: WHO Guidelines Approved by the Guidelines Review Committee, 2021.",
        "[6] D. Wild, U. S. Nayak, B. Isaacs: How dangerous are falls in old people at home?. British Medical Journal (Clinical Research Ed.), 282(6260):266-268, 1981.",
        "[7] M. E. Tinetti, W. L. Liu, E. B. Claus: Predictors and prognosis of inability to get up after falls among elderly persons. JAMA: The Journal of the American Medical Association, 269(1):65-70, 1993.",
        "[8] Intel Corporation: OpenVINO Toolkit: Deep Learning Deployment Framework and Action Recognition Models. Intel Technical Documentation, 2022.",
        "[9] Microsoft Corporation: ONNX Runtime: Cross-platform, high performance ML inferencing and training accelerator. 2023. https://onnxruntime.ai",
        "[10] C. Rougier, J. Meunier, A. St-Arnaud, J. Rousseau: Robust Video Surveillance for Fall Detection Based on 3D Head Trajectory Analysis. IEEE Transactions on Circuits and Systems for Video Technology, 21(9):1232-1241, 2011.",
        "[11] H. Foroughi, A. Rezvanian, A. Paziraee: Robust fall detection using eigenspaces and upper bound shape features. In: 2008 8th IEEE International Conference on Computer and Information Technology, pp. 721-726, 2008.",
        "[12] Z. Cao, G. Hidalgo, T. Simon, S.-E. Wei, Y. Sheikh: OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields. IEEE Transactions on Pattern Analysis and Machine Intelligence, 43(1):172-186, 2019.",
        "[13] Európai Parlament és Tanács: Az Európai Parlament és a Tanács (EU) 2016/679 rendelete (Általános Adatvédelmi Rendelet - GDPR). Hivatalos Lapja az Európai Uniónak, L 119, 2016.",
        "[14] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollár, C. L. Zitnick: Microsoft COCO: Common Objects in Context. In: European Conference on Computer Vision (ECCV), pp. 740-755, Springer, 2014.",
        "[15] ARM Limited: Arm Cortex-A Programmer's Guide for ARMv8-A: NEON Technology and Advanced SIMD Architecture. Arm Technical Reference Manual, 2020."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        run_ref = p_ref.add_run(ref)
        run_ref.font.name = 'Times New Roman'
        run_ref.font.size = Pt(10)
'''

# Update generate_approved_docx.py
with open(GEN_PATH, "r", encoding="utf-8") as f:
    gen_content = f.read()

target_save = "    # Mentés a célútvonalakra"
if target_save in gen_content:
    if "7. FEJEZET: KUTATÁSI ÉS KÍSÉRLETI TERV A SZAKDOLGOZAT 2 FÉLÉVRE" not in gen_content:
        new_gen = gen_content.replace(target_save, ch7_docx_code + "\n" + target_save)
        with open(GEN_PATH, "w", encoding="utf-8") as f:
            f.write(new_gen)
        print("[OK] Chapter 7 and Bibliography added to generate_approved_docx.py")
    else:
        print("[INFO] Chapter 7 already present in generate_approved_docx.py")
else:
    print("[ERROR] target_save not found in generate_approved_docx.py")
