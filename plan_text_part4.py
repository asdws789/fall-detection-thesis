# -*- coding: utf-8 -*-
"""
Part 4 of the Thesis Research & Implementation Plan
Contains:
- 10. Részletes 14 hetes ütemterv, sprint-terv és mérföldkövek
- 11. Kockázatelemzés és mitigációs stratégia
- 12. Adatvédelmi, jogi és etikai megfontolások
- 13. A végleges szakdolgozat tervezett fejezeti felépítése
- 14. Kiterjedt tudományos hivatkozásjegyzék
"""

PART4_MD = r"""## 10. Részletes 14 hetes ütemterv, sprint-terv és mérföldkövek

A kutatás és megvalósítás egy szabványos egyetemi félév 14 hetes időtartamára van ütemezve, kéthetes sprintciklusokba szervezve:

### 10.1 Heti bontású munkaterv (Sprints & Tasks)

| Hét / Sprint | Fókuszterület | Konkrét technikai feladatok | Heti mérföldkő és kimenet |
| :---: | :--- | :--- | :--- |
| **1–2. hét**<br>(Sprint 1) | **Irodalomkutatás és környezet-előkészítés** | * ST-GCN, YOLOv8-Pose és az akciófelismerési alapcikkek részletes feldolgozása.<br>* Fejlesztői környezet kiépítése (Python 3.11, PyTorch CUDA, OpenCV, Ultralytics telepítés).<br>* Részletes kutatási terv véglegesítése a témavezetővel. | Működő GPU-s fejlesztői környezet, jóváhagyott témaleírás és irodalomjegyzék Zoteróban. |
| **3. hét**<br>(Sprint 2A) | **Pózbecslő és követő pipeline megvalósítása** | * Ultralytics YOLOv8-Pose tesztelése minta videókon.<br>* ByteTrack követő integrálása: személy-ID stabilitás tesztelése.<br>* Kinyerő szkript (`extract_skeletons.py`) megírása, amely videóból `.npy` fájlba menti a koordinátákat és konfidenciákat. | Működő, tesztelt vázkinyerő és követő programkód. |
| **4. hét**<br>(Sprint 2B) | **Referencia adatbázisok beszerzése és feldolgozása** | * RWF-2000 és CCTV-Fights adathalmazok letöltése, integritás-ellenőrzése.<br>* Kötegelt (Batch) vázkinyerés futtatása a letöltött videókon.<br>* Minőségellenőrzés: hibás, üres vagy elcsúszott vázak automatikus szűrése. | Strukturált váz-adathalmaz (train/val/test könyvtárakban, bináris formátumban). |
| **5. hét**<br>(Sprint 3A) | **Adat-előkészítés és PyTorch DataLoader** | * Normalizálási algoritmus (csípőközép origó, törzshossz skálázás) kódolása.<br>* Csúszóablak képző modul ($T=48$ képkocka, átfedések kezelése).<br>* PyTorch Dataset és DataLoader osztályok megírása adatbővítéssel (rotáció, tükrözés, jitter). | Hatékony, GPU-ra optimalizált PyTorch DataLoader pipeline. |
| **6. hét**<br>(Sprint 3B) | **Baseline modellek felépítése és mérése** | * Ízületi szögek és deriváltak (szögsebesség, szöggyorsulás) kiszámítása.<br>* Random Forest és XGBoost modellek betanítása és keresztvalidációja.<br>* Szekvenciális LSTM baseline megvalósítása és első metrikák (F1-score) rögzítése. | Dokumentált baseline eredmények összehasonlító táblázatban. |
| **7. hét**<br>(Sprint 4A) | **ST-GCN architektúra építése (PyTorch)** | * COCO-17 anatómiai szomszédsági mátrixok implementálása.<br>* Spatial Graph Convolution és Temporal Convolution rétegek megírása (vagy PYSKL adaptálása).<br>* Teljes 9-blokkos ST-GCN hálózat összeállítása, ellenőrzése mesterséges tenzorral. | Forduló és futtatható ST-GCN modell hálózati topológia. |
| **8. hét**<br>(Sprint 4B) | **ST-GCN tanítás és hiperparaméter-hangolás** | * Modell tanítása Focal Loss veszteségfüggvénnyel és Cosine Annealing ütemezővel.<br>* Kétáramú (Two-Stream: Joint + Bone) kiterjesztés betanítása.<br>* Tanulási görbék (Loss, F1) naplózása TensorBoardban, Early Stopping alkalmazása. | Betanított súlyfájlok (`best_stgcn_joint.pth`, `best_stgcn_bone.pth`). |
| **9. hét**<br>(Sprint 5A) | **Modell kiértékelés és benchmark elemzés** | * Teszthalmazos kiértékelés: Accuracy, Precision, Recall, Macro F1, ROC-AUC.<br>* Konfúziós mátrixok generálása az ST-GCN és a baseline modellek között (RQ1, RQ2 igazolása).<br>* Időablak-érzékenység ($T=16, 32, 48, 64$) vizsgálata. | Részletes kísérleti eredménytáblázatok és publikációs minőségű ábrák. |
| **10. hét**<br>(Sprint 5B) | **Saját szórakozóhelyi tesztek és hibaelemzés** | * Saját szimulált felvételek rögzítése (tánc, lökdösődés, verekedés, stroboszkóp).<br>* Stresszteszt: modell tesztelése a saját készleten; tánc vs. verekedés hibaelemzés.<br>* Takarások és gyenge fény hatásának számszerűsítése (H2, H3 vizsgálata). | Validált szórakozóhelyi teszteredmények, strukturált hibaelemzési fejezet. |
| **11. hét**<br>(Sprint 6A) | **Valós idejű prototípus és demó alkalmazás** | * Többszálú valós idejű feldolgozó motor (Real-time Worker) megírása.<br>* Hiszterézis és False Positive Suppression algoritmus integrálása.<br>* Operátori vizualizációs nézet (színes vázak, riasztási villogás, FPS számláló).<br>* Futásidő profilozás (RQ3, H4 igazolása). | Interaktív, futtatható demonstrációs szoftver (Webcam / RTSP / Videó bemenettel). |
| **12. hét**<br>(Sprint 6B) | **Eredmények szintetizálása és fejezetvázlatok** | * Összes mérési adat, táblázat és diagram véglegesítése.<br>* Szakdolgozati eredményfejezetek szövegezése, forráskód refaktorálás és GitHub repo rendszerezés. | Elkészült eredmény- és megvalósítási fejezetek, témavezetői előzetes áttekintés. |
| **13. hét**<br>(Sprint 7A) | **Szakdolgozat teljes szövegének megírása** | * Bevezetés, elméleti háttér, rendszerarchitektúra, mérések és konklúzió összefűzése.<br>* Formázás az egyetemi formai követelményeknek megfelelően.<br>* Hivatkozások és ábrajegyzék ellenőrzése. | A szakdolgozat teljes, összefüggő első piszkozata (Draft v1.0). |
| **14. hét**<br>(Sprint 7B) | **Lektorálás, finomhangolás és beadás** | * Témavezetői és konzultensi visszajelzések beépítése.<br>* Nyelvi, helyesírási és formai javítások, plágium-ellenőrzés előkészítése.<br>* Demó videó és prezentációs anyag elkészítése a védéshez. | Végleges, beadásra kész szakdolgozat (PDF és forráskód csomag). |

### 10.2 Fő mérföldkövek (Milestones) és átvételi kritériumok

1. **M1 Mérföldkő (3. hét) – Működő Kulcspont-kinyerés és Követés:**  
   *Kritérium:* A script tetszőleges videóból stabilan, személyenkénti azonosítókkal menti a 17 kulcspontot legalább 25 FPS feldolgozási sebességgel.
2. **M2 Mérföldkő (6. hét) – Validált Baseline Eredmények:**  
   *Kritérium:* A kinematikai jellemzőkre épülő Random Forest és LSTM modellek betanítva, F1-score és konfúziós mátrix rögzítve az RWF-2000 készleten.
3. **M3 Mérföldkő (8. hét) – Betanított és Konvergált ST-GCN Modell:**  
   *Kritérium:* A gráfkonvolúciós modell hibája konvergált, túltanulás kizárva (Early Stopping), és szignifikánsan felülmúlja a baseline modellek F1-értékét.
4. **M4 Mérföldkő (10. hét) – Szórakozóhelyi Stresszteszt és Adatbázis:**  
   *Kritérium:* A saját szimulált szórakozóhelyi videók rögzítve, vázak kinyerve, és a tánc vs. verekedés diszkriminációs pontosság számszerűsítve.
5. **M5 Mérföldkő (11. hét) – Valós Idejű Demonstrációs Prototípus:**  
   *Kritérium:* A rendszer élő videófolyamon vagy kamerán késleltetésmentesen fut, vizuálisan kirajzolja az állapotot, és hiszterézissel szűrt riasztást ad.
6. **M6 Mérföldkő (14. hét) – Végleges Szakdolgozat és Forráskód:**  
   *Kritérium:* Formailag és tartalmilag kifogástalan, egyetemi követelményeknek megfelelő dolgozat, reprodukálható GitHub repository-val.

---

## 11. Kockázatelemzés és mitigációs stratégia

A projekt sikeres és határidőre történő megvalósítása érdekében azonosítottuk a potenciális technikai, módszertani és időgazdálkodási kockázatokat:

| Kockázat leírása | Kategória | Valószínűség (1–5) | Hatás (1–5) | Kockázati Pont (V × H) | Megelőző és mitigációs intézkedés | Fallback / B-terv |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **K1: Elégtelen szórakozóhelyi nyilvános adat** | Adat | 4 | 4 | **16 (Magas)** | Nyilvános felügyeleti adatok (RWF-2000, CCTV-Fights) használata gerincként, kiegészítve saját kontrollált megrendezett jelenetekkel. | Ha kevés a szórakozóhelyi adat, a dolgozat fókusza a felügyeleti kamerás erőszakdetekcióra helyeződik, a klubkörnyezet pedig dedikált tesztesetként szerepel. |
| **K2: Tánc miatti magas téves riasztás (False Positives)** | Módszertan | 4 | 4 | **16 (Magas)** | Táncvideók szándékos bevonása a tanító halmazba kemény negatívként; időablak növelése $T \ge 48$-ra; kétlépcsős hiszterézis szűrés. | Szükség esetén egy frekvencia-alapú Fourier előszűrő beépítése, amely detektálja a periodikus ritmust és letiltja a riasztást. |
| **K3: Zajos vázak sűrű tömegben (Occlusion)** | Technológia | 4 | 3 | **12 (Közepes)** | Láthatósági konfidencia ($conf_i$) súlyozása a gráfban; spline interpoláció; ByteTrack alacsony konfidenciájú párosításának kihasználása. | Alsótest kiesése esetén csak a felsőtest 11 ízületére szűkített gráfmodell használata. |
| **K4: Számítási késleltetés valós idejű üzemben** | Teljesítmény | 3 | 4 | **12 (Közepes)** | YOLOv8n (nano) modell használata, FP16 féllebegőpontos inferencia, többszálú képkocka-pufferelés. | Ha a GPU nem bírja, a képkockák ritkítása (Frame Skipping: minden 2. frame feldolgozása), ami felezi a számítási igényt. |
| **K5: Gráfkonvolúciós tanítás elhúzódása / GPU hiány** | Erőforrás | 2 | 4 | **8 (Közepes)** | Google Colab Pro és Kaggle ingyenes GPU-k bevonása; PYSKL referencia-architektúra átvétele saját scratch kód helyett. | Szükség esetén az előre tanított modell finomhangolása (Transfer Learning). |
| **K6: 3-osztályos feladat túl nehéznek bizonyul** | Módszertan | 3 | 2 | **6 (Alacsony)** | Pontos időbeli szegmentációs annotáció és fokozatos tanítás (először 2 osztály, majd finomhangolás 3 osztályra). | Visszalépés a 2-osztályos (Erőszak / Nem erőszak) architektúrára, ami a szakirodalomban teljesen elfogadott BSc szinten. |
| **K7: Személy-ID ugrálás (ID Switches)** | Követés | 3 | 3 | **9 (Közepes)** | BoT-SORT Re-ID vizuális beágyazásainak bekapcsolása a tiszta IoU helyett. | Rövid időablakos ($T=32$) helyi aggregáció, amely kevésbé érzékeny a hosszú távú ID stabilitásra. |
| **K8: Időgazdálkodási csúszás a félév során** | Projekt | 3 | 4 | **12 (Közepes)** | Kéthetes sprintek, szigorú heti mérföldkövek betartása, heti konzultáció a témavezetővel. | A kiegészítő feladatok (pl. 4-osztályos kiterjesztés, PyG saját gráfréteg) elhagyása, fókusz a fő vonalon. |

---

## 12. Adatvédelem, GDPR és etikai megfontolások

A mesterséges intelligenciával támogatott képi megfigyelés társadalmilag és jogilag az egyik legszenzitívebb terület. A szakdolgozat dedikált fejezetben tárgyalja a megoldás adatvédelmi megfelelőségét:

### 12.1 GDPR megfelelőség és a vázalapú feldolgozás személytelensége
Az Európai Unió Általános Adatvédelmi Rendelete (GDPR) 9. cikke értelmében a biometrikus adatok különleges kategóriájú személyes adatnak minősülnek, amelyek kezelése szigorú feltételekhez kötött:
* **Arcfelismerés tilalma a kutatásban:** A rendszer szándékosan és tervezetten nem tartalmaz semmilyen arcfelismerő vagy egyedi azonosításra (Face Recognition / Re-Identification) alkalmas biometrikus modult.
* **Anonimizálás a forrásnál (Privacy by Design):**  
  A feldolgozási láncban az RGB képpontok azonnal törlődnek a memóriából a 17 kulcspont koordinátáinak kinyerése után. A koordináták önmagukban csupán 2D számhármasok ($x, y, conf$), amelyekből az egyén személyazonossága, neme, etnikuma vagy vallási hovatartozása **matematikailag visszafejthetetlen**.
* **Adatminimalizálás elve:** Csak annyi és olyan adatot dolgozunk fel, amely a közvetlen fizikai veszélyhelyzet felismeréséhez elengedhetetlenül szükséges.

### 12.2 Ember-a-hurokban (Human-in-the-Loop) etikai alapelv
A rendszer alapvető tervezési filozófiája, hogy **nem hoz autonóm döntést**, és nem indít el automatizált szankciót:
* A rendszer egy **intelligens döntéstámogató asszisztens** a biztonsági operátor számára.
* Riasztás esetén felhívja az ember figyelmét a gyanús képernyőre, de a helyszíni beavatkozásról vagy a hatóságok értesítéséről kizárólag a képzett humán operátor dönt.
* Ez megvédi a vendégeket az esetleges téves riasztásokból adódó indokolatlan intézkedésektől.

---

## 13. A végleges szakdolgozat tervezett fejezeti felépítése

A végleges szakdolgozat terjedelme a tervek szerint ~65-75 oldal lesz, az alábbi struktúrában és oldalszám-allokációval:

* **Címlap, Tartalomjegyzék, Nyilatkozatok, Absztrakt (magyar/angol)** (~4 oldal)
* **1. Bevezetés és Problémafelvetés** (~6-8 oldal)
  * 1.1 A szórakozóhelyi biztonságvédelem kihívásai
  * 1.2 Az automatizált viselkedéselemzés szerepe
  * 1.3 Kutatási célkitűzések, kérdések és hipotézisek
  * 1.4 A dolgozat szerkezeti áttekintése
* **2. Szakirodalmi Áttekintés és Elméleti Háttér** (~14-16 oldal)
  * 2.1 Erőszakfelismerési módszerek fejlődése a számítógépes látásban
  * 2.2 Emberi pózbecslés: felülről-lefelé és alulról-felfelé építkező rendszerek
  * 2.3 A YOLOv8-Pose belső architektúrája és OKS veszteségfüggvénye
  * 2.4 Többszemélyes objektumkövetés (MOT: ByteTrack, BoT-SORT)
  * 2.5 Gráfkonvolúciós hálózatok és az ST-GCN matematikai formalizmusa
* **3. Rendszerterv és Szórakozóhely-specifikus Megoldások** (~12-14 oldal)
  * 3.1 A domain-specifikus kihívások elemzése (tánc, takarás, fény, kameraszög)
  * 3.2 A feldolgozási folyamat moduláris architektúrája
  * 3.3 Normalizálási transzformációk és tenzorkonstrukció
  * 3.4 Időbeli simítás, hiszterézis és téves riasztások elnyomása
  * 3.5 Adatbővítési stratégiák váz-gráfokon
* **4. Kísérleti Eredmények és Kiértékelés** (~16-18 oldal)
  * 4.1 A felhasznált adathalmazok (RWF-2000, CCTV-Fights, saját adatok)
  * 4.2 Baseline modellek eredményei (Random Forest, LSTM)
  * 4.3 Az ST-GCN modell tanítása és validációja (Ablation study, Two-Stream fúzió)
  * 4.4 Szórakozóhelyi stressztesztek (Tánc vs. Verekedés, stroboszkóphatás mérése)
  * 4.5 Korai előrejelzési ablak vizsgálata (RQ4 válaszadás)
  * 4.6 Számítási teljesítmény és késleltetési profilozás (RQ3 válaszadás)
* **5. Prototípus Implementáció és Demonstráció** (~8-10 oldal)
  * 5.1 Szoftvertechnológiai komponensek és architektúra
  * 5.2 Többszálú valós idejű feldolgozó motor működése
  * 5.3 Az operátori kezelőfelület (Dashboard) bemutatása esettanulmányokon
* **6. Adatvédelmi, Jogi és Etikai Megfontolások** (~4-5 oldal)
  * 6.1 GDPR megfelelőség és az arcmentes vázfeldolgozás
  * 6.2 Etikai normák és a Human-in-the-Loop paradigma
* **7. Összegzés és Továbbfejlesztési Lehetőségek** (~4-5 oldal)
  * 7.1 A kutatási hipotézisek kiértékelése
  * 7.2 Mérnöki és tudományos konklúziók
  * 7.3 Továbbfejlesztési irányok (3D vázak, Edge AI telepítés)
* **Irodalomjegyzék, Ábrajegyzék, Táblázatjegyzék, Függelék** (~6-8 oldal)

---

## 14. Kiterjedt tudományos hivatkozásjegyzék

1. Yan, S., Xiong, Y., & Lin, D. (2018). Spatial temporal graph convolutional networks for skeleton-based action recognition. *Proceedings of the AAAI Conference on Artificial Intelligence*, 32(1), 7444–7452. https://arxiv.org/abs/1801.07455
2. Jocher, G., Chaurasia, A., & Qiu, J. (2023). Ultralytics YOLOv8 (Version 8.0.0) [Computer software]. https://github.com/ultralytics/ultralytics
3. Maji, D., Nagori, S., Mathew, M., & Poddar, D. (2022). YOLO-Pose: Enhancing YOLO for multi-person pose estimation using object keypoint similarity loss. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops*, 2637–2646. https://arxiv.org/abs/2204.06806
4. Zhang, Y., Sun, P., Dong, Y., Dong, H., Lu, W., Zhou, Z., Zhang, Z., & Luo, J. (2022). ByteTrack: Multi-object tracking by associating every detection box. *European Conference on Computer Vision (ECCV)*, 1–21. https://arxiv.org/abs/2110.06864
5. Aharon, N., Orfaig, R., & Bobrovsky, B. Z. (2022). BoT-SORT: Robust associations multi-pedestrian tracker. *arXiv preprint arXiv:2206.14651*.
6. Duan, H., Wang, J., Chen, K., & Lin, D. (2022). PYSKL: Towards good practices for skeleton action recognition. *Proceedings of the 30th ACM International Conference on Multimedia*, 7351–7354. https://arxiv.org/abs/2205.09443
7. Shi, L., Zhang, Y., Cheng, J., & Lu, H. (2019). Two-stream adaptive graph convolutional networks for skeleton-based action recognition. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 12026–12035.
8. Cheng, M., Cai, K., & Li, M. (2020). RWF-2000: An open large scale video database for violence detection. *25th International Conference on Pattern Recognition (ICPR)*, 4183–4190. https://arxiv.org/abs/1911.05913
9. Perez, M., Kot, A. C., & Rocha, A. (2019). Detection of real-world fights in surveillance videos. *IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2662–2666.
10. Sultani, W., Chen, C., & Shah, M. (2018). Real-world anomaly detection in surveillance videos. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 6479–6488. https://arxiv.org/abs/1801.04264
11. Liu, J., Shahroudy, A., Perez, M., Wang, G., Duan, L. Y., & Kot, A. C. (2020). NTU RGB+D 120: A large-scale benchmark for 3D human activity analysis. *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)*, 42(10), 2684–2701.
12. Yang, H., Ren, Z., Yuan, H., Wei, W., Zhang, Q., & Zhang, Z. (2022). Multi-scale and attention enhanced graph convolution network for skeleton-based violence action recognition. *Frontiers in Neurorobotics*, 16, 1091361. https://doi.org/10.3389/fnbot.2022.1091361
13. Aung, S. T. Y., Kusakunniran, W., & Hooi, Y. K. (2025). Leveraging fusion methods of human pose and motion dynamics for accurate violence detection in video surveillance. *IEEE Access*, 13, 14210–14225.
14. Aparicio Borjas, L. A., Nieto, V. E., Vasquez, J. I., Fernandez-Vazquez, A., & Alvarez Hernandez, G. A. (2026). Human activity recognition method for moderate violence detection. *arXiv preprint arXiv:2605.02659*.
15. San Miguel, J. C., & Garcia-Cobo, G. (2021). Human skeletons and change detection for efficient violence detection in surveillance videos. *Source Code Repository: github.com/atmguille/Violence-Detection-With-Human-Skeletons*.
16. Kipf, T. N., & Welling, M. (2017). Semi-supervised classification with graph convolutional networks. *International Conference on Learning Representations (ICLR)*. https://arxiv.org/abs/1609.02907
17. Lin, T. Y., Goyal, P., Girshick, R., He, K., & Dollár, P. (2017). Focal loss for dense object detection. *Proceedings of the IEEE International Conference on Computer Vision (ICCV)*, 2980–2988.
18. Feichtenhofer, C., Fan, H., Malik, J., & He, K. (2019). SlowFast networks for video recognition. *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 6202–6211.
19. Carreira, J., & Zisserman, A. (2017). Quo vadis, action recognition? A new model and the kinetics dataset. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 6299–6308.
20. Cao, Z., Hidalgo, G., Simon, T., Wei, S. E., & Sheikh, Y. (2019). OpenPose: Realtime multi-person 2D pose estimation using part affinity fields. *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)*, 43(1), 172–186.
"""

print("Part 4 defined successfully.")
