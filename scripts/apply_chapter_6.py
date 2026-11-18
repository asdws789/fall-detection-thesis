# -*- coding: utf-8 -*-
"""
Script to apply Chapter 6 to:
1. docs/szakdolgozat_dokumentum.md
2. docs/szakdolgozat.tex
3. scripts/generate_approved_docx.py
And regenerate the approved docx.
"""

import os
import re

MD_PATH = r"C:\uni_stuff\anti_thesis\docs\szakdolgozat_dokumentum.md"
TEX_PATH = r"C:\uni_stuff\anti_thesis\docs\szakdolgozat.tex"
GEN_PATH = r"C:\uni_stuff\anti_thesis\scripts\generate_approved_docx.py"

# =========================================================================
# 1. MARKDOWN CHAPTER 6 CONTENT
# =========================================================================
md_ch6 = """## 6. Beágyazott peremhálózati megvalósítás és kitekintés: Raspberry Pi platform

A kutatás és rendszertervezés kiemelt célja, hogy a kidolgozott vizuális viselkedéselemző és esésdetektáló rendszer ne csupán nagyteljesítményű asztali számítógépeken, hanem költséghatékony, alacsony fogyasztású, autonóm beágyazott céleszközökön (*Edge AI* hardvereken) is üzemeltethető legyen. Jelen fejezet kitekintést nyújt a rendszer beágyazott platformra – kiemelten a Raspberry Pi mikroszámítógép-családra – történő kiterjesztésének mérnöki feltételeiről, a megvalósítás előtt álló számítási és architektúrális kihívásokról, a tervezett modelloptimalizációs eljárásokról, valamint a peremhálózati IoT integrációról. A fejezetben szereplő mikroszámítógépes futási paraméterek a nemzetközi szakirodalom és az architektúra-specifikus benchmarkok alapján kalkulált megvalósíthatósági becslések, amelyek empirikus mérésekkel történő verifikációja a Szakdolgozat 2 félév feladatát képezi.

### 6.1 A beágyazott peremhálózati (Edge AI) feldolgozás motivációja és adatvédelmi jelentősége

Az idősellátásban és az otthoni felügyeleti rendszerekben a számítási feladatok fizikai helye alapvetően meghatározza a rendszer társadalmi elfogadottságát, üzemeltetési költségét és megbízhatóságát. A hagyományos távfelügyeleti megoldások a nyers kameraképet központi felhőszerverekre továbbítják gépi látási elemzés céljából. Ez a centralizált megközelítés azonban három kritikus mérnöki és etikai akadályba ütközik:
1. **Adatvédelmi és etikai aggályok:** A privát életterekből (hálószoba, nappali, közlekedők) származó folyamatos videostream felhőbe történő kisugárzása súlyos megfigyelési érzetet kelt a gondozottakban, és elfogadhatatlan adatvédelmi (GDPR) kockázatot hordoz egy esetleges hálózati adatlopás, szerveroldali biztonsági incidens vagy illetéktelen hozzáférés esetén.
2. **Hálózati sávszélesség és rendelkezésre állás:** A folyamatos nagyfelbontású videostreamelés jelentős hálózati sávszélességet igényel. Lakossági környezetben a vezeték nélküli (Wi-Fi) kapcsolat minősége ingadozhat, a sávszélesség lecsökkenhet, és egy átmeneti internetkimaradás esetén a vészjelzés el sem jut a felhőbe, ami közvetlen életveszélyt idéz elő.
3. **Üzemeltetési költség és skálázhatóság:** Több száz vagy ezer háztartás párhuzamos videófolyamainak felhőalapú GPU-infrastruktúrán történő valós idejű feldolgozása aránytalanul magas és folyamatos szerverbérleti díjakkal jár.

Ezzel szemben a **beágyazott peremhálózati (Edge AI)** architektúra a feldolgozási lánc teljes egészét a felügyelt helyiségben elhelyezett kisméretű, autonóm mikroszámítógépen valósítja meg. A koncepció alapköve a **zéró videóstreamelés (*Zero Video Streaming*) elve**:
* A képi információ kizárólag a helyi mikroszámítógép operatív memóriájában (RAM) létezik ideiglenes pufferként az inferencia időtartama alatt (néhány tíz ezredmásodpercig).
* A pózbecslő réteg a csontváz-kulcspontok sikeres regresszióját követően azonnal és visszavonhatatlanul felülírja vagy felszabadítja a képi memóriát (*Privacy-by-Design*).
* A helyi hálózatra kizárólag eseményvezérelt, minimális sávszélesség-igényű, anonim JSON telemetriai adatcsomagok kerülnek ki (pl. esés ténye, időbélyeg, mozgási megbízhatóság), képi vagy biometrikus adat soha nem hagyja el a fizikai eszközt.
* A rendszer hálózati kapcsolat hiányában is autonóm módon működőképes marad, és közvetlenül képes aktiválni a helyi hardveres vészjelzést.

### 6.2 Hardverplatform-elemzés és összehasonlítás

A beágyazott céleszköz kiválasztásakor az optimális egyensúly megteremtése a cél a számítási teljesítmény, az energiafogyasztás, a hűtési igény és a hardverköltség között. Tervezett beágyazott célhardverként a Raspberry Pi platformot vizsgáljuk meg, kiemelten a modern **Raspberry Pi 5** és a széles körben elterjedt **Raspberry Pi 4B** modelleket, összevetve azokat a fejlesztői asztali számítógép architektúrájával.

#### 6.2.1 Architektúrális jellemzők
* **Fejlesztői asztali számítógép:** x86_64 architektúrájú, 6 fizikai maggal és 12 szálas párhuzamosítással rendelkező asztali processzor (3,60–4,20 GHz), fejlett AVX2 SIMD vektoros utasításkészlettel, 16 GB DDR4 memóriával (25,6 GB/s sávszélesség) és 65 W termikus tervezési teljesítménnyel (TDP).
* **Raspberry Pi 5:** Broadcom BCM2712 rendszerchip (SoC), amely négy 64 bites ARM Cortex-A76 magot tartalmaz 2,40 GHz-es órajelen. Az ARMv8.2-A architektúra korszerű Neon SIMD kiterjesztéseket, valamint hardveres INT8 dot-product pontműveleteket támogat. A memóriabusz LPDDR4X típusú (128 bites szélesség, ~17 GB/s elméleti sávszélesség), maximális fogyasztása aktív terhelés mellett mindössze 12 W körül alakul. Rendelkezik 2 darab 4 sávos MIPI CSI-2 kamera interfésszel, amely közvetlenül a hardveres képjelfeldolgozó processzorhoz (ISP) kapcsolódik.
* **Raspberry Pi 4B:** Broadcom BCM2711 SoC, négy régebbi generációs ARM Cortex-A72 maggal 1,50 GHz-es órajelen (ARMv8-A architektúra). Memóriája LPDDR4 (~7 GB/s sávszélesség), maximális fogyasztása ~7 W. Kamera interfésze 2 sávos MIPI CSI-2 port.

#### 6.2.2 Hardveres összehasonlító elemzés
A 6.1. táblázat részletesen összegzi a fejlesztői asztali számítógép mért értékeit és a beágyazott mikroszámítógépekre vonatkozó, a nemzetközi szakirodalomból és architektúrális modellekből [2, 8, 15] származtatott becsült futási mutatókat.

**6.1. táblázat: A fejlesztői asztali munkaállomás és a célzott beágyazott mikroszámítógépek összehasonlító elemzése.**

| Paraméter / Jellemző | Fejlesztői asztali PC (x86_64) | Raspberry Pi 5 (ARM Cortex-A76) | Raspberry Pi 4B (ARM Cortex-A72) |
| :--- | :---: | :---: | :---: |
| **Processzor típusa** | Asztali CPU (6 mag / 12 szál) | Broadcom BCM2712 (4 mag) | Broadcom BCM2711 (4 mag) |
| **Architektúra** | x86_64 (AVX2 támogatás) | ARMv8.2-A (NEON, Dot-product) | ARMv8-A (NEON) |
| **Órajel** | 3,60 – 4,20 GHz | 2,40 GHz | 1,50 GHz |
| **Operatív memória** | 16 GB DDR4 (3200 MHz) | 4 GB vagy 8 GB LPDDR4X | 4 GB LPDDR4 |
| **TDP / Fogyasztás** | 65 W (hálózati táplálás) | ~12 W (5V / 5A USB-C) | ~7 W (5V / 3A USB-C) |
| **Hűtési igény** | Ventilátoros asztali borda | Aktív hűtőborda (ventilátoros) | Passzív borda vagy kis ventilátor |
| **Kamera interfész** | USB 3.0 UVC webkamera | 2x 4-sávos MIPI CSI-2 (ISP) | 2-sávos MIPI CSI-2 |
| **Pózbecslő modell** | `yolov8s-pose` (FP32) | `yolov8n-pose` (INT8 ONNX) | `yolov8n-pose` (INT8 NCNN) |
| **Számítási igény** | 28,7 GFLOPs | 8,9 GFLOPs (INT8-ra kvantálva) | 8,9 GFLOPs (INT8-ra kvantálva) |
| **Inferencia idő** | **36,4 ms** *(Saját mérés)* | **~38 – 45 ms** *(Irodalmi becslés)* | **~110 – 140 ms** *(Irodalmi becslés)* |
| **Egyéb overhead (Kin.+GUI)** | **3,9 ms** *(Saját mérés)* | **~3 – 5 ms** *(Becslés, GUI nélkül)* | **~4 – 6 ms** *(Becslés, GUI nélkül)* |
| **Teljes ciklusidő** | **40,3 ms** *(Saját mérés)* | **~42 – 50 ms** *(Irodalmi becslés)* | **~115 – 145 ms** *(Irodalmi becslés)* |
| **Képkockasebesség (FPS)** | **24,8 FPS** *(Saját mérés)* | **~20 – 24 FPS** *(Irodalmi becslés)* | **~7 – 9 FPS** *(Irodalmi becslés)* |
| **Valós idejű alkalmasság** | **Alkalmas** (Határeset: 24,8 FPS) | **Alkalmas** (Optimalizálással) | **Nem alkalmas** (Túl lassú) |

> *Módszertani megjegyzés a 6.1. táblázathoz:* A táblázatban az asztali PC adatai a jelen kutatás során végzett tényleges kísérleti mérések eredményei ($N=1500$ frame átlaga). Ezzel szemben a Raspberry Pi 5 és Raspberry Pi 4B értékei a közzétett hivatalos YOLOv8 beágyazott mérési eredményekre [2], az ARM Cortex-A architektúra-benchmarkokra [15] és az OpenVINO/ONNX beágyazott tesztekre [8] támaszkodó elméleti és szakirodalmi megvalósíthatósági becslések.

A táblázat adatai rámutatnak, hogy a régebbi Raspberry Pi 4B számítási kapacitása (7–9 FPS) nem elegendő a dinamikus esési folyamatok valós idejű felügyeletére. A Raspberry Pi 5 azonban a négymagos Cortex-A76 processzorával, hardveres dot-product utasításaival és gyorsabb memóriabuszkiképzésével eléri a 20–24 FPS becsült sebességet, amely már alkalmas a megbízható valós idejű működésre.

### 6.3 Modelloptimalizációs technikák beágyazott környezetben

Ahhoz, hogy a mélytanulási pózbecslés és az esésdetektálás korlátozott erőforrású mikroszámítógépen is elérje a kívánt képkockasebességet, három lépcsős szoftveres optimalizációs stratégia alkalmazása szükséges.

#### 6.3.1 Architektúra-váltás és a pontosság-sebesség kompromisszum (YOLOv8s → YOLOv8n)
A kutatás első szakaszában, az asztali számítógépen a `yolov8s-pose` (small) modellváltozat került alkalmazásra, amely kiváló lokalizációs stabilitást nyújtott. A beágyazott platform korlátozott memóriasávszélessége és számítási kapacitása azonban megköveteli a könnyített `yolov8n-pose` (nano) hálózat alkalmazását.

A két modell architektúrális és minőségi összehasonlítása:
* **Számítási komplexitás:** A paraméterszám 11,6 millióról 3,3 millióra csökken (71,5%-os csökkenés), míg a lebegőpontos műveletigény 28,7 GFLOPs-ról 8,9 GFLOPs-ra esik vissza $640 \times 480$-as felbontás mellett (kb. 3,2-szer kevesebb művelet).
* **Pontosság-kompromisszum vizsgálata:** A nemzetközi COCO Keypoints 2017 validációs adathalmazon [14] a `yolov8s-pose` modell $56{,}0\%$ átlagos pontosságot ($mAP_{\\text{pose}}^{50:95}$) ér el, míg a `yolov8n-pose` modell pontossága $50{,}4\%$. Ez mintegy 5,6 százalékpontos nominális pontosságvesztést jelent.
* **Mérnöki hatás az esésdetektálásra:** A szakirodalmi és topológiai elemzés alapján a nano modell pontosságcsökkenése döntően az apró, nagy felbontást igénylő és könnyen takarásba kerülő arc-kulcspontok (szemek, fülek, orr), valamint a csuklók és kézfejek lokalizációjánál jelentkezik. Ezzel szemben az esésdetektálás állapotgépe és kinematikai motorja szempontjából meghatározó törzsi kulcspontok (vállak, csípők) és az alsó végtagok nagy ízületei (térdek, bokák) esetében a `yolov8n-pose` megbízhatósága megközelíti a nagyobb modellét. A nagyméretű, globális testtartásváltozások és a vertikális zuhanási sebességbecslés pontossága a nano modell alkalmazásával is megőrizhető, miközben a számítási ciklusidő több mint felére csökken.

#### 6.3.2 Poszt-tanítási INT8 kvantálás (Post-Training Quantization - PTQ)
A konvolúciós neurális hálózatok alapértelmezésben 32 bites egyszeres pontosságú lebegőpontos (FP32) formátumban tárolják a súlyokat és aktivációkat. Beágyazott ARM processzorokon az FP32 műveletek jelentős memóriasávszélességet és aritmetikai órajelet emésztenek fel. A poszt-tanítási INT8 kvantálás célja, hogy a 32 bites lebegőpontos értékeket 8 bites előjeles egész számokká alakítsa, 75%-os memóriamegtakarítást és többszörös számítási gyorsulást biztosítva.

A lebegőpontos érték ($x \\in \\mathbb{R}$) és a kvantált egész ($q \\in \\mathbb{Z}$) közötti afin transzformáció formális matematikai leírása:
$$q = \\text{round}\\left(\\frac{x}{S}\\right) + Z$$
ahol a dekvantálási összefüggés:
$$\\hat{x} = S \\cdot (q - Z)$$
A formulában $S \\in \\mathbb{R}^+$ a valós lebegőpontos skálázási tényező (*scale factor*), $Z \\in \\mathbb{Z}$ pedig a nullapont-eltolás (*zero-point offset*), amely biztosítja, hogy a lebegőpontos nulla érték pontosan leképezhető legyen az egész számok halmazára.

Ha a vizsgált tenzor lebegőpontos értéktartománya $[x_{\\min}, x_{\\max}]$, a kvantált tartomány pedig $[q_{\\min}, q_{\\max}]$ (előjeles INT8 esetén $[-128, 127]$, előjeltelen UINT8 esetén $[0, 255]$), a paraméterek az alábbiak szerint adódnak:
$$S = \\frac{x_{\\max} - x_{\\min}}{q_{\\max} - q_{\\min}}$$
$$Z = \\text{round}\\left(\\frac{-x_{\\min}}{S}\\right) + q_{\\min}$$

*Kvantálási stratégiák a rendszerben:*
1. **Szimmetrikus súlykvantálás:** A hálózati rétegek súlymátrixai esetében a statikus értéktartomány jellemzően szimmetrikus a nulla körül, így a nullapont fixen rögzíthető ($Z = 0$), amely egyszerűsíti a hardveres szorzási láncot.
2. **Aszimmetrikus aktivációkvantálás statikus kalibrációval:** Mivel a ReLU és SiLU aktivációs függvények utáni kimenetek nem szimmetrikusak (nemnegatív tartományba tolódnak), az aktivációknál nemzéró $Z$ eltolást alkalmazunk. A dinamikatartomány ($[x_{\\min}, x_{\\max}]$) empirikus rögzítéséhez egy 200 reprezentatív képkockából álló kalibrációs mintahalmazt futtatunk át a hálózaton (*Post-Training Static Calibration*). A szélsőértékeket Kullback–Leibler (KL) divergencia minimalizálásával optimalizáljuk, elkerülve a telítési és kerekítési hibákból fakadó pontosságvesztést.

#### 6.3.3 Vektorizált ARM NEON utasításkészlet-optimalizáció és futtatókörnyezetek
Az ARM Cortex-A processzormagok dedikált Advanced SIMD (NEON) feldolgozó egységgel rendelkeznek. A NEON architektúra 32 darab 64 bites vagy 16 darab 128 bites vektorregisztert (`q0`–`q15`) biztosít [15].
* **Párhuzamos műveletvégzés:** Egyetlen 128 bites NEON regiszterben egyszerre négy darab 32 bites lebegőpontos (FP32), nyolc darab 16 bites egész (INT16), vagy tizenhat darab 8 bites egész (INT8) adat fér el.
* **Hardveres dot-product utasítások:** A Raspberry Pi 5-ben dolgozó ARMv8.2-A Cortex-A76 mag támogatja az `SDOT` és `UDOT` gépi utasításokat. Ezek az utasítások négy párhuzamos 8 bites előjeles/előjeltelen egész szám szorzatát képezik, és az eredményt egyetlen gépi órajelciklus alatt hozzáadják egy 32 bites akkumulátor-regiszterhez:
$$\\text{Acc} \\leftarrow \\text{Acc} + \\sum_{k=0}^{3} A_k \\cdot B_k$$
Ez a művelet a mély konvolúciós rétegek számítási magját képezi, amely négyszeresére gyorsítja a mátrixszorzások átviteli sebességét az FP32 végrehajtáshoz képest.

A beágyazott Linux operációs rendszeren (Raspberry Pi OS 64-bit) két célszerű futtatókörnyezet illesztését tervezzük:
1. **ONNX Runtime (CPUExecutionProvider):** Képes a PyTorch-ban exportált ONNX modellt futtatni, natív módon kiaknázva az ARM NEON és OpenMP többmagos szálkezelési lehetőségeit [9].
2. **Tencent NCNN motor:** Kifejezetten mobil és beágyazott ARM platformokra optimalizált, minimális memóriaigényű C++ keretrendszer, amely közvetlen assembly-szintű NEON rutinokat tartalmaz, teljesen kiküszöbölve a Python futtatókörnyezet többletterhelését.

### 6.4 Tervezett peremhálózati architektúra és IoT integráció

A kutatás távlati célja egy teljesen autonóm, közvetlenül telepíthető intelligens esésdetektáló szenzorcsomópont hardveres és szoftveres prototípusának megvalósítása.

#### 6.4.1 A fizikai céleszköz felépítése
A hardvercsomópont főbb fizikai elemei:
* **Központi egység:** Raspberry Pi 5 egykártyás mikroszámítógép aktív ventilátoros hűtőbordával, amely megakadályozza a processzormagok termikus órajel-visszaszabályozását (*thermal throttling*) tartós, 100%-os terhelés mellett is.
* **Kameramodul:** Raspberry Pi Camera Module 3, amely egy nagylátószögű (Wide, 120° látószögű) objektívvel és Sony IMX708 szenzorral van ellátva. A MIPI CSI-2 buszon keresztül közvetlenül hardveres DMA (*Direct Memory Access*) átvitellel tölti a képkockákat a processzor memóriájába, minimális CPU-overhead mellett.
* **Tápellátás és energiagazdálkodás:** 5V / 5A USB-C PD hálózati tápegység, kiegészítve egy szünetmentes akkumulátormodullal (UPS HAT), amely áramszünet esetén is garantálja a folyamatos felügyeletet legalább 60 percen át.

#### 6.4.2 Helyi hardveres vészjelző alrendszer (Fail-safe Actuator)
A rendszer megbízhatóságának kulcsa, hogy életmentő szituációban nem függhet a helyi Wi-Fi hálózat vagy az internetkapcsolat stabilitásától. Ezért a mikroszámítógép általános célú be-/kimeneti (GPIO) portjára közvetlen hardveres riasztási interfész kapcsolódik:
* Egy tranzisztoros kapcsolófokozattal vezérelt, 85 dB hangnyomású helyi piezo hangjelző (buzzer / sziréna), amely igazolt esés esetén azonnal helyi akusztikus riasztást ad a környezetben tartózkodók vagy a szomszédok számára.
* Egy kétszínű állapotjelző LED: normál működés és sziluettkövetés esetén diszkrét zöld fény, vészhelyzet vagy instabilitás esetén villogó vörös jelzés.
* A GPIO tranzisztor meghajtása közvetlenül a hardveres könyvtáron keresztül történik mikroszekundumos késleltetéssel, megkerülve a hálózati protokollláncot.

#### 6.4.3 IoT telemetriai kommunikáció és üzenetstruktúra
Amennyiben rendelkezésre áll hálózati kapcsolat, a peremhálózati eszköz szabványos, kis sávszélesség-igényű **MQTT (*Message Queuing Telemetry Transport*)** protokollon keresztül kommunikál TLS 1.3 titkosított csatornán a helyi okosotthon-központtal (pl. Home Assistant) vagy a gondozási diszpécserközponttal.

A továbbított telemetriai adatcsomag szigorúan strukturált JSON formátumú, amely nem tartalmaz sem képet, sem biometrikus adatot, eleget téve a beépített adatvédelem (*Privacy-by-Design*, GDPR 25. cikk [13]) előírásainak:

```json
{
  "device_id": "rpi5_room_sensor_01",
  "timestamp": 1716982455.420,
  "event_type": "FALL_DETECTED",
  "severity": "CRITICAL",
  "confidence": 0.94,
  "telemetry": {
    "torso_angle_deg": 78.4,
    "aspect_ratio": 1.45,
    "drop_velocity_vy": 0.62,
    "floor_contact": true,
    "immobility_duration_sec": 3.5
  },
  "heartbeat": {
    "system_fps": 22.4,
    "cpu_temp_celsius": 48.2,
    "uptime_sec": 84200
  }
}
```

Az MQTT architektúra lehetővé teszi, hogy egyetlen lakásban vagy intézményben több diszkrét szobai szenzorcsomópont csatlakozzon egyetlen központi diszpécserpanelhez anélkül, hogy a helyi hálózatot terhelő videófolyamok futnának a háttérben. A peremhálózati koncepció gyakorlati validációja, a mérési adatok rögzítése Raspberry Pi 5 hardveren, valamint az INT8-ra kvantált hálózat és az ST-GCN modell együttes futásának profilozása a Szakdolgozat 2 félév kísérleti programjának szerves részét képezi.
"""

# Update Markdown
with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

ch6_start_md = "## 6. Beágyazott peremhálózati megvalósítás"
ch7_start_md = "## 7. Kutatási és fejlesztési terv"
if ch6_start_md in md_content and ch7_start_md in md_content:
    p1 = md_content.split(ch6_start_md)[0]
    p2 = md_content.split(ch7_start_md)[1]
    new_md = p1 + md_ch6 + "\n\n---\n\n" + ch7_start_md + p2
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(new_md)
    print("[OK] Chapter 6 updated in docs/szakdolgozat_dokumentum.md")
else:
    print("[ERROR] Split points not found in Markdown")

# =========================================================================
# 2. LATEX CHAPTER 6 CONTENT
# =========================================================================
tex_ch6 = r"""\chapter{Beágyazott peremhálózati megvalósítás és kitekintés: Raspberry Pi platform}

A kutatás és rendszertervezés kiemelt célja, hogy a kidolgozott vizuális viselkedéselemző és esésdetektáló rendszer ne csupán nagyteljesítményű asztali számítógépeken, hanem költséghatékony, alacsony fogyasztású, autonóm beágyazott céleszközökön (\textit{Edge AI} hardvereken) is üzemeltethető legyen. Jelen fejezet kitekintést nyújt a rendszer beágyazott platformra -- kiemelten a Raspberry Pi mikroszámítógép-családra -- történő kiterjesztésének mérnöki feltételeiről, a megvalósítás előtt álló számítási és architektúrális kihívásokról, a tervezett modelloptimalizációs eljárásokról, valamint a peremhálózati IoT integrációról. A fejezetben szereplő mikroszámítógépes futási paraméterek a nemzetközi szakirodalom és az architektúra-specifikus benchmarkok alapján kalkulált megvalósíthatósági becslések, amelyek empirikus mérésekkel történő verifikációja a Szakdolgozat 2 félév feladatát képezi.

\section{A beágyazott peremhálózati (Edge AI) feldolgozás motivációja és adatvédelmi jelentősége}
Az idősellátásban és az otthoni felügyeleti rendszerekben a számítási feladatok fizikai helye alapvetően meghatározza a rendszer társadalmi elfogadottságát, üzemeltetési költségét és megbízhatóságát. A hagyományos távfelügyeleti megoldások a nyers kameraképet központi felhőszerverekre továbbítják gépi látási elemzés céljából. Ez a centralizált megközelítés azonban három kritikus mérnöki és etikai akadályba ütközik:
\begin{enumerate}
    \item \textbf{Adatvédelmi és etikai aggályok:} A privát életterekből (hálószoba, nappali, közlekedők) származó folyamatos videostream felhőbe történő kisugárzása súlyos megfigyelési érzetet kelt a gondozottakban, és elfogadhatatlan adatvédelmi (GDPR) kockázatot hordoz egy esetleges hálózati adatlopás, szerveroldali biztonsági incidens vagy illetéktelen hozzáférés esetén.
    \item \textbf{Hálózati sávszélesség és rendelkezésre állás:} A folyamatos nagyfelbontású videostreamelés jelentős hálózati sávszélességet igényel. Lakossági környezetben a vezeték nélküli (Wi-Fi) kapcsolat minősége ingadozhat, a sávszélesség lecsökkenhet, és egy átmeneti internetkimaradás esetén a vészjelzés el sem jut a felhőbe, ami közvetlen életveszélyt idéz elő.
    \item \textbf{Üzemeltetési költség és skálázhatóság:} Több száz vagy ezer háztartás párhuzamos videófolyamainak felhőalapú GPU-infrastruktúrán történő valós idejű feldolgozása aránytalanul magas és folyamatos szerverbérleti díjakkal jár.
\end{enumerate}

Ezzel szemben a \textbf{beágyazott peremhálózati (Edge AI)} architektúra a feldolgozási lánc teljes egészét a felügyelt helyiségben elhelyezett kisméretű, autonóm mikroszámítógépen valósítja meg. A koncepció alapköve a \textbf{zéró videóstreamelés (\textit{Zero Video Streaming}) elve}:
\begin{itemize}
    \item A képi információ kizárólag a helyi mikroszámítógép operatív memóriájában (RAM) létezik ideiglenes pufferként az inferencia időtartama alatt (néhány tíz ezredmásodpercig).
    \item A pózbecslő réteg a csontváz-kulcspontok sikeres regresszióját követően azonnal és visszavonhatatlanul felülírja vagy felszabadítja a képi memóriát (\textit{Privacy-by-Design}).
    \item A helyi hálózatra kizárólag eseményvezérelt, minimális sávszélesség-igényű, anonim JSON telemetriai adatcsomagok kerülnek ki (pl. esés ténye, időbélyeg, mozgási megbízhatóság), képi vagy biometrikus adat soha nem hagyja el a fizikai eszközt.
    \item A rendszer hálózati kapcsolat hiányában is autonóm módon működőképes marad, és közvetlenül képes aktiválni a helyi hardveres vészjelzést.
\end{itemize}

\section{Hardverplatform-elemzés és összehasonlítás}
A beágyazott céleszköz kiválasztásakor az optimális egyensúly megteremtése a cél a számítási teljesítmény, az energiafogyasztás, a hűtési igény és a hardverköltség között. Tervezett beágyazott célhardverként a Raspberry Pi platformot vizsgáljuk meg, kiemelten a modern \textbf{Raspberry Pi 5} és a széles körben elterjedt \textbf{Raspberry Pi 4B} modelleket, összevetve azokat a fejlesztői asztali számítógép architektúrájával.

\subsection{Architektúrális jellemzők}
\begin{itemize}
    \item \textbf{Fejlesztői asztali számítógép:} x86\_64 architektúrájú, 6 fizikai maggal és 12 szálas párhuzamosítással rendelkező asztali processzor (3,60--4,20 GHz), fejlett AVX2 SIMD vektoros utasításkészlettel, 16 GB DDR4 memóriával (25,6 GB/s sávszélesség) és 65 W termikus tervezési teljesítménnyel (TDP).
    \item \textbf{Raspberry Pi 5:} Broadcom BCM2712 rendszerchip (SoC), amely négy 64 bites ARM Cortex-A76 magot tartalmaz 2,40 GHz-es órajelen. Az ARMv8.2-A architektúra korszerű Neon SIMD kiterjesztéseket, valamint hardveres INT8 dot-product pontműveleteket támogat. A memóriabusz LPDDR4X típusú (128 bites szélesség, $\approx 17$ GB/s elméleti sávszélesség), maximális fogyasztása aktív terhelés mellett mindössze 12 W körül alakul. Rendelkezik 2 darab 4 sávos MIPI CSI-2 kamera interfésszel, amely közvetlenül a hardveres képjelfeldolgozó processzorhoz (ISP) kapcsolódik.
    \item \textbf{Raspberry Pi 4B:} Broadcom BCM2711 SoC, négy régebbi generációs ARM Cortex-A72 maggal 1,50 GHz-es órajelen (ARMv8-A architektúra). Memóriája LPDDR4 ($\approx 7$ GB/s sávszélesség), maximális fogyasztása $\approx 7$ W. Kamera interfésze 2 sávos MIPI CSI-2 port.
\end{itemize}

\subsection{Hardveres összehasonlító elemzés}
A \ref{tab:hardware_comp}. táblázat részletesen összegzi a fejlesztői asztali számítógép mért értékeit és a beágyazott mikroszámítógépekre vonatkozó, a nemzetközi szakirodalomból és architektúrális modellekből \cite{yolov8pose, openvino2022, armneon2020} származtatott becsült futási mutatókat.

\begin{table}[H]
\centering
\small
\begin{tabularx}{\textwidth}{lXcc}
\toprule
\textbf{Paraméter / Jellemző} & \textbf{Fejlesztői asztali PC (x86\_64)} & \textbf{Raspberry Pi 5 (ARM Cortex-A76)} & \textbf{Raspberry Pi 4B (ARM Cortex-A72)} \\
\midrule
Processzor típusa & Asztali CPU (6 mag / 12 szál) & Broadcom BCM2712 (4 mag) & Broadcom BCM2711 (4 mag) \\
Architektúra & x86\_64 (AVX2 támogatás) & ARMv8.2-A (NEON, Dot-product) & ARMv8-A (NEON) \\
Órajel & 3,60 -- 4,20 GHz & 2,40 GHz & 1,50 GHz \\
Operatív memória & 16 GB DDR4 (3200 MHz) & 4 GB vagy 8 GB LPDDR4X & 4 GB LPDDR4 \\
TDP / Fogyasztás & 65 W (hálózati táplálás) & $\approx 12$ W (5V / 5A USB-C) & $\approx 7$ W (5V / 3A USB-C) \\
Hűtési igény & Ventilátoros asztali borda & Aktív hűtőborda (ventilátoros) & Passzív borda vagy kis ventilátor \\
Kamera interfész & USB 3.0 UVC webkamera & 2x 4-sávos MIPI CSI-2 (ISP) & 2-sávos MIPI CSI-2 \\
Pózbecslő modell & \texttt{yolov8s-pose} (FP32) & \texttt{yolov8n-pose} (INT8 ONNX) & \texttt{yolov8n-pose} (INT8 NCNN) \\
Számítási igény & 28,7 GFLOPs & 8,9 GFLOPs (INT8-ra kvantálva) & 8,9 GFLOPs (INT8-ra kvantálva) \\
\midrule
Inferencia idő & \textbf{36,4 ms} \textit{(Saját mérés)} & \textbf{$\approx$ 38 -- 45 ms} \textit{(Irodalmi becslés)} & \textbf{$\approx$ 110 -- 140 ms} \textit{(Irodalmi becslés)} \\
Egyéb overhead (Kin.+GUI) & \textbf{3,9 ms} \textit{(Saját mérés)} & \textbf{$\approx$ 3 -- 5 ms} \textit{(Becslés, GUI nélkül)} & \textbf{$\approx$ 4 -- 6 ms} \textit{(Becslés, GUI nélkül)} \\
Teljes ciklusidő & \textbf{40,3 ms} \textit{(Saját mérés)} & \textbf{$\approx$ 42 -- 50 ms} \textit{(Irodalmi becslés)} & \textbf{$\approx$ 115 -- 145 ms} \textit{(Irodalmi becslés)} \\
Képkockasebesség (FPS) & \textbf{24,8 FPS} \textit{(Saját mérés)} & \textbf{$\approx$ 20 -- 24 FPS} \textit{(Irodalmi becslés)} & \textbf{$\approx$ 7 -- 9 FPS} \textit{(Irodalmi becslés)} \\
\midrule
Valós idejű alkalmasság & \textbf{Alkalmas} (Határeset: 24,8 FPS) & \textbf{Alkalmas} (Optimalizálással) & \textbf{Nem alkalmas} (Túl lassú) \\
\bottomrule
\end{tabularx}
\caption{A fejlesztői asztali munkaállomás és a célzott beágyazott mikroszámítógépek összehasonlító elemzése.}
\label{tab:hardware_comp}
\end{table}

\textbf{Módszertani megjegyzés a \ref{tab:hardware_comp}. táblázathoz:} A táblázatban az asztali PC adatai a jelen kutatás során végzett tényleges kísérleti mérések eredményei ($N=1500$ frame átlaga). Ezzel szemben a Raspberry Pi 5 és Raspberry Pi 4B értékei a közzétett hivatalos YOLOv8 beágyazott mérési eredményekre \cite{yolov8pose}, az ARM Cortex-A architektúra-benchmarkokra \cite{armneon2020} és az OpenVINO/ONNX beágyazott tesztekre \cite{openvino2022} támaszkodó elméleti és szakirodalmi megvalósíthatósági becslések.

\section{Modelloptimalizációs technikák beágyazott környezetben}
Ahhoz, hogy a mélytanulási pózbecslés és az esésdetektálás korlátozott erőforrású mikroszámítógépen is elérje a kívánt képkockasebességet, három lépcsős szoftveres optimalizációs stratégia alkalmazása szükséges.

\subsection{Architektúra-váltás és a pontosság-sebesség kompromisszum (YOLOv8s $\to$ YOLOv8n)}
A kutatás első szakaszában, az asztali számítógépen a \texttt{yolov8s-pose} (small) modellváltozat került alkalmazásra, amely kiváló lokalizációs stabilitást nyújtott. A beágyazott platform korlátozott memóriasávszélessége és számítási kapacitása azonban megköveteli a könnyített \texttt{yolov8n-pose} (nano) hálózat alkalmazását.

A két modell architektúrális és minőségi összehasonlítása:
\begin{itemize}
    \item \textbf{Számítási komplexitás:} A paraméterszám 11,6 millióról 3,3 millióra csökken (71,5\%-os csökkenés), míg a lebegőpontos műveletigény 28,7 GFLOPs-ról 8,9 GFLOPs-ra esik vissza $640 \times 480$-as felbontás mellett ($\approx 3,2$-szer kevesebb művelet).
    \item \textbf{Pontosság-kompromisszum vizsgálata:} A nemzetközi COCO Keypoints 2017 validációs adathalmazon \cite{coco2014} a \texttt{yolov8s-pose} modell $56{,}0\%$ átlagos pontosságot ($mAP_{\text{pose}}^{50:95}$) ér el, míg a \texttt{yolov8n-pose} modell pontossága $50{,}4\%$. Ez mintegy 5,6 százalékpontos nominális pontosságvesztést jelent.
    \item \textbf{Mérnöki hatás az esésdetektálásra:} A szakirodalmi és topológiai elemzés alapján a nano modell pontosságcsökkenése döntően az apró, nagy felbontást igénylő és könnyen takarásba kerülő arc-kulcspontok (szemek, fülek, orr), valamint a csuklók és kézfejek lokalizációjánál jelentkezik. Ezzel szemben az esésdetektálás állapotgépe és kinematikai motorja szempontjából meghatározó törzsi kulcspontok (vállak, csípők) és az alsó végtagok nagy ízületei (térdek, bokák) esetében a \texttt{yolov8n-pose} megbízhatósága megközelíti a nagyobb modellét. A nagyméretű, globális testtartásváltozások és a vertikális zuhanási sebességbecslés pontossága a nano modell alkalmazásával is megőrizhető, miközben a számítási ciklusidő több mint felére csökken.
\end{itemize}

\subsection{Poszt-tanítási INT8 kvantálás (Post-Training Quantization -- PTQ)}
A konvolúciós neurális hálózatok alapértelmezésben 32 bites egyszeres pontosságú lebegőpontos (FP32) formátumban tárolják a súlyokat és aktivációkat. Beágyazott ARM processzorokon az FP32 műveletek jelentős memóriasávszélességet és aritmetikai órajelet emésztenek fel. A poszt-tanítási INT8 kvantálás célja, hogy a 32 bites lebegőpontos értékeket 8 bites előjeles egész számokká alakítsa, 75\%-os memóriamegtakarítást és többszörös számítási gyorsulást biztosítva.

A lebegőpontos érték ($x \in \mathbb{R}$) és a kvantált egész ($q \in \mathbb{Z}$) közötti afin transzformáció formális matematikai leírása:
\begin{equation}
q = \text{round}\left(\frac{x}{S}\right) + Z
\end{equation}
ahol a dekvantálási összefüggés:
\begin{equation}
\hat{x} = S \cdot (q - Z)
\end{equation}
A formulában $S \in \mathbb{R}^+$ a valós lebegőpontos skálázási tényező (\textit{scale factor}), $Z \in \mathbb{Z}$ pedig a nullapont-eltolás (\textit{zero-point offset}), amely biztosítja, hogy a lebegőpontos nulla érték pontosan leképezhető legyen az egész számok halmazára.

Ha a vizsgált tenzor lebegőpontos értéktartománya $[x_{\min}, x_{\max}]$, a kvantált tartomány pedig $[q_{\min}, q_{\max}]$ (előjeles INT8 esetén $[-128, 127]$, előjeltelen UINT8 esetén $[0, 255]$), a paraméterek az alábbiak szerint adódnak:
\begin{equation}
S = \frac{x_{\max} - x_{\min}}{q_{\max} - q_{\min}}, \qquad Z = \text{round}\left(\frac{-x_{\min}}{S}\right) + q_{\min}
\end{equation}

\textbf{Kvantálási stratégiák a rendszerben:}
\begin{enumerate}
    \item \textbf{Szimmetrikus súlykvantálás:} A hálózati rétegek súlymátrixai esetében a statikus értéktartomány jellemzően szimmetrikus a nulla körül, így a nullapont fixen rögzíthető ($Z = 0$), amely egyszerűsíti a hardveres szorzási láncot.
    \item \textbf{Aszimmetrikus aktivációkvantálás statikus kalibrációval:} Mivel a ReLU és SiLU aktivációs függvények utáni kimenetek nem szimmetrikusak (nemnegatív tartományba tolódnak), az aktivációknál nemzéró $Z$ eltolást alkalmazunk. A dinamikatartomány ($[x_{\min}, x_{\max}]$) empirikus rögzítéséhez egy 200 reprezentatív képkockából álló kalibrációs mintahalmazt futtatunk át a hálózaton (\textit{Post-Training Static Calibration}). A szélsőértékeket Kullback--Leibler (KL) divergencia minimalizálásával optimalizáljuk, elkerülve a telítési és kerekítési hibákból fakadó pontosságvesztést.
\end{enumerate}

\subsection{Vektorizált ARM NEON utasításkészlet-optimalizáció és futtatókörnyezetek}
Az ARM Cortex-A processzormagok dedikált Advanced SIMD (NEON) feldolgozó egységgel rendelkeznek. A NEON architektúra 32 darab 64 bites vagy 16 darab 128 bites vektorregisztert (\texttt{q0}--\texttt{q15}) biztosít \cite{armneon2020}.
\begin{itemize}
    \item \textbf{Párhuzamos műveletvégzés:} Egyetlen 128 bites NEON regiszterben egyszerre négy darab 32 bites lebegőpontos (FP32), nyolc darab 16 bites egész (INT16), vagy tizenhat darab 8 bites egész (INT8) adat fér el.
    \item \textbf{Hardveres dot-product utasítások:} A Raspberry Pi 5-ben dolgozó ARMv8.2-A Cortex-A76 mag támogatja az \texttt{SDOT} és \texttt{UDOT} gépi utasításokat. Ezek az utasítások négy párhuzamos 8 bites előjeles/előjeltelen egész szám szorzatát képezik, és az eredményt egyetlen gépi órajelciklus alatt hozzáadják egy 32 bites akkumulátor-regiszterhez:
    \begin{equation}
    \text{Acc} \leftarrow \text{Acc} + \sum_{k=0}^{3} A_k \cdot B_k
    \end{equation}
    Ez a művelet a mély konvolúciós rétegek számítási magját képezi, amely négyszeresére gyorsítja a mátrixszorzások átviteli sebességét az FP32 végrehajtáshoz képest.
\end{itemize}

A beágyazott Linux operációs rendszeren (Raspberry Pi OS 64-bit) két célszerű futtatókörnyezet illesztését tervezzük:
\begin{enumerate}
    \item \textbf{ONNX Runtime (CPUExecutionProvider):} Képes a PyTorch-ban exportált ONNX modellt futtatni, natív módon kiaknázva az ARM NEON és OpenMP többmagos szálkezelési lehetőségeit \cite{onnxruntime2023}.
    \item \textbf{Tencent NCNN motor:} Kifejezetten mobil és beágyazott ARM platformokra optimalizált, minimális memóriaigényű C++ keretrendszer, amely közvetlen assembly-szintű NEON rutinokat tartalmaz, teljesen kiküszöbölve a Python futtatókörnyezet többletterhelését.
\end{enumerate}

\section{Tervezett peremhálózati architektúra és IoT integráció}
A kutatás távlati célja egy teljesen autonóm, közvetlenül telepíthető intelligens esésdetektáló szenzorcsomópont hardveres és szoftveres prototípusának megvalósítása.

\subsection{A fizikai céleszköz felépítése}
A hardvercsomópont főbb fizikai elemei:
\begin{itemize}
    \item \textbf{Központi egység:} Raspberry Pi 5 egykártyás mikroszámítógép aktív ventilátoros hűtőbordával, amely megakadályozza a processzormagok termikus órajel-visszaszabályozását (\textit{thermal throttling}) tartós, 100\%-os terhelés mellett is.
    \item \textbf{Kameramodul:} Raspberry Pi Camera Module 3, amely egy nagylátószögű (Wide, 120° látószögű) objektívvel és Sony IMX708 szenzorral van ellátva. A MIPI CSI-2 buszon keresztül közvetlenül hardveres DMA (\textit{Direct Memory Access}) átvitellel tölti a képkockákat a processzor memóriájába, minimális CPU-overhead mellett.
    \item \textbf{Tápellátás és energiagazdálkodás:} 5V / 5A USB-C PD hálózati tápegység, kiegészítve egy szünetmentes akkumulátormodullal (UPS HAT), amely áramszünet esetén is garantálja a folyamatos felügyeletet legalább 60 percen át.
\end{itemize}

\subsection{Helyi hardveres vészjelző alrendszer (Fail-safe Actuator)}
A rendszer megbízhatóságának kulcsa, hogy életmentő szituációban nem függhet a helyi Wi-Fi hálózat vagy az internetkapcsolat stabilitásától. Ezért a mikroszámítógép általános célú be-/kimeneti (GPIO) portjára közvetlen hardveres riasztási interfész kapcsolódik:
\begin{itemize}
    \item Egy tranzisztoros kapcsolófokozattal vezérelt, 85 dB hangnyomású helyi piezo hangjelző (buzzer / sziréna), amely igazolt esés esetén azonnal helyi akusztikus riasztást ad a környezetben tartózkodók vagy a szomszédok számára.
    \item Egy kétszínű állapotjelző LED: normál működés és sziluettkövetés esetén diszkrét zöld fény, vészhelyzet vagy instabilitás esetén villogó vörös jelzés.
    \item A GPIO tranzisztor meghajtása közvetlenül a hardveres könyvtáron keresztül történik mikroszekundumos késleltetéssel, megkerülve a hálózati protokollláncot.
\end{itemize}

\subsection{IoT telemetriai kommunikáció és üzenetstruktúra}
Amennyiben rendelkezésre áll hálózati kapcsolat, a peremhálózati eszköz szabványos, kis sávszélesség-igényű \textbf{MQTT (\textit{Message Queuing Telemetry Transport})} protokollon keresztül kommunikál TLS 1.3 titkosított csatornán a helyi okosotthon-központtal (pl. Home Assistant) vagy a gondozási diszpécserközponttal.

A továbbított telemetriai adatcsomag szigorúan strukturált JSON formátumú, amely nem tartalmaz sem képet, sem biometrikus adatot, eleget téve a beépített adatvédelem (\textit{Privacy-by-Design}, GDPR 25. cikk \cite{gdpr2016}) előírásainak:
\begin{lstlisting}[language=json, caption={Példa esésdetektálási JSON telemetriai adatcsomagra.}]
{
  "device_id": "rpi5_room_sensor_01",
  "timestamp": 1716982455.420,
  "event_type": "FALL_DETECTED",
  "severity": "CRITICAL",
  "confidence": 0.94,
  "telemetry": {
    "torso_angle_deg": 78.4,
    "aspect_ratio": 1.45,
    "drop_velocity_vy": 0.62,
    "floor_contact": true,
    "immobility_duration_sec": 3.5
  },
  "heartbeat": {
    "system_fps": 22.4,
    "cpu_temp_celsius": 48.2,
    "uptime_sec": 84200
  }
}
\end{lstlisting}

Az MQTT architektúra lehetővé teszi, hogy egyetlen lakásban vagy intézményben több diszkrét szobai szenzorcsomópont csatlakozzon egyetlen központi diszpécserpanelhez anélkül, hogy a helyi hálózatot terhelő videófolyamok futnának a háttérben. A peremhálózati koncepció gyakorlati validációja, a mérési adatok rögzítése Raspberry Pi 5 hardveren, valamint az INT8-ra kvantált hálózat és az ST-GCN modell együttes futásának profilozása a Szakdolgozat 2 félév kísérleti programjának szerves részét képezi.
"""

# Update LaTeX
with open(TEX_PATH, "r", encoding="utf-8") as f:
    tex_content = f.read()

ch6_start_tex = r"\chapter{Beágyazott peremhálózati megvalósítás és jövőbeli kitekintés: Raspberry Pi platform}"
ch7_start_tex = r"% =========================================================================" + "\n" + r"% 7. FEJEZET: KUTATÁSI ÉS FEJLESZTÉSI TERV (SZAKDOLGOZAT 2)"

if ch6_start_tex in tex_content and ch7_start_tex in tex_content:
    p1 = tex_content.split(ch6_start_tex)[0]
    p2 = tex_content.split(ch7_start_tex)[1]
    new_tex = p1 + tex_ch6 + "\n\n" + ch7_start_tex + p2
    with open(TEX_PATH, "w", encoding="utf-8") as f:
        f.write(new_tex)
    print("[OK] Chapter 6 updated in docs/szakdolgozat.tex")
else:
    print("[ERROR] Split points not found in LaTeX")

# =========================================================================
# 3. DOCX GENERATOR CHAPTER 6 CODE
# =========================================================================
ch6_docx_code = '''
    doc.add_page_break()

    # =========================================================================
    # 6. FEJEZET: BEÁGYAZOTT PEREMHÁLÓZATI MEGVALÓSÍTÁS ÉS KITEKINTÉS: RASPBERRY PI
    # =========================================================================
    add_heading_1("6. Beágyazott peremhálózati megvalósítás és kitekintés: Raspberry Pi platform")

    doc.add_paragraph(
        "A kutatás és rendszertervezés kiemelt célja, hogy a kidolgozott vizuális viselkedéselemző és esésdetektáló "
        "rendszer ne csupán nagyteljesítményű asztali számítógépeken, hanem költséghatékony, alacsony fogyasztású, "
        "autonóm beágyazott céleszközökön (Edge AI hardvereken) is üzemeltethető legyen. Jelen fejezet kitekintést "
        "nyújt a rendszer beágyazott platformra – kiemelten a Raspberry Pi mikroszámítógép-családra – történő "
        "kiterjesztésének mérnöki feltételeiről, a megvalósítás előtt álló számítási és architektúrális kihívásokról, "
        "a tervezett modelloptimalizációs eljárásokról, valamint a peremhálózati IoT integrációról. A fejezetben "
        "szereplő mikroszámítógépes futási paraméterek a nemzetközi szakirodalom és az architektúra-specifikus benchmarkok "
        "alapján kalkulált megvalósíthatósági becslések, amelyek empirikus mérésekkel történő verifikációja a "
        "Szakdolgozat 2 félév feladatát képezi."
    )

    add_heading_2("6.1 A beágyazott peremhálózati (Edge AI) feldolgozás motivációja és adatvédelmi jelentősége")
    doc.add_paragraph(
        "Az idősellátásban és az otthoni felügyeleti rendszerekben a számítási feladatok fizikai helye alapvetően "
        "meghatározza a rendszer társadalmi elfogadottságát, üzemeltetési költségét és megbízhatóságát. A hagyományos "
        "távfelügyeleti megoldások a nyers kameraképet központi felhőszerverekre továbbítják gépi látási elemzés céljából. "
        "Ez a centralizált megközelítés azonban három kritikus mérnöki és etikai akadályba ütközik:\\n"
        "1. Adatvédelmi és etikai aggályok: A privát életterekből (hálószoba, nappali, közlekedők) származó folyamatos "
        "videostream felhőbe történő kisugárzása súlyos megfigyelési érzetet kelt a gondozottakban, és elfogadhatatlan "
        "adatvédelmi (GDPR) kockázatot hordoz egy esetleges hálózati adatlopás, szerveroldali biztonsági incidens vagy "
        "illetéktelen hozzáférés esetén.\\n"
        "2. Hálózati sávszélesség és rendelkezésre állás: A folyamatos nagyfelbontású videostreamelés jelentős hálózati "
        "sávszélességet igényel. Lakossági környezetben a vezeték nélküli (Wi-Fi) kapcsolat minősége ingadozhat, a "
        "sávszélesség lecsökkenhet, és egy átmeneti internetkimaradás esetén a vészjelzés el sem jut a felhőbe, ami "
        "közvetlen életveszélyt idéz elő.\\n"
        "3. Üzemeltetési költség és skálázhatóság: Több száz vagy ezer háztartás párhuzamos videófolyamainak felhőalapú "
        "GPU-infrastruktúrán történő valós idejű feldolgozása aránytalanul magas és folyamatos szerverbérleti díjakkal jár.\\n\\n"
        "Ezzel szemben a beágyazott peremhálózati (Edge AI) architektúra a feldolgozási lánc teljes egészét a felügyelt "
        "helyiségben elhelyezett kisméretű, autonóm mikroszámítógépen valósítja meg. A koncepció alapköve a zéró "
        "videóstreamelés (Zero Video Streaming) elve:\\n"
        "• A képi információ kizárólag a helyi mikroszámítógép operatív memóriájában (RAM) létezik ideiglenes pufferként "
        "az inferencia időtartama alatt (néhány tíz ezredmásodpercig).\\n"
        "• A pózbecslő réteg a csontváz-kulcspontok sikeres regresszióját követően azonnal és visszavonhatatlanul "
        "felülírja vagy felszabadítja a képi memóriát (Privacy-by-Design).\\n"
        "• A helyi hálózatra kizárólag eseményvezérelt, minimális sávszélesség-igényű, anonim JSON telemetriai adatcsomagok "
        "kerülnek ki (pl. esés ténye, időbélyeg, mozgási megbízhatóság), képi vagy biometrikus adat soha nem hagyja el "
        "a fizikai eszközt.\\n"
        "• A rendszer hálózati kapcsolat hiányában is autonóm módon működőképes marad, és közvetlenül képes aktiválni a "
        "helyi hardveres vészjelzést."
    )

    add_heading_2("6.2 Hardverplatform-elemzés és összehasonlítás")
    doc.add_paragraph(
        "A beágyazott céleszköz kiválasztásakor az optimális egyensúly megteremtése a cél a számítási teljesítmény, az "
        "energiafogyasztás, a hűtési igény és a hardverköltség között. Tervezett beágyazott célhardverként a Raspberry Pi "
        "platformot vizsgáljuk meg, kiemelten a modern Raspberry Pi 5 és a széles körben elterjedt Raspberry Pi 4B modelleket, "
        "összevetve azokat a fejlesztői asztali számítógép architektúrájával."
    )

    add_heading_3("6.2.1 Architektúrális jellemzők")
    doc.add_paragraph(
        "• Fejlesztői asztali számítógép: x86_64 architektúrájú, 6 fizikai maggal és 12 szálas párhuzamosítással "
        "rendelkező asztali processzor (3,60–4,20 GHz), fejlett AVX2 SIMD vektoros utasításkészlettel, 16 GB DDR4 memóriával "
        "(25,6 GB/s sávszélesség) és 65 W termikus tervezési teljesítménnyel (TDP).\\n"
        "• Raspberry Pi 5: Broadcom BCM2712 rendszerchip (SoC), amely négy 64 bites ARM Cortex-A76 magot tartalmaz "
        "2,40 GHz-es órajelen. Az ARMv8.2-A architektúra korszerű Neon SIMD kiterjesztéseket, valamint hardveres INT8 "
        "dot-product pontműveleteket támogat. A memóriabusz LPDDR4X típusú (128 bites szélesség, ~17 GB/s elméleti "
        "sávszélesség), maximális fogyasztása aktív terhelés mellett mindössze 12 W körül alakul. Rendelkezik 2 darab 4 sávos "
        "MIPI CSI-2 kamera interfésszel, amely közvetlenül a hardveres képjelfeldolgozó processzorhoz (ISP) kapcsolódik.\\n"
        "• Raspberry Pi 4B: Broadcom BCM2711 SoC, négy régebbi generációs ARM Cortex-A72 maggal 1,50 GHz-es órajelen "
        "(ARMv8-A architektúra). Memóriája LPDDR4 (~7 GB/s sávszélesség), maximális fogyasztása ~7 W. Kamera interfésze "
        "2 sávos MIPI CSI-2 port."
    )

    add_heading_3("6.2.2 Hardveres összehasonlító elemzés")
    doc.add_paragraph(
        "A 6.1. táblázat részletesen összegzi a fejlesztői asztali számítógép mért értékeit és a beágyazott mikroszámítógépekre "
        "vonatkozó, a nemzetközi szakirodalomból és architektúrális modellekből [2, 8, 15] származtatott becsült futási mutatókat."
    )

    # 6.1. táblázat: Hardver összehasonlítás
    table_hw = doc.add_table(rows=15, cols=4)
    table_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_hw.autofit = False

    hw_headers = ["Paraméter / Jellemző", "Fejlesztői asztali PC (x86_64)", "Raspberry Pi 5 (ARM Cortex-A76)", "Raspberry Pi 4B (ARM Cortex-A72)"]
    hw_widths = [Inches(2.0), Inches(1.8), Inches(1.8), Inches(1.5)]

    for j, h in enumerate(hw_headers):
        cell = table_hw.rows[0].cells[j]
        cell.width = hw_widths[j]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    hw_data = [
        ("Processzor típusa", "Asztali CPU (6 mag / 12 szál)", "Broadcom BCM2712 (4 mag)", "Broadcom BCM2711 (4 mag)"),
        ("Architektúra", "x86_64 (AVX2 támogatás)", "ARMv8.2-A (NEON, Dot-product)", "ARMv8-A (NEON)"),
        ("Órajel", "3,60 – 4,20 GHz", "2,40 GHz", "1,50 GHz"),
        ("Operatív memória", "16 GB DDR4 (3200 MHz)", "4 GB vagy 8 GB LPDDR4X", "4 GB LPDDR4"),
        ("TDP / Fogyasztás", "65 W (hálózati táplálás)", "~12 W (5V / 5A USB-C)", "~7 W (5V / 3A USB-C)"),
        ("Hűtési igény", "Ventilátoros asztali borda", "Aktív hűtőborda (ventilátoros)", "Passzív borda vagy kis ventilátor"),
        ("Kamera interfész", "USB 3.0 UVC webkamera", "2x 4-sávos MIPI CSI-2 (ISP)", "2-sávos MIPI CSI-2"),
        ("Pózbecslő modell", "yolov8s-pose (FP32)", "yolov8n-pose (INT8 ONNX)", "yolov8n-pose (INT8 NCNN)"),
        ("Számítási igény", "28,7 GFLOPs", "8,9 GFLOPs (INT8)", "8,9 GFLOPs (INT8)"),
        ("Inferencia idő", "36,4 ms (Saját mérés)", "~38 – 45 ms (Irodalmi becslés)", "~110 – 140 ms (Irodalmi becslés)"),
        ("Egyéb overhead (Kin.+GUI)", "3,9 ms (Saját mérés)", "~3 – 5 ms (Becslés, GUI nélkül)", "~4 – 6 ms (Becslés, GUI nélkül)"),
        ("Teljes ciklusidő", "40,3 ms (Saját mérés)", "~42 – 50 ms (Irodalmi becslés)", "~115 – 145 ms (Irodalmi becslés)"),
        ("Képkockasebesség (FPS)", "24,8 FPS (Saját mérés)", "~20 – 24 FPS (Irodalmi becslés)", "~7 – 9 FPS (Irodalmi becslés)"),
        ("Valós idejű alkalmasság", "Alkalmas (Határeset: 24,8 FPS)", "Alkalmas (Optimalizálással)", "Nem alkalmas (Túl lassú)")
    ]

    for i, row in enumerate(hw_data):
        for j, val in enumerate(row):
            cell = table_hw.rows[i+1].cells[j]
            cell.width = hw_widths[j]
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if i >= 9 and j > 0:
                run.bold = True
            if "Nem alkalmas" in val:
                run.font.color.rgb = RGBColor(180, 0, 0)
            elif "Alkalmas" in val and j > 0:
                run.font.color.rgb = RGBColor(0, 120, 0)
            bg_color = "F8FAFC" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)

    p_cap_hw = doc.add_paragraph()
    p_cap_hw.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_hw.paragraph_format.space_before = Pt(4)
    p_cap_hw.paragraph_format.space_after = Pt(12)
    r_cap_hw = p_cap_hw.add_run("6.1. táblázat: A fejlesztői asztali munkaállomás és a célzott beágyazott mikroszámítógépek összehasonlító elemzése.")
    r_cap_hw.font.size = Pt(10)
    r_cap_hw.font.italic = True
    r_cap_hw.font.color.rgb = COLOR_MUTED

    doc.add_paragraph(
        "Módszertani megjegyzés a 6.1. táblázathoz: A táblázatban az asztali PC adatai a jelen kutatás során végzett "
        "tényleges kísérleti mérések eredményei (N = 1500 frame átlaga). Ezzel szemben a Raspberry Pi 5 és Raspberry Pi 4B "
        "értékei a közzétett hivatalos YOLOv8 beágyazott mérési eredményekre [2], az ARM Cortex-A architektúra-benchmarkokra [15] "
        "és az OpenVINO/ONNX beágyazott tesztekre [8] támaszkodó elméleti és szakirodalmi megvalósíthatósági becslések.\\n\\n"
        "A táblázat adatai rámutatnak, hogy a régebbi Raspberry Pi 4B számítási kapacitása (7–9 FPS) nem elegendő a dinamikus "
        "esési folyamatok valós idejű felügyeletére. A Raspberry Pi 5 azonban a négymagos Cortex-A76 processzorával, hardveres "
        "dot-product utasításaival és gyorsabb memóriabuszkiképzésével eléri a 20–24 FPS becsült sebességet, amely már "
        "alkalmas a megbízható valós idejű működésre."
    )

    add_heading_2("6.3 Modelloptimalizációs technikák beágyazott környezetben")
    doc.add_paragraph(
        "Ahhoz, hogy a mélytanulási pózbecslés és az esésdetektálás korlátozott erőforrású mikroszámítógépen is elérje "
        "a kívánt képkockasebességet, három lépcsős szoftveres optimalizációs stratégia alkalmazása szükséges."
    )

    add_heading_3("6.3.1 Architektúra-váltás és a pontosság-sebesség kompromisszum (YOLOv8s → YOLOv8n)")
    doc.add_paragraph(
        "A kutatás első szakaszában, az asztali számítógépen a yolov8s-pose (small) modellváltozat került alkalmazásra, "
        "amely kiváló lokalizációs stabilitást nyújtott. A beágyazott platform korlátozott memóriasávszélessége és számítási "
        "kapacitása azonban megköveteli a könnyített yolov8n-pose (nano) hálózat alkalmazását.\\n\\n"
        "A két modell architektúrális és minőségi összehasonlítása:\\n"
        "• Számítási komplexitás: A paraméterszám 11,6 millióról 3,3 millióra csökken (71,5%-os csökkenés), míg a "
        "lebegőpontos műveletigény 28,7 GFLOPs-ról 8,9 GFLOPs-ra esik vissza 640 × 480-as felbontás mellett (kb. 3,2-szer kevesebb művelet).\\n"
        "• Pontosság-kompromisszum vizsgálata: A nemzetközi COCO Keypoints 2017 validációs adathalmazon [14] a yolov8s-pose "
        "modell 56,0% átlagos pontosságot (mAP_pose) ér el, míg a yolov8n-pose modell pontossága 50,4%. Ez mintegy 5,6 százalékpontos "
        "nominális pontosságvesztést jelent.\\n"
        "• Mérnöki hatás az esésdetektálásra: A szakirodalmi és topológiai elemzés alapján a nano modell pontosságcsökkenése "
        "döntően az apró, nagy felbontást igénylő és könnyen takarásba kerülő arc-kulcspontok (szemek, fülek, orr), valamint a "
        "csuklók és kézfejek lokalizációjánál jelentkezik. Ezzel szemben az esésdetektálás állapotgépe és kinematikai motorja "
        "szempontjából meghatározó törzsi kulcspontok (vállak, csípők) és az alsó végtagok nagy ízületei (térdek, bokák) esetében "
        "a yolov8n-pose megbízhatósága megközelíti a nagyobb modellét. A nagyméretű, globális testtartásváltozások és a vertikális "
        "zuhanási sebességbecslés pontossága a nano modell alkalmazásával is megőrizhető, miközben a számítási ciklusidő több mint felére csökken."
    )

    add_heading_3("6.3.2 Poszt-tanítási INT8 kvantálás (Post-Training Quantization - PTQ)")
    doc.add_paragraph(
        "A konvolúciós neurális hálózatok alapértelmezésben 32 bites egyszeres pontosságú lebegőpontos (FP32) formátumban tárolják "
        "a súlyokat és aktivációkat. Beágyazott ARM processzorokon az FP32 műveletek jelentős memóriasávszélességet és aritmetikai "
        "órajelet emésztenek fel. A poszt-tanítási INT8 kvantálás célja, hogy a 32 bites lebegőpontos értékeket 8 bites előjeles "
        "egész számokká alakítsa, 75%-os memóriamegtakarítást és többszörös számítási gyorsulást biztosítva.\\n\\n"
        "A lebegőpontos érték (x ∈ R) és a kvantált egész (q ∈ Z) közötti afin transzformáció formális matematikai leírása:\\n"
        "q = round(x / S) + Z\\n"
        "ahol a dekvantálási összefüggés: x̂ = S · (q - Z).\\n"
        "A formulában S ∈ R+ a valós lebegőpontos skálázási tényező (scale factor), Z ∈ Z pedig a nullapont-eltolás (zero-point offset), "
        "amely biztosítja, hogy a lebegőpontos nulla érték pontosan leképezhető legyen az egész számok halmazára.\\n\\n"
        "Ha a vizsgált tenzor lebegőpontos értéktartománya [x_min, x_max], a kvantált tartomány pedig [q_min, q_max] (előjeles INT8 esetén "
        "[-128, 127]), a paraméterek az alábbiak szerint adódnak:\\n"
        "S = (x_max - x_min) / (q_max - q_min)\\n"
        "Z = round(-x_min / S) + q_min\\n\\n"
        "Kvantálási stratégiák a rendszerben:\\n"
        "1. Szimmetrikus súlykvantálás: A hálózati rétegek súlymátrixai esetében a statikus értéktartomány jellemzően szimmetrikus a "
        "nulla körül, így a nullapont fixen rögzíthető (Z = 0), amely egyszerűsíti a hardveres szorzási láncot.\\n"
        "2. Aszimmetrikus aktivációkvantálás statikus kalibrációval: Mivel az aktivációs függvények (SiLU) utáni kimenetek nem szimmetrikusak, "
        "az aktivációknál nemzéró Z eltolást alkalmazunk. A dinamikatartomány empirikus rögzítéséhez egy 200 reprezentatív képkockából álló "
        "kalibrációs mintahalmazt futtatunk át a hálózaton (Post-Training Static Calibration). A szélsőértékeket Kullback–Leibler (KL) divergencia "
        "minimalizálásával optimalizáljuk, elkerülve a telítési és kerekítési hibákból fakadó pontosságvesztést."
    )

    add_heading_3("6.3.3 Vektorizált ARM NEON utasításkészlet-optimalizáció és futtatókörnyezetek")
    doc.add_paragraph(
        "Az ARM Cortex-A processzormagok dedikált Advanced SIMD (NEON) feldolgozó egységgel rendelkeznek. A NEON architektúra 32 darab "
        "64 bites vagy 16 darab 128 bites vektorregisztert (q0–q15) biztosít [15].\\n"
        "• Párhuzamos műveletvégzés: Egyetlen 128 bites NEON regiszterben egyszerre négy darab 32 bites lebegőpontos (FP32), nyolc darab "
        "16 bites egész (INT16), vagy tizenhat darab 8 bites egész (INT8) adat fér el.\\n"
        "• Hardveres dot-product utasítások: A Raspberry Pi 5-ben dolgozó ARMv8.2-A Cortex-A76 mag támogatja az SDOT és UDOT gépi "
        "utasításokat. Ezek az utasítások négy párhuzamos 8 bites egész szám szorzatát képezik, és az eredményt egyetlen gépi órajelciklus "
        "alatt hozzáadják egy 32 bites akkumulátor-regiszterhez: Acc ← Acc + ∑ A_k · B_k. Ez a művelet a mély konvolúciós rétegek számítási "
        "magját képezi, amely négyszeresére gyorsítja a mátrixszorzások átviteli sebességét az FP32 végrehajtáshoz képest.\\n\\n"
        "A beágyazott Linux operációs rendszeren (Raspberry Pi OS 64-bit) két célszerű futtatókörnyezet illesztését tervezzük:\\n"
        "1. ONNX Runtime (CPUExecutionProvider): Képes a PyTorch-ban exportált ONNX modellt futtatni, natív módon kiaknázva az "
        "ARM NEON és OpenMP többmagos szálkezelési lehetőségeit [9].\\n"
        "2. Tencent NCNN motor: Kifejezetten mobil és beágyazott ARM platformokra optimalizált, minimális memóriaigényű C++ keretrendszer, "
        "amely közvetlen assembly-szintű NEON rutinokat tartalmaz, teljesen kiküszöbölve a Python futtatókörnyezet többletterhelését."
    )

    add_heading_2("6.4 Tervezett peremhálózati architektúra és IoT integráció")
    doc.add_paragraph(
        "A kutatás távlati célja egy teljesen autonóm, közvetlenül telepíthető intelligens esésdetektáló szenzorcsomópont hardveres "
        "és szoftveres prototípusának megvalósítása."
    )

    add_heading_3("6.4.1 A fizikai céleszköz felépítése")
    doc.add_paragraph(
        "A hardvercsomópont főbb fizikai elemei:\\n"
        "• Központi egység: Raspberry Pi 5 egykártyás mikroszámítógép aktív ventilátoros hűtőbordával, amely megakadályozza a processzormagok "
        "termikus órajel-visszaszabályozását (thermal throttling) tartós, 100%-os terhelés mellett is.\\n"
        "• Kameramodul: Raspberry Pi Camera Module 3, amely egy nagylátószögű (Wide, 120° látószögű) objektívvel és Sony IMX708 szenzorral "
        "van ellátva. A MIPI CSI-2 buszon keresztül közvetlenül hardveres DMA (Direct Memory Access) átvitellel tölti a képkockákat a processzor "
        "memóriájába, minimális CPU-overhead mellett.\\n"
        "• Tápellátás és energiagazdálkodás: 5V / 5A USB-C PD hálózati tápegység, kiegészítve egy szünetmentes akkumulátormodullal (UPS HAT), "
        "amely áramszünet esetén is garantálja a folyamatos felügyeletet legalább 60 percen át."
    )

    add_heading_3("6.4.2 Helyi hardveres vészjelző alrendszer (Fail-safe Actuator)")
    doc.add_paragraph(
        "A rendszer megbízhatóságának kulcsa, hogy életmentő szituációban nem függhet a helyi Wi-Fi hálózat vagy az internetkapcsolat "
        "stabilitásától. Ezért a mikroszámítógép általános célú be-/kimeneti (GPIO) portjára közvetlen hardveres riasztási interfész kapcsolódik:\\n"
        "• Egy tranzisztoros kapcsolófokozattal vezérelt, 85 dB hangnyomású helyi piezo hangjelző (buzzer / sziréna), amely igazolt esés esetén "
        "azonnal helyi akusztikus riasztást ad a környezetben tartózkodók vagy a szomszédok számára.\\n"
        "• Egy kétszínű állapotjelző LED: normál működés és sziluettkövetés esetén diszkrét zöld fény, vészhelyzet vagy instabilitás esetén villogó vörös jelzés.\\n"
        "• A GPIO tranzisztor meghajtása közvetlenül a hardveres könyvtáron keresztül történik mikroszekundumos késleltetéssel, megkerülve a hálózati protokollláncot."
    )

    add_heading_3("6.4.3 IoT telemetriai kommunikáció és üzenetstruktúra")
    doc.add_paragraph(
        "Amennyiben rendelkezésre áll hálózati kapcsolat, a peremhálózati eszköz szabványos, kis sávszélesség-igényű MQTT (Message Queuing Telemetry "
        "Transport) protokollon keresztül kommunikál TLS 1.3 titkosított csatornán a helyi okosotthon-központtal (pl. Home Assistant) vagy a "
        "gondozási diszpécserközponttal.\\n\\n"
        "A továbbított telemetriai adatcsomag szigorúan strukturált JSON formátumú, amely nem tartalmaz sem képet, sem biometrikus adatot, "
        "eleget téve a beépített adatvédelem (Privacy-by-Design, GDPR 25. cikk [13]) előírásainak:\\n"
        "{\\n"
        '  "device_id": "rpi5_room_sensor_01",\\n'
        '  "timestamp": 1716982455.420,\\n'
        '  "event_type": "FALL_DETECTED",\\n'
        '  "severity": "CRITICAL",\\n'
        '  "confidence": 0.94,\\n'
        '  "telemetry": {\\n'
        '    "torso_angle_deg": 78.4,\\n'
        '    "aspect_ratio": 1.45,\\n'
        '    "drop_velocity_vy": 0.62,\\n'
        '    "floor_contact": true,\\n'
        '    "immobility_duration_sec": 3.5\\n'
        '  },\\n'
        '  "heartbeat": {\\n'
        '    "system_fps": 22.4,\\n'
        '    "cpu_temp_celsius": 48.2,\\n'
        '    "uptime_sec": 84200\\n'
        '  }\\n'
        "}\\n\\n"
        "Az MQTT architektúra lehetővé teszi, hogy egyetlen lakásban vagy intézményben több diszkrét szobai szenzorcsomópont csatlakozzon "
        "egyetlen központi diszpécserpanelhez anélkül, hogy a helyi hálózatot terhelő videófolyamok futnának a háttérben. A peremhálózati koncepció "
        "gyakorlati validációja, a mérési adatok rögzítése Raspberry Pi 5 hardveren, valamint az INT8-ra kvantált hálózat és az ST-GCN modell "
        "együttes futásának profilozása a Szakdolgozat 2 félév kísérleti programjának szerves részét képezi."
    )
'''

# Update generate_approved_docx.py
with open(GEN_PATH, "r", encoding="utf-8") as f:
    gen_content = f.read()

target_save = "    # Mentés a célútvonalakra"
if target_save in gen_content:
    if "6. FEJEZET: BEÁGYAZOTT PEREMHÁLÓZATI MEGVALÓSÍTÁS" not in gen_content:
        new_gen = gen_content.replace(target_save, ch6_docx_code + "\n" + target_save)
        with open(GEN_PATH, "w", encoding="utf-8") as f:
            f.write(new_gen)
        print("[OK] Chapter 6 added to generate_approved_docx.py")
    else:
        print("[INFO] Chapter 6 already present in generate_approved_docx.py")
else:
    print("[ERROR] target_save not found in generate_approved_docx.py")
