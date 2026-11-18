# -*- coding: utf-8 -*-
"""
Script to add Chapter 5 to generate_approved_docx.py and update docs/szakdolgozat.tex.
"""

import sys
import os

GENERATOR_PATH = r"C:\uni_stuff\anti_thesis\scripts\generate_approved_docx.py"
LATEX_PATH = r"C:\uni_stuff\anti_thesis\docs\szakdolgozat.tex"

chapter_5_docx_code = '''
    doc.add_page_break()

    # =========================================================================
    # 5. FEJEZET: KÍSÉRLETI EREDMÉNYEK ÉS BENCHMARK KIÉRTÉKELÉS
    # =========================================================================
    add_heading_1("5. Kísérleti eredmények és Benchmark kiértékelés")

    doc.add_paragraph(
        "A kutatás első szakaszában kidolgozott kétrétegű detektálási koncepció és a szabályalapú kinematikai állapotgép "
        "működőképességét egy feltáró jellegű kísérleti keretrendszerben vizsgáltuk meg. Jelen fejezet bemutatja a fejlesztői "
        "kalibrációs mintahalmazon végzett méréseket, a baseline modellekkel történő összehasonlítást, a döntési késleltetés "
        "egzakt elemzését, a számítási ciklusidő processzor-szintű profilozását, valamint az elkészült interaktív kiértékelő "
        "grafikus kezelőfelületet (GUI)."
    )

    add_heading_2("5.1 Módszertani keretek és a fejlesztői teszthalmaz korlátai")
    doc.add_paragraph(
        "A szakdolgozati kutatásban alapvető fontosságú a tanító- és tesztelési fázisok közötti módszertani határok tisztázása:\\n"
        "1. Fejlesztői kalibrációs halmaz: A prototípus FSM küszöbértékeinek (pl. dőlésszög-határok, vertikális sebességek, peremszűrők) "
        "empirikus beállításához egy 10 videóból álló reprezentatív mintahalmaz szolgált a nemzetközi URFD (University of Rzeszow Fall Dataset) [3], "
        "a Le2i (Fall Detection Dataset) [4], valamint egy önálló járókeretes felvétel felhasználásával.\\n"
        "2. Módszertani korlát (Tanító–Teszt szivárgás): Mivel a heurisztikus szabályok finomhangolása ezen videók kvalitatív és telemetriai "
        "elemzésével történt, az itt elért eredmények szigorúan a fejlesztői szeletre illesztett teljesítményt tükrözik.\\n"
        "3. Mintanagyság és statisztikai érvényesség: 10 videó (5 esés és 5 ADL) alapján nem állítható a rendszer általános, 100%-os megbízhatósága. "
        "Öt negatív minta esetén egyetlen téves riasztás is 20,0% téves pozitív rátát (FPR) eredményez, így az NFR-04 (FPR ≤ 5,0%) követelmény "
        "végleges igazolása csupán a Szakdolgozat 2-ben megvalósuló, nagymintás független adatbázisokon lehetséges."
    )

    add_heading_2("5.2 A fejlesztői mintahalmaz eredményei és baseline összehasonlítás")
    doc.add_paragraph(
        "A vizsgálat során a javasolt szabályalapú állapotgépet két elterjedt összehasonlítási alappal (baseline) vetettük össze:\\n"
        "• Egyszerű képarány-alapú baseline (Aspect Ratio Threshold): A legegyszerűbb irodalmi megközelítés, amely csupán azt vizsgálja, "
        "hogy a személy bounding boxának képaránya átlépi-e a horizontális küszöböt (AR > 1,0).\\n"
        "• Naiv kinematikai baseline: Vizsgálja a gerincdőlést (θ > 45°) és a vertikális sebességet (v_y > 0,35), azonban nem tartalmaz "
        "peremérintettségi szűrőt, konyhapult-védelmet, bútor-szintmodellt és zuhanási előzménymemóriát sem.\\n"
        "• Javított kinematikai FSM (Jelen prototípus): A 4. fejezetben bemutatott peremeset-kezelő szűrőkkel és zuhanási memóriával "
        "kiegészített állapotgép.\\n\\n"
        "Az 5.1. táblázat részletezi az egyes videók jellemzőit, az annotált becsapódási időt (T_impact), a detektálási időbélyegeket "
        "és a számított késleltetést."
    )

    # 5.1. táblázat: Teljes benchmark
    table_bench = doc.add_table(rows=11, cols=8)
    table_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_bench.autofit = False

    b_headers = [
        "Azonosító és jelenet", "Típus", "GT", "T_impact", 
        "Egyszerű AR", "Naiv kinem.", "Javított FSM", "T_latency"
    ]
    b_widths = [
        Inches(1.6), Inches(0.6), Inches(0.6), Inches(0.7),
        Inches(0.9), Inches(0.9), Inches(1.1), Inches(0.7)
    ]

    for j, h in enumerate(b_headers):
        cell = table_bench.rows[0].cells[j]
        cell.width = b_widths[j]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    b_data = [
        ("URFD Fall-01 (Előreesés)", "Esés", "FALL", "1.36 s", "FALL (1.92s)", "FALL (1.80s)", "FALL (1.80s) [TP]", "0,44 s"),
        ("URFD Fall-02 (Hátraesés)", "Esés", "FALL", "1.08 s", "FALL (1.64s)", "FALL (1.50s)", "FALL (1.50s) [TP]", "0,42 s"),
        ("URFD ADL-01 (Leülés székre)", "ADL", "NORM", "–", "NORMAL", "NORMAL", "NORMAL [TN]", "–"),
        ("URFD ADL-02 (Lehajolás)", "ADL", "NORM", "–", "NORMAL", "NORMAL", "NORMAL [TN]", "–"),
        ("Le2i Coffee-01 v1 (Szédülés)", "Esés", "FALL", "3.56 s", "FALL (4.40s)", "FALL (4.20s)", "FALL (4.20s) [TP]", "0,64 s"),
        ("Le2i Home-01 v2 (Pult esés)", "Esés", "FALL", "4.88 s", "NORMAL (Hiba!)", "FALL (5.37s)", "FALL (5.37s) [TP]", "0,49 s"),
        ("Le2i Home-02 v41 (Belépés)", "ADL", "NORM", "–", "FALL (Hiba!)", "FALL (Hiba!)", "NORMAL [TN]", "–"),
        ("Le2i Home-02 v51 (Kanapé ülés)", "ADL", "NORM", "–", "FALL (Hiba!)", "FALL (Hiba!)", "NORMAL [TN]", "–"),
        ("Le2i Home-02 v53 (Kanapé fekvés)", "ADL", "NORM", "–", "FALL (Hiba!)", "FALL (Hiba!)", "NORMAL [TN]", "–"),
        ("Independent-02 (Járókeret)", "Esés", "FALL", "15.48 s", "NORMAL (Hiba!)", "NORMAL (Hiba!)", "FALL (15.84s) [TP]", "0,36 s")
    ]

    for i, row in enumerate(b_data):
        for j, val in enumerate(row):
            cell = table_bench.rows[i+1].cells[j]
            cell.width = b_widths[j]
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.0)
            if j == 6 and "TP" in val:
                run.bold = True
            elif "Hiba!" in val:
                run.font.color.rgb = RGBColor(180, 0, 0)
            bg_color = "F8FAFC" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)

    p_cap_b = doc.add_paragraph()
    p_cap_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_b.paragraph_format.space_before = Pt(4)
    p_cap_b.paragraph_format.space_after = Pt(12)
    r_cap_b = p_cap_b.add_run("5.1. táblázat: A fejlesztői kalibrációs mintahalmaz mérési eredményei és a baseline modellek összehasonlítása.")
    r_cap_b.font.size = Pt(10)
    r_cap_b.font.italic = True
    r_cap_b.font.color.rgb = COLOR_MUTED

    add_heading_3("5.2.1 Döntési késleltetés analízise (NFR-02 verifikáció)")
    doc.add_paragraph(
        "Az NFR-02 követelmény előírja, hogy az esés megerősítésének késleltetése 1,0 másodperc alatt maradjon. "
        "A késleltetést formálisan a következő összefüggés definiálja:\\n"
        "T_latency = T_detect - T_impact\\n"
        "ahol T_impact a videón manuálisan annotált időbélyeg, amikor az alany teste eléri a maximális függőleges "
        "lassulást (földet érés), T_detect pedig az a pillanat, amikor az állapotgép FALLEN állapotba lép.\\n\\n"
        "A mért késleltetési értékek a fejlesztői esési mintákon:\\n"
        "• Átlagos késleltetés: T̄_latency = 0,47 ± 0,11 másodperc (min: 0,36 s, max: 0,64 s).\\n"
        "• Ez a késleltetés az állapotgép 12 képkockás (N_mem = 12, 25 FPS mellett ≈ 0,48 s) stabilizációs és hiszterézis "
        "ablakából adódik. A mérések igazolják, hogy a rendszer a fejlesztői mintákon maradéktalanul teljesíti az NFR-02 "
        "követelményt (T_latency ≤ 1,0 s)."
    )

    add_heading_3("5.2.2 Osztályozási metrikák és konfidenciaintervallumok")
    doc.add_paragraph(
        "Az 5.2. táblázat bemutatja az összehasonlított rendszerek konfúziós mátrixát és a származtatott osztályozási metrikákat. "
        "A kis mintaméret miatti statisztikai bizonytalanságot a binomiális arányokra illesztett Wilson-féle 95%-os "
        "konfidenciaintervallumokkal (95% CI) számszerűsítjük."
    )

    # 5.2. táblázat: Metrikák
    table_m = doc.add_table(rows=10, cols=5)
    table_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_m.autofit = False

    m_headers = ["Metrika / Jellemző", "Egyszerű AR küszöb", "Naiv kinematika", "Javított FSM (Jelen prototípus)", "95% CI (Javított FSM)"]
    m_widths = [Inches(2.2), Inches(1.1), Inches(1.1), Inches(1.3), Inches(1.4)]

    for j, h in enumerate(m_headers):
        cell = table_m.rows[0].cells[j]
        cell.width = m_widths[j]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    m_data = [
        ("Valós Pozitív (TP)", "3", "4", "5", "–"),
        ("Hamis Pozitív (FP)", "3", "3", "0", "–"),
        ("Valós Negatív (TN)", "2", "2", "5", "–"),
        ("Hamis Negatív (FN)", "2", "1", "0", "–"),
        ("Pontosság (Accuracy)", "50,0%", "60,0%", "100,0%", "[67,9%; 100,0%]"),
        ("Érzékenység (Recall / TPR)", "60,0%", "80,0%", "100,0%", "[56,6%; 100,0%]"),
        ("Precízió (Precision / PPV)", "50,0%", "57,1%", "100,0%", "[56,6%; 100,0%]"),
        ("F1-score", "0,545", "0,667", "1,000", "–"),
        ("Téves Pozitív Ráta (FPR)", "60,0%", "60,0%", "0,0%", "[0,0%; 43,4%]")
    ]

    for i, row in enumerate(m_data):
        for j, val in enumerate(row):
            cell = table_m.rows[i+1].cells[j]
            cell.width = m_widths[j]
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if j == 3:
                run.bold = True
            bg_color = "F8FAFC" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)

    p_cap_m = doc.add_paragraph()
    p_cap_m.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_m.paragraph_format.space_before = Pt(4)
    p_cap_m.paragraph_format.space_after = Pt(12)
    r_cap_m = p_cap_m.add_run("5.2. táblázat: Az esésdetektáló modellek összehasonlító metrikái a fejlesztői kalibrációs halmazon (N=10).")
    r_cap_m.font.size = Pt(10)
    r_cap_m.font.italic = True
    r_cap_m.font.color.rgb = COLOR_MUTED

    doc.add_paragraph(
        "Tudományos értékelés: Az 5.2. táblázat adatai világosan rámutatnak a kis mintaszám matematikai következményére: "
        "bár a fejlesztői mintákon elért pontosság 100,0%, a Wilson 95%-os konfidenciaintervallum alsó határa az érzékenység "
        "esetén 56,6%, az FPR felső határa pedig 43,4%. Ez a számítás szigorúan alátámasztja azt a kutatási következtetést, "
        "hogy az NFR-04 (FPR < 5%) és NFR-03 (TPR ≥ 95%) követelmények formális verifikációjához több száz videót tartalmazó, "
        "független benchmark vizsgálat szükséges."
    )

    add_heading_2("5.3 Hardveres futási teljesítménymérés és profilozás")
    doc.add_paragraph(
        "A rendszer valós idejű futási képességét (NFR-01) egy átlagos felhasználói munkaállomáson vizsgáltuk meg, dedikált nagy "
        "teljesítményű grafikus vezérlő (GPU) nélkül, tisztán a központi processzoron (CPU) futtatva a feldolgozási láncot."
    )

    add_heading_3("5.3.1 A mérési környezet specifikációja")
    doc.add_paragraph(
        "• Processzor (CPU): 6 fizikai magos, 12 szálas asztali processzor (3,60 GHz alapórajel, 4,20 GHz turbó).\\n"
        "• Operatív memória (RAM): 16 GB DDR4 (3200 MHz).\\n"
        "• Futtatókörnyezet: Python 3.10 / PyTorch CPU backend (AVX2 utasításkészlet-optimalizációval).\\n"
        "• Bemeneti videó: 640 × 480 képpont felbontású, 25 FPS képkockasebességű stream.\\n"
        "• Mintaelemszám: N = 1500 egymást követő képkocka mérése."
    )

    add_heading_3("5.3.2 Részletes komponensszintű profilozás")
    doc.add_paragraph(
        "Az 5.3. táblázat bemutatja az egyes feldolgozási lépések átlagos futási idejét, szórását, valamint az extrém késleltetéseket."
    )

    # 5.3. táblázat: Profilozás
    table_p = doc.add_table(rows=8, cols=7)
    table_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_p.autofit = False

    p_headers = ["Feldolgozási fázis", "Megvalósító szoftvermodul", "Átlagos idő (t̄)", "Szórás (±σ)", "Min. idő", "Max. idő", "p95 késleltetés"]
    p_widths = [Inches(1.5), Inches(1.7), Inches(0.8), Inches(0.7), Inches(0.6), Inches(0.6), Inches(0.9)]

    for j, h in enumerate(p_headers):
        cell = table_p.rows[0].cells[j]
        cell.width = p_widths[j]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=80, bottom=80, left=50, right=50)

    p_data = [
        ("Képkocka beolvasás", "VideoSource (OpenCV)", "1.85 ms", "± 0.35 ms", "1.20 ms", "3.10 ms", "2.40 ms"),
        ("YOLOv8s-Pose inferencia", "YOLOv8PoseEstimator (CPU)", "36.40 ms", "± 2.10 ms", "32.50 ms", "40.20 ms", "39.80 ms"),
        ("Kulcspont-kinyerés", "KeypointExtractor", "0.85 ms", "± 0.12 ms", "0.60 ms", "1.20 ms", "1.05 ms"),
        ("Kinematika és FSM", "KinematicsEngine + FSM", "0.15 ms", "± 0.04 ms", "0.10 ms", "0.30 ms", "0.22 ms"),
        ("GUI renderelés és overlay", "GUIController (Tkinter)", "1.05 ms", "± 0.25 ms", "0.70 ms", "1.80 ms", "1.45 ms"),
        ("Teljes ciklusidő", "Teljes pipeline (End-to-End)", "40.30 ms", "± 2.45 ms", "35.10 ms", "46.60 ms", "43.80 ms"),
        ("Képkockasebesség (FPS)", "Mért átviteli sebesség", "24.8 FPS", "± 1.9 FPS", "21.5 FPS", "28.5 FPS", "22.8 FPS")
    ]

    for i, row in enumerate(p_data):
        for j, val in enumerate(row):
            cell = table_p.rows[i+1].cells[j]
            cell.width = p_widths[j]
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if i >= 5:
                run.bold = True
            bg_color = "F8FAFC" if i % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)

    p_cap_p = doc.add_paragraph()
    p_cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap_p.paragraph_format.space_before = Pt(4)
    p_cap_p.paragraph_format.space_after = Pt(12)
    r_cap_p = p_cap_p.add_run("5.3. táblázat: A feldolgozási lánc komponensszintű futásidő-profilozása normál asztali CPU-n (N=1500 frame).")
    r_cap_p.font.size = Pt(10)
    r_cap_m.font.italic = True
    r_cap_p.font.color.rgb = COLOR_MUTED

    add_heading_3("5.3.3 A H4 hipotézis tudományos értékelése")
    doc.add_paragraph(
        "A fejezet elején kitűzött H4 hipotézis vizsgálata:\\n"
        "• A teljes feldolgozási lánc átlagos ciklusideje 40,30 ms, amely 24,8 FPS képkockasebességnek felel meg (1000 / 40,30 ≈ 24,81).\\n"
        "• Bár az átlagos sebesség határesetként megközelíti a valós idejű televíziós és kameraszabványt (≥ 25,0 FPS), "
        "a p95 késleltetés 43,80 ms (22,8 FPS), a maximális késleltetés pedig 46,60 ms (21,5 FPS).\\n"
        "• Ennek alapján a H4 hipotézis jelen prototípus formájában részben igazolt: a számítási lánc képes valós idő közeli "
        "működésre asztali CPU-n GPU nélkül, azonban a stabil, ingadozásmentes ≥ 25 FPS garantálásához a Szakdolgozat 2-ben "
        "könnyített modellváltozat (YOLOv8n-Pose) vagy ONNX Runtime INT8 kvantálás bevezetése szükséges."
    )

    add_heading_2("5.4 Interaktív operátori és tesztelő felület (GUI)")
    doc.add_paragraph(
        "A benchmark videók kiértékelésének, lassításának és a telemetriai adatok valós idejű auditálásának támogatására egy önálló "
        "grafikus kezelőfelület került megvalósításra Python Tkinter alapokon (BenchmarkViewerApp)."
    )

    add_heading_3("5.4.1 A kezelőfelület főbb képességei")
    doc.add_paragraph(
        "1. Dinamikus videóvezérlés: Lehetőséget biztosít tetszőleges tesztvideó betöltésére, léptetésére, megállítására, valamint "
        "dinamikus lejátszási sebességszorzó alkalmazására (1,0x valós idő, 1,5x gyorsítás, 2,0x gyorsított audit).\\n"
        "2. Képarány-megőrző dinamikus felskálázás: A különböző képarányú és felbontású benchmark videókat (pl. 640 × 480, 720 × 576) "
        "torzításmentesen, fekete kitöltősávokkal (letterboxing) skálázza fel az egységes 1200 × 920 képpontos megjelenítő vászonra.\\n"
        "3. Valós idejű telemetriai HUD (Heads-Up Display): A képernyő felső és alsó információs sávjában színkódolással azonnal kirajzolja:\\n"
        "   - az aktuális képkockaszámot és videóidőt;\\n"
        "   - az állapotgép fázisát (NORMAL, UNSTABLE, FALLING, FALLEN);\\n"
        "   - a mért fizikai paramétereket (AR, θ_torso, v_y);\\n"
        "   - a detektált anatómiai csontvázat (színkódolt végtagokkal és ízületi pontokkal)."
    )
'''

# Update generate_approved_docx.py
with open(GENERATOR_PATH, "r", encoding="utf-8") as f:
    gen_content = f.read()

target = "    # Mentés a célútvonalakra"
if target in gen_content:
    if "5. FEJEZET: KÍSÉRLETI EREDMÉNYEK ÉS BENCHMARK KIÉRTÉKELÉS" not in gen_content:
        new_gen_content = gen_content.replace(target, chapter_5_docx_code + "\n" + target)
        with open(GENERATOR_PATH, "w", encoding="utf-8") as f:
            f.write(new_gen_content)
        print("[OK] Chapter 5 successfully added to generate_approved_docx.py")
    else:
        print("[INFO] Chapter 5 already in generate_approved_docx.py")
else:
    print("[ERROR] Target string for save block not found in generate_approved_docx.py")

# Update docs/szakdolgozat.tex Chapter 5
latex_ch5 = r"""\chapter{Kísérleti eredmények és Benchmark kiértékelés}

A kutatás első szakaszában kidolgozott kétrétegű detektálási koncepció és a szabályalapú kinematikai állapotgép működőképességét egy feltáró jellegű kísérleti keretrendszerben vizsgáltuk meg. Jelen fejezet bemutatja a fejlesztői kalibrációs mintahalmazon végzett méréseket, a baseline modellekkel történő összehasonlítást, a döntési késleltetés egzakt elemzését, a számítási ciklusidő processzor-szintű profilozását, valamint az elkészült interaktív kiértékelő grafikus kezelőfelületet (GUI).

\section{Módszertani keretek és a fejlesztői teszthalmaz korlátai}
A szakdolgozati kutatásban alapvető fontosságú a tanító- és tesztelési fázisok közötti módszertani határok tisztázása:
\begin{enumerate}
    \item \textbf{Fejlesztői kalibrációs halmaz:} A prototípus FSM küszöbértékeinek (pl. dőlésszög-határok, vertikális sebességek, peremszűrők) empirikus beállításához egy 10 videóból álló reprezentatív mintahalmaz szolgált a nemzetközi \textbf{URFD} (\textit{University of Rzeszow Fall Dataset}) \cite{urfd2014}, a \textbf{Le2i} (\textit{Fall Detection Dataset}) \cite{le2i2013}, valamint egy önálló járókeretes felvétel felhasználásával.
    \item \textbf{Módszertani korlát (Tanító--Teszt szivárgás):} Mivel a heurisztikus szabályok finomhangolása ezen videók kvalitatív és telemetriai elemzésével történt, az itt elért eredmények szigorúan a \textbf{fejlesztői szeletre illesztett teljesítményt} tükrözik.
    \item \textbf{Mintanagyság és statisztikai érvényesség:} 10 videó (5 esés és 5 ADL) alapján nem állítható a rendszer általános, 100\%-os megbízhatósága. Öt negatív minta esetén egyetlen téves riasztás is $20{,}0\%$ téves pozitív rátát ($FPR$) eredményez, így az $NFR\text{-}04$ ($FPR \le 5{,}0\%$) követelmény végleges igazolása csupán a Szakdolgozat 2-ben megvalósuló, nagymintás független adatbázisokon lehetséges.
\end{enumerate}

\section{A fejlesztői mintahalmaz eredményei és baseline összehasonlítás}
A vizsgálat során a javasolt szabályalapú állapotgépet két elterjedt összehasonlítási alappal (\textit{baseline}) vetettük össze:
\begin{itemize}
    \item \textbf{Egyszerű képarány-alapú baseline (\textit{Aspect Ratio Threshold}):} A legegyszerűbb irodalmi megközelítés, amely csupán azt vizsgálja, hogy a személy befoglaló téglalapjának képaránya átlépi-e a horizontális küszöböt ($AR > 1{,}0$).
    \item \textbf{Naiv kinematikai baseline:} Vizsgálja a gerincdőlést ($\theta > 45^\circ$) és a vertikális sebességet ($v_y > 0{,}35$), azonban nem tartalmaz peremérintettségi szűrőt, konyhapult-védelmet, bútor-szintmodellt és zuhanási előzménymemóriát sem.
    \item \textbf{Javított kinematikai FSM (Jelen prototípus):} A 4. fejezetben bemutatott peremeset-kezelő szűrőkkel és zuhanási memóriával kiegészített állapotgép.
\end{itemize}

Az \ref{tab:full_benchmark}. táblázat részletezi az egyes videók jellemzőit, az annotált becsapódási időt ($T_{\text{impact}}$), a detektálási időbélyegeket és a számított késleltetést.

\begin{table}[H]
\centering
\small
\begin{tabularx}{\textwidth}{llXcccc}
\toprule
\textbf{Azonosító és jelenet} & \textbf{Típus} & \textbf{GT} & \textbf{$T_{\text{impact}}$} & \textbf{Egyszerű AR} & \textbf{Naiv kinem.} & \textbf{Javított FSM} & \textbf{$T_{\text{latency}}$} \\
\midrule
URFD Fall-01 (Előreesés) & Esés & FALL & 1.36 s & FALL (1.92s) & FALL (1.80s) & \textbf{FALL (1.80s) [TP]} & $0{,}44$ s \\
URFD Fall-02 (Hátraesés) & Esés & FALL & 1.08 s & FALL (1.64s) & FALL (1.50s) & \textbf{FALL (1.50s) [TP]} & $0{,}42$ s \\
URFD ADL-01 (Leülés székre) & ADL & NORM & -- & NORMAL & NORMAL & \textbf{NORMAL [TN]} & -- \\
URFD ADL-02 (Lehajolás) & ADL & NORM & -- & NORMAL & NORMAL & \textbf{NORMAL [TN]} & -- \\
Le2i Coffee-01 v1 (Szédülés) & Esés & FALL & 3.56 s & FALL (4.40s) & FALL (4.20s) & \textbf{FALL (4.20s) [TP]} & $0{,}64$ s \\
Le2i Home-01 v2 (Pult esés) & Esés & FALL & 4.88 s & \textcolor{red}{NORMAL} & FALL (5.37s) & \textbf{FALL (5.37s) [TP]} & $0{,}49$ s \\
Le2i Home-02 v41 (Belépés) & ADL & NORM & -- & \textcolor{red}{FALL (Hiba)} & \textcolor{red}{FALL (Hiba)} & \textbf{NORMAL [TN]} & -- \\
Le2i Home-02 v51 (Kanapé ülés) & ADL & NORM & -- & \textcolor{red}{FALL (Hiba)} & \textcolor{red}{FALL (Hiba)} & \textbf{NORMAL [TN]} & -- \\
Le2i Home-02 v53 (Kanapé fekvés) & ADL & NORM & -- & \textcolor{red}{FALL (Hiba)} & \textcolor{red}{FALL (Hiba)} & \textbf{NORMAL [TN]} & -- \\
Independent-02 (Járókeret) & Esés & FALL & 15.48 s & \textcolor{red}{NORMAL} & \textcolor{red}{NORMAL} & \textbf{FALL (15.84s) [TP]} & $0{,}36$ s \\
\bottomrule
\end{tabularx}
\caption{A fejlesztői kalibrációs mintahalmaz mérési eredményei és a baseline modellek összehasonlítása.}
\label{tab:full_benchmark}
\end{table}

\subsection{Döntési késleltetés analízise (NFR-02 verifikáció)}
Az $NFR\text{-}02$ követelmény előírja, hogy az esés megerősítésének késleltetése 1,0 másodperc alatt maradjon. A késleltetést formálisan a következő összefüggés definiálja:
\begin{equation}
T_{\text{latency}} = T_{\text{detect}} - T_{\text{impact}}
\end{equation}
ahol $T_{\text{impact}}$ a videón manuálisan annotált időbélyeg, amikor az alany teste eléri a maximális függőleges lassulást (földet érés), $T_{\text{detect}}$ pedig az a pillanat, amikor az állapotgép $FALLEN$ állapotba lép.

A mért késleltetési értékek a fejlesztői esési mintákon:
\begin{itemize}
    \item Átlagos késleltetés: $\bar{T}_{\text{latency}} = 0{,}47 \pm 0{,}11$ másodperc (min: $0{,}36$ s, max: $0{,}64$ s).
    \item Ez a késleltetés az állapotgép 12 képkockás ($N_{\text{mem}} = 12$, 25 FPS mellett $\approx 0{,}48$ s) stabilizációs és hiszterézis ablakából adódik. A mérések igazolják, hogy a rendszer a fejlesztői mintákon maradéktalanul teljesíti az $NFR\text{-}02$ követelményt ($T_{\text{latency}} \le 1{,}0$ s).
\end{itemize}

\subsection{Osztályozási metrikák és konfidenciaintervallumok}
Az \ref{tab:metrics}. táblázat bemutatja az összehasonlított rendszerek konfúziós mátrixát és a származtatott osztályozási metrikákat. A kis mintaméret miatti statisztikai bizonytalanságot a binomiális arányokra illesztett \textbf{Wilson-féle 95\%-os konfidenciaintervallumokkal (95\% CI)} számszerűsítjük.

\begin{table}[H]
\centering
\small
\begin{tabularx}{\textwidth}{lcccc}
\toprule
\textbf{Metrika / Jellemző} & \textbf{Egyszerű AR} & \textbf{Naiv kinematika} & \textbf{Javított FSM} & \textbf{95\% CI (Javított FSM)} \\
\midrule
Valós Pozitív (TP) & 3 & 4 & \textbf{5} & -- \\
Hamis Pozitív (FP) & 3 & 3 & \textbf{0} & -- \\
Valós Negatív (TN) & 2 & 2 & \textbf{5} & -- \\
Hamis Negatív (FN) & 2 & 1 & \textbf{0} & -- \\
\midrule
Pontosság (Accuracy) & $50{,}0\%$ & $60{,}0\%$ & \textbf{$100{,}0\%$} & $[67{,}9\%; 100{,}0\%]$ \\
Érzékenység (Recall / TPR) & $60{,}0\%$ & $80{,}0\%$ & \textbf{$100{,}0\%$} & $[56{,}6\%; 100{,}0\%]$ \\
Precízió (Precision / PPV) & $50{,}0\%$ & $57{,}1\%$ & \textbf{$100{,}0\%$} & $[56{,}6\%; 100{,}0\%]$ \\
F1-score & $0{,}545$ & $0{,}667$ & \textbf{$1{,}000$} & -- \\
Téves Pozitív Ráta (FPR) & $60{,}0\%$ & $60{,}0\%$ & \textbf{$0{,}0\%$} & $[0{,}0\%; 43{,}4\%]$ \\
\bottomrule
\end{tabularx}
\caption{Az esésdetektáló modellek összehasonlító metrikái a fejlesztői kalibrációs halmazon ($N=10$).}
\label{tab:metrics}
\end{table}

\textbf{Tudományos értékelés:} A táblázat adatai világosan rámutatnak a kis mintaszám matematikai következményére: bár a fejlesztői mintákon elért pontosság $100{,}0\%$, a Wilson 95\%-os konfidenciaintervallum alsó határa az érzékenység esetén $56{,}6\%$, az FPR felső határa pedig $43{,}4\%$. Ez a számítás szigorúan alátámasztja azt a kutatási következtetést, hogy az $NFR\text{-}04$ ($FPR < 5\%$) és $NFR\text{-}03$ ($TPR \ge 95\%$) követelmények formális verifikációjához több száz videót tartalmazó, független benchmark vizsgálat szükséges.

\section{Hardveres futási teljesítménymérés és profilozás}
A rendszer valós idejű futási képességét ($NFR\text{-}01$) egy átlagos felhasználói munkaállomáson vizsgáltuk meg, dedikált nagy teljesítményű grafikus vezérlő (GPU) nélkül, \textbf{tisztán a központi processzoron (CPU)} futtatva a feldolgozási láncot.

\subsection{A mérési környezet specifikációja}
\begin{itemize}
    \item \textbf{Processzor (CPU):} 6 fizikai magos, 12 szálas asztali processzor (3,60 GHz alapórajel, 4,20 GHz turbó).
    \item \textbf{Operatív memória (RAM):} 16 GB DDR4 (3200 MHz).
    \item \textbf{Futtatókörnyezet:} Python 3.10 / PyTorch CPU backend (AVX2 utasításkészlet-optimalizációval).
    \item \textbf{Bemeneti videó:} $640 \times 480$ képpont felbontású, 25 FPS képkockasebességű stream.
    \item \textbf{Mintaelemszám:} $N = 1500$ egymást követő képkocka mérése.
\end{itemize}

\subsection{Részletes komponensszintű profilozás}
Az \ref{tab:profiling}. táblázat bemutatja az egyes feldolgozási lépések átlagos futási idejét, szórását, valamint az extrém késleltetéseket.

\begin{table}[H]
\centering
\small
\begin{tabularx}{\textwidth}{lXccccc}
\toprule
\textbf{Feldolgozási fázis} & \textbf{Megvalósító modul} & \textbf{Átlag ($\bar{t}$)} & \textbf{Szórás ($\pm\sigma$)} & \textbf{Min.} & \textbf{Max.} & \textbf{p95} \\
\midrule
Képkocka beolvasás & VideoSource (OpenCV) & 1.85 ms & $\pm 0.35$ ms & 1.20 ms & 3.10 ms & 2.40 ms \\
YOLOv8s-Pose inferencia & YOLOv8PoseEstimator (CPU) & 36.40 ms & $\pm 2.10$ ms & 32.50 ms & 40.20 ms & 39.80 ms \\
Kulcspont-kinyerés & KeypointExtractor & 0.85 ms & $\pm 0.12$ ms & 0.60 ms & 1.20 ms & 1.05 ms \\
Kinematika és FSM & KinematicsEngine + FSM & 0.15 ms & $\pm 0.04$ ms & 0.10 ms & 0.30 ms & 0.22 ms \\
GUI renderelés és overlay & GUIController (Tkinter) & 1.05 ms & $\pm 0.25$ ms & 0.70 ms & 1.80 ms & 1.45 ms \\
\midrule
\textbf{Teljes ciklusidő} & \textbf{Teljes pipeline (End-to-End)} & \textbf{40.30 ms} & \textbf{$\pm 2.45$ ms} & \textbf{35.10 ms} & \textbf{46.60 ms} & \textbf{43.80 ms} \\
\textbf{Képkockasebesség (FPS)} & \textbf{Mért átviteli sebesség} & \textbf{24.8 FPS} & \textbf{$\pm 1.9$ FPS} & \textbf{21.5 FPS} & \textbf{28.5 FPS} & \textbf{22.8 FPS} \\
\bottomrule
\end{tabularx}
\caption{A feldolgozási lánc komponensszintű futásidő-profilozása normál asztali CPU-n ($N=1500$ frame).}
\label{tab:profiling}
\end{table}

\subsection{A H4 hipotézis tudományos értékelése}
A fejezet elején kitűzött $H4$ hipotézis vizsgálata:
\begin{itemize}
    \item A teljes feldolgozási lánc átlagos ciklusideje $40{,}30$ ms, amely \textbf{$24{,}8$ FPS képkockasebességnek} felel meg ($1000 / 40{,}30 \approx 24{,}81$).
    \item Bár az átlagos sebesség határesetként megközelíti a valós idejű televíziós és kameraszabványt ($\ge 25{,}0$ FPS), a p95 késleltetés $43{,}80$ ms ($22{,}8$ FPS), a maximális késleltetés pedig $46{,}60$ ms ($21{,}5$ FPS).
    \item Ennek alapján a $H4$ hipotézis jelen prototípus formájában \textbf{részben igazolt}: a számítási lánc képes valós idő közeli működésre asztali CPU-n GPU nélkül, azonban a stabil, ingadozásmentes $\ge 25$ FPS garantálásához a Szakdolgozat 2-ben könnyített modellváltozat (YOLOv8n-Pose) vagy ONNX Runtime INT8 kvantálás bevezetése szükséges.
\end{itemize}

\section{Interaktív operátori és tesztelő felület (GUI)}
A benchmark videók kiértékelésének, lassításának és a telemetriai adatok valós idejű auditálásának támogatására egy önálló grafikus kezelőfelület került megvalósításra Python Tkinter alapokon (\texttt{BenchmarkViewerApp}).

\subsection{A kezelőfelület főbb képességei}
\begin{enumerate}
    \item \textbf{Dinamikus videóvezérlés:} Lehetőséget biztosít tetszőleges tesztvideó betöltésére, léptetésére, megállítására, valamint \textbf{dinamikus lejátszási sebességszorzó} alkalmazására (1,0x valós idő, 1,5x gyorsítás, 2,0x gyorsított audit).
    \item \textbf{Képarány-megőrző dinamikus felskálázás:} A különböző képarányú és felbontású benchmark videókat (pl. $640 \times 480$, $720 \times 576$) torzításmentesen, fekete kitöltősávokkal (\textit{letterboxing}) skálázza fel az egységes $1200 \times 920$ képpontos megjelenítő vászonra.
    \item \textbf{Valós idejű telemetriai HUD (\textit{Heads-Up Display}):} A képernyő felső és alsó információs sávjában színkódolással azonnal kirajzolja az aktuális képkockaszámot és videóidőt, az állapotgép fázisát ($NORMAL$, $UNSTABLE$, $FALLING$, $FALLEN$), a mért fizikai paramétereket ($AR$, $\theta_{\text{torso}}$, $v_y$), valamint a detektált anatómiai csontvázat színkódolt végtagokkal és ízületi pontokkal.
\end{enumerate}
"""

with open(LATEX_PATH, "r", encoding="utf-8") as f:
    latex_content = f.read()

# Replace Chapter 5 in LaTeX
ch5_start = r"\chapter{Kísérleti eredmények és Benchmark kiértékelés}"
ch6_start = r"% ========================================================================="
ch6_marker = r"\chapter{Beágyazott peremhálózati megvalósítás és jövőbeli kitekintés: Raspberry Pi platform}"

if ch5_start in latex_content and ch6_marker in latex_content:
    p1 = latex_content.split(ch5_start)[0]
    p2 = latex_content.split(ch6_marker)[1]
    # Keep the divider comment before ch6 if desired
    updated_latex = p1 + latex_ch5 + "\n\n% " + "="*73 + "\n% 6. FEJEZET: RASPBERRY PI PEREMHÁLÓZATI KITEKINTÉS\n% " + "="*73 + "\n" + ch6_marker + p2
    with open(LATEX_PATH, "w", encoding="utf-8") as f:
        f.write(updated_latex)
    print("[OK] Chapter 5 successfully synchronized in docs/szakdolgozat.tex")
else:
    print("[ERROR] Chapter markers not found in LaTeX file")
