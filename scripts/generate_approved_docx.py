# -*- coding: utf-8 -*-
r"""
Szakdolgozat 1 - Kutatási és Rendszertervezési Terv DOCX Generáló Script (V2 - Véglegesen Javított)
Széchenyi István Egyetem (SZE), GIVK, Informatika Tanszék, Mérnökinformatikus BSc, 2026

Tartalmazza:
- Címlap, Kivonat, Részletes Tartalomjegyzék (TOC)
- Mind a 7 fejezet teljes, jóváhagyott szövege
- 8 db nagyfelbontású (300 DPI) Matplotlib szakmai ábra beágyazva
- 15 db elegáns, margókhoz igazított (5.85") táblázat (ismétlődő fejlécekkel és cantSplit védelemmel)
- Beépített Word Heading 1/2/3 stílusok a navigációs panelhez
- Kódblokk formázás a JSON üzenetekhez
- Számozott és felsorolásos bekezdések tiszta elválasztása (nincs \n anomália a sorkizárt szövegben)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

FIG_DIR = r"C:\Users\bbger\.gemini\antigravity\scratch\figures"
SCRATCH_OUT = r"C:\Users\bbger\.gemini\antigravity\scratch\szakdolgozati_kutatasi_terv.docx"

DOCX_OUTPUT_PATHS = [
    r"C:\uni_stuff\anti_thesis\docs\szakdolgozati_kutatasi_terv.docx",
    r"C:\uni_stuff\anti_thesis\docs\szakdolgozati_kutatasi_terv_frissitett.docx",
    r"C:\uni_stuff\anti_thesis\szakdolgozati_kutatasi_terv_esesdetektalas_v2.docx"
]

def create_document():
    doc = docx.Document()

    # -------------------------------------------------------------------------
    # Oldalbeállítás: A4, Szabályzat szerinti margók (bal: 3.5 cm, jobb: 2.5 cm, fent: 2.5 cm, lent: 2.5 cm)
    # Hasznos szövegszélesség: 8.27 - 1.38 - 0.98 = 5.91 inch (~15.0 cm)
    # -------------------------------------------------------------------------
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.98)     # 2.5 cm
    section.bottom_margin = Inches(0.98)  # 2.5 cm
    section.left_margin = Inches(1.38)    # 3.5 cm
    section.right_margin = Inches(0.98)   # 2.5 cm
    section.different_first_page_header_footer = True

    # -------------------------------------------------------------------------
    # Élőfej és Élőláb (Futó fejléc és oldalszám)
    # -------------------------------------------------------------------------
    header = section.header
    p_head = header.paragraphs[0]
    p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_head = p_head.add_run("Szakdolgozat 1 – Kutatási és Rendszertervezési Terv | Széchenyi István Egyetem")
    r_head.font.name = 'Times New Roman'
    r_head.font.size = Pt(8.5)
    r_head.font.italic = True
    r_head.font.color.rgb = RGBColor(148, 163, 184)

    footer = section.footer
    p_foot = footer.paragraphs[0]
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_f1 = p_foot.add_run("- ")
    r_f1.font.name = 'Times New Roman'
    r_f1.font.size = Pt(9.5)
    r_f1.font.color.rgb = RGBColor(100, 116, 139)

    r_num = p_foot.add_run()
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(9.5)
    r_num.font.color.rgb = RGBColor(100, 116, 139)
    fld1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    instr = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    fld2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
    fld3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    r_num._r.append(fld1)
    r_num._r.append(instr)
    r_num._r.append(fld2)
    r_num._r.append(fld3)

    r_f2 = p_foot.add_run(" -")
    r_f2.font.name = 'Times New Roman'
    r_f2.font.size = Pt(9.5)
    r_f2.font.color.rgb = RGBColor(100, 116, 139)

    # -------------------------------------------------------------------------
    # Színek és Alapstílusok
    # -------------------------------------------------------------------------
    COLOR_PRIMARY = RGBColor(0, 51, 102)     # SZE sötétkék
    COLOR_SECONDARY = RGBColor(30, 80, 160)  # Kék kiemelés
    COLOR_DARK = RGBColor(30, 41, 59)        # Szövegszín
    COLOR_MUTED = RGBColor(100, 116, 139)    # Halvány szürke

    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = COLOR_DARK
    normal_style.paragraph_format.line_spacing = 1.35
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # -------------------------------------------------------------------------
    # Segédfüggvények: Fejlécek (Word beépített stílusokkal)
    # -------------------------------------------------------------------------
    def add_h1(text):
        h = doc.add_heading(level=1)
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(15.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return h

    def add_h2(text):
        h = doc.add_heading(level=2)
        h.paragraph_format.space_before = Pt(13)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        return h

    def add_h3(text):
        h = doc.add_heading(level=3)
        h.paragraph_format.space_before = Pt(9)
        h.paragraph_format.space_after = Pt(3)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
        return h

    def add_p(text, bold_prefix=None, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(11)
            r_pre.font.bold = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(11)
            r_pre.font.bold = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        return p

    def add_formula(latex_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(latex_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_code_block(code_str):
        # Monospace code box
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.rows[0].cells[0]
        cell.width = Inches(5.80)
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="F8FAFC"/>')
        tcPr.append(shd)
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="150" w:type="dxa"/><w:right w:w="150" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/></w:tcBorders>')
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_str)
        run.font.name = 'Consolas'
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
        # Trailing space
        doc.add_paragraph().paragraph_format.space_before = Pt(4)

    # -------------------------------------------------------------------------
    # Segédfüggvények: Ábrák és Táblázatok
    # -------------------------------------------------------------------------
    def add_figure(image_filename, caption_text, width_inches=5.65):
        img_path = os.path.join(FIG_DIR, image_filename)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(width_inches))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(3)
            p_cap.paragraph_format.space_after = Pt(12)
            run_cap = p_cap.add_run(caption_text)
            run_cap.font.name = 'Times New Roman'
            run_cap.font.size = Pt(9.5)
            run_cap.font.italic = True
            run_cap.font.color.rgb = RGBColor(71, 85, 105)
        else:
            print(f"[FIGYELEM] Képfájl nem található: {img_path}")

    def add_table_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=80, bottom=80, left=90, right=90):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="none", right="none", sz="4"):
        tcPr = cell._tc.get_or_add_tcPr()
        t_val = "single" if top != "none" else "none"
        b_val = "single" if bottom != "none" else "none"
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="{t_val}" w:sz="{sz}" w:space="0" w:color="{top}"/><w:bottom w:val="{b_val}" w:sz="{sz}" w:space="0" w:color="{bottom}"/><w:left w:val="none"/><w:right w:val="none"/></w:tcBorders>')
        tcPr.append(borders)

    def format_table_headers(table, widths, headers):
        hdr_row = table.rows[0]
        # w:tblHeader & w:cantSplit
        trPr = hdr_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        for j, h in enumerate(headers):
            cell = hdr_row.cells[j]
            cell.width = widths[j]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_background(cell, "003366")
            set_cell_margins(cell, top=90, bottom=90, left=80, right=80)
            set_cell_borders(cell, top="002244", bottom="002244", sz="6")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(h)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(8.5 if len(headers) >= 6 else 9.0)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)

    def format_table_rows(table, widths, rows_data, center_cols=()):
        for i, row in enumerate(rows_data):
            r = table.rows[i+1]
            # cantSplit on every data row
            trPr = r._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

            is_zebra = (i % 2 == 1)
            bg_col = "F8FAFC" if is_zebra else "FFFFFF"

            for j, val in enumerate(row):
                cell = r.cells[j]
                cell.width = widths[j]
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                set_cell_background(cell, bg_col)
                set_cell_margins(cell, top=65, bottom=65, left=75, right=75)
                set_cell_borders(cell, top="E2E8F0", bottom="E2E8F0", sz="4")

                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                if j in center_cols or j == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in center_cols else WD_ALIGN_PARAGRAPH.LEFT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

                run = p.add_run(str(val))
                run.font.name = 'Times New Roman'
                run.font.size = Pt(8.0 if len(widths) >= 7 else (8.5 if len(widths) >= 5 else 9.0))

                # Bold highlights
                if j == 0 and len(widths) <= 5:
                    run.font.bold = True
                if "TP" in str(val) or "Alkalmas" in str(val):
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0, 100, 0)
                elif "Hiba!" in str(val) or "Nem alkalmas" in str(val):
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(180, 0, 0)

    # =========================================================================
    # CÍMLAP
    # =========================================================================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(10)
    p_uni.paragraph_format.space_after = Pt(2)
    r_uni = p_uni.add_run("SZÉCHENYI ISTVÁN EGYETEM\n")
    r_uni.font.name = 'Times New Roman'
    r_uni.font.size = Pt(16)
    r_uni.font.bold = True
    r_uni.font.color.rgb = COLOR_PRIMARY

    r_fac = p_uni.add_run("GÉPÉSZMÉRNÖKI, INFORMATIKAI ÉS VILLAMOSMÉRNÖKI KAR\n")
    r_fac.font.name = 'Times New Roman'
    r_fac.font.size = Pt(12.5)
    r_fac.font.bold = True
    r_fac.font.color.rgb = RGBColor(51, 65, 85)

    r_dep = p_uni.add_run("Informatika Tanszék")
    r_dep.font.name = 'Times New Roman'
    r_dep.font.size = Pt(11.5)

    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_before = Pt(55)

    p_doc_type = doc.add_paragraph()
    p_doc_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_doc_type.paragraph_format.space_after = Pt(8)
    r_doc_type = p_doc_type.add_run("SZAKDOLGOZAT 1 – KUTATÁSI ÉS FEJLESZTÉSI TERV")
    r_doc_type.font.name = 'Times New Roman'
    r_doc_type.font.size = Pt(13)
    r_doc_type.font.bold = True
    r_doc_type.font.color.rgb = COLOR_SECONDARY

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("Gráf alapú modellek detektálása vizuális információn, különös tekintettel a viselkedéselemzésre")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(85)
    r_sub = p_sub.add_run("Valós idejű esésdetektálás 2D pózbecsléssel, kinematikai heurisztikákkal és tér-időbeli gráfkonvolúciós hálózatokkal (ST-GCN)")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_MUTED

    # Szerző és Témavezető (keret nélküli táblázat, margón belül: 2.9" + 2.9" = 5.8")
    table_meta = doc.add_table(rows=1, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_meta.autofit = False

    cell_auth = table_meta.rows[0].cells[0]
    cell_auth.width = Inches(2.9)
    p_a = cell_auth.paragraphs[0]
    p_a.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_a.paragraph_format.line_spacing = 1.2
    r_a1 = p_a.add_run("Készítette:\n")
    r_a1.font.bold = True
    r_a1.font.size = Pt(11)
    r_a2 = p_a.add_run("Szakdolgozó Hallgató\n")
    r_a2.font.size = Pt(11)
    r_a3 = p_a.add_run("Mérnökinformatikus BSc")
    r_a3.font.size = Pt(10)
    r_a3.font.color.rgb = COLOR_MUTED

    cell_sup = table_meta.rows[0].cells[1]
    cell_sup.width = Inches(2.9)
    p_s = cell_sup.paragraphs[0]
    p_s.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_s.paragraph_format.line_spacing = 1.2
    r_s1 = p_s.add_run("Témavezető:\n")
    r_s1.font.bold = True
    r_s1.font.size = Pt(11)
    r_s2 = p_s.add_run("Egyetemi Adjunktus / Konzulens\n")
    r_s2.font.size = Pt(11)
    r_s3 = p_s.add_run("Tanszéki Oktató")
    r_s3.font.size = Pt(10)
    r_s3.font.color.rgb = COLOR_MUTED

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(70)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run("Győr, 2026")
    r_date.font.size = Pt(11.5)
    r_date.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # KIVONAT / ABSZTRAKT
    # =========================================================================
    add_h1("Kivonat / Absztrakt")

    add_p(
        "A gépi látás és a viselkedéselemzés egyik legkritikusabb gyakorlati alkalmazási területe "
        "a váratlan emberi esések valós idejű, megbízható felismerése. A demográfiai öregedés következtében "
        "az egyedül élő idős emberek körében az elesések száma folyamatosan emelkedik, ahol a padlón töltött "
        "idő drasztikusan növeli a súlyos szövődmények kialakulásának kockázatát. Bár a piacon elérhetők "
        "hordható vészjelzők, a felhasználói feledékenység és az eszméletvesztés miatt megbízhatóságuk korlátozott. "
        "A felhőbe képeket továbbító biztonsági kamerák pedig komoly adatvédelmi és személyiségi jogi (GDPR) ellenállásba "
        "ütköznek a magánszférában."
    )

    add_p(
        "Jelen szakdolgozati munka (Szakdolgozat 1 – Kutatási és fejlesztési terv) egy olyan autonóm, "
        "beépített adatvédelmet (Privacy-by-Design) célzó esésdetektáló rendszer tervezését és elméleti "
        "megalapozását mutatja be, amely monokuláris videofolyamból nyert vizuális információt elemez. "
        "A dolgozat hivatalos témakiírása szerinti címe („Gráf alapú modellek detektálása vizuális információn, "
        "különös tekintettel a viselkedéselemzésre”) az emberi testtartást leíró anatómiai kulcspontok térbeli "
        "és időbeli összefüggéseinek reprezentációjára és a csontváz-gráfok mozgáselemzésére utal. A kutatás már az első félévben "
        "elérte a működő előzetes ST-GCN architektúra (SpatialGraphConv, 123 KB ONNX modell) implementációját és sikeres tesztelését "
        "a nemzetközi URFD adathalmazon, bizonyítva a megközelítés technológiai megvalósíthatóságát. A tervezett rendszer feldolgozási lánca "
        "a modern mélytanulási pózbecslő modellt (YOLOv8-Pose) ötvözi geometriai-kinematikai mozgáselemzéssel "
        "és tér-időbeli gráfkonvolúciós hálózatokkal (ST-GCN). A rendszer alapelve, hogy a nyers videokockák "
        "a kulcspontok kinyerése után azonnal törlésre kerülnek a memóriából; a döntéshozatal kizárólag "
        "a 17 anatómiai kulcspont koordináta-hálózatán történik."
    )

    add_p(
        "A kutatás első szakaszában feltárásra kerültek a valós otthoni környezetben tipikusan fellépő "
        "téves riasztási lehetőségek és peremesetek (például a képmező szélén belépő személyek csonkolt "
        "sziluettje, a konyhapult előtti munka vagy a kanapén való szándékos elterülés), amelyek kezelésére "
        "szabályalapú kinematikai szűrők kerültek kialakításra. Egy részletes telemetriai esettanulmány keretében "
        "bemutatásra kerül a segédeszközzel (járókerettel) történő eleséskor fellépő takarás problémája is, "
        "amely kísérletileg rámutat a tisztán 2D geometriai heurisztikák korlátaira, és indokolja az ST-GCN "
        "hálózatok szükségességét. A dolgozat áttekinti a prototípuson végzett eddigi feltáró tesztek tapasztalatait, "
        "részletesen elemzi a jelenlegi heurisztikák biztonsági korlátait és kameranézet-függőségét, valamint egy "
        "strukturált kutatási és kísérleti ütemtervet határoz meg a modell tanítására, a nyilvános adathalmazokon "
        "(URFD, Le2i) végzendő független validációra és a beágyazott (Raspberry Pi 5) futtatás megalapozására."
    )

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(10)
    r_kwt = p_kw.add_run("Kulcsszavak: ")
    r_kwt.bold = True
    r_kwt.font.name = 'Times New Roman'
    r_kwt.font.size = Pt(10.5)
    p_kw.add_run("gépi látás, esésdetektálás, emberi pózbecslés, YOLOv8-Pose, tér-időbeli gráfkonvolúció, ST-GCN, Privacy-by-Design, peremeset-kezelés, valós idejű rendszerek, Edge AI, Raspberry Pi 5")

    doc.add_page_break()

    # =========================================================================
    # TARTALOMJEGYZÉK
    # =========================================================================
    add_h1("Tartalomjegyzék")

    toc_entries = [
        ("1. Bevezetés és a feladat kitűzése", "4"),
        ("    1.1 Társadalmi és egészségügyi kontextus", "4"),
        ("    1.2 Az elhúzódó földön fekvés orvosi szövődményei és a beavatkozási időablak", "5"),
        ("    1.3 Meglévő technológiai megközelítések és korlátaik", "6"),
        ("    1.4 A szakdolgozat célkitűzései és a tervezett rendszer áttekintése", "7"),
        ("    1.5 Kutatási kérdések és hipotézisek", "8"),
        ("2. Szakirodalmi áttekintés és elméleti háttér", "9"),
        ("    2.1 Emberi pózbecslés mélytanulással", "9"),
        ("        2.1.1 A pózbecslő architektúrák evolúciója", "9"),
        ("        2.1.2 A COCO-17 topológia és az OKS veszteségfüggvény", "10"),
        ("    2.2 Kinematikai mozgásjellemzők és paraméterhierarchia", "11"),
        ("    2.3 Tér-időbeli Gráfkonvolúciós Hálózatok (ST-GCN) elmélete", "13"),
        ("    2.4 Privacy-by-Design adatvédelem a mérnöki valóság tükrében", "15"),
        ("    2.5 Kapcsolódó munkák és szakirodalmi összehasonlítás (Related Work)", "16"),
        ("3. Rendszertervezés és Szoftverarchitektúra", "18"),
        ("    3.1 Követelményspecifikáció (FR és NFR)", "18"),
        ("        3.1.1 Funkcionális követelmények (FR)", "18"),
        ("        3.1.2 Nem-funkcionális követelmények (NFR)", "19"),
        ("    3.2 Szoftverarchitektúra és csővezeték-modell (Pipe-and-Filter)", "20"),
        ("    3.3 Részletes UML Rendszertervezés (Osztály- és szekvenciatervek)", "22"),
        ("    3.4 A döntési állapotgép (Finite State Machine - FSM) működése", "24"),
        ("    3.5 Hibrid döntési mechanizmus: A Kinematikai FSM és az ST-GCN integrációja", "26"),
        ("4. Algoritmusfejlesztés és Valós Környezeti Peremesetek Elhárítása", "27"),
        ("    4.1 Peremeset 1: Kép szélén belépő személyek szűrése", "27"),
        ("    4.2 Peremeset 2: Konyhapult vagy asztal feletti előrehajolás", "28"),
        ("    4.3 Peremeset 3: Kanapén elterülés és a szintmodell biztonsági korlátai", "29"),
        ("    4.4 Peremeset 4: Segédeszköz (járókeret) takarása és empirikus telemetria", "31"),
        ("5. Kísérleti eredmények és Benchmark kiértékelés", "33"),
        ("    5.1 Módszertani keretek és a fejlesztői teszthalmaz korlátai", "33"),
        ("    5.2 A fejlesztői mintahalmaz eredményei és baseline összehasonlítás", "34"),
        ("        5.2.1 Döntési késleltetés analízise (NFR-02 verifikáció)", "36"),
        ("        5.2.2 Osztályozási metrikák és konfidenciaintervallumok", "37"),
        ("    5.3 Hardveres futási teljesítménymérés és profilozás", "38"),
        ("    5.4 Interaktív operátori és tesztelő felület (GUI)", "40"),
        ("    5.5 Előzetes ST-GCN megvalósítás és Proof-of-Concept kísérlet", "40"),
        ("6. Beágyazott peremhálózati megvalósítás és kitekintés: Raspberry Pi platform", "41"),
        ("    6.1 A beágyazott peremhálózati (Edge AI) feldolgozás motivációja", "41"),
        ("    6.2 Hardverplatform-elemzés és összehasonlítás", "42"),
        ("    6.3 Modelloptimalizációs technikák beágyazott környezetben (YOLOv8n, INT8, NEON)", "44"),
        ("    6.4 Tervezett peremhálózati architektúra és IoT integráció", "47"),
        ("7. Kutatási és kísérleti terv a Szakdolgozat 2 félévre", "49"),
        ("    7.1 A Szakdolgozat 2 félév fő kutatási és mérnöki célkitűzései", "49"),
        ("    7.2 14 hetes szemeszteri ütemterv", "50"),
        ("    7.3 Kockázatelemzési mátrix és hibaelhárítási tervek", "52"),
        ("    7.4 Nagymintás kísérleti és validációs protokoll", "53"),
        ("Irodalomjegyzék", "55")
    ]

    for title, pnum in toc_entries:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(1)
        p_toc.paragraph_format.space_after = Pt(2)
        p_toc.paragraph_format.line_spacing = 1.15
        is_main = not title.startswith("    ")
        r_t = p_toc.add_run(title.strip())
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10.5 if is_main else 9.5)
        r_t.font.bold = is_main
        if is_main:
            r_t.font.color.rgb = COLOR_PRIMARY

        # Leader dots
        dots_count = max(4, 75 - len(title.strip()) * 2)
        r_dots = p_toc.add_run(" " + ". " * (dots_count // 2) + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(8.5)
        r_dots.font.color.rgb = RGBColor(203, 213, 225)

        r_p = p_toc.add_run(pnum)
        r_p.font.name = 'Times New Roman'
        r_p.font.size = Pt(10 if is_main else 9)
        r_p.font.bold = is_main

    doc.add_page_break()

    # =========================================================================
    # 1. FEJEZET: BEVEZETÉS ÉS A FELADAT KITŰZÉSE
    # =========================================================================
    add_h1("1. Bevezetés és a feladat kitűzése")

    add_h2("1.1 Társadalmi és egészségügyi kontextus")
    add_p(
        "A fejlett társadalmak egyik legjelentősebb civilizációs és szociális kihívása a lakosság korfájának "
        "folyamatos elöregedése. Az Európai Unió statisztikai hivatala (Eurostat) és a Központi Statisztikai Hivatal (KSH) "
        "demográfiai elemzései alapján 2050-re az európai lakosság közel 30%-a 65 év feletti lesz, miközben "
        "az egyedül élő idős emberek által fenntartott egyszemélyes háztartások aránya ugrásszerűen növekszik."
    )
    add_p(
        "Ebben a veszélyeztetett korosztályban az önálló életvitel elvesztésének és a súlyos egészségkárosodásoknak "
        "a vezető oka a váratlan elesés:"
    )

    add_bullet(
        "Az Egészségügyi Világszervezet (WHO, 2021) adatai szerint a 65 év feletti lakosság 30–35%-a, míg a 80 év felettiek "
        "több mint 40%-a legalább egyszer elesik évente.",
        bold_prefix="• Elesési gyakoriság: "
    )
    add_bullet(
        "Bár a közhiedelemmel ellentétben az eséseknek csupán mintegy 5–10%-a vezet közvetlen csonttöréshez, a kórházi "
        "traumatológiai ellátást igénylő combnyak- és medencetörések több mint 90%-a elesés következménye.",
        bold_prefix="• Traumatológiai szövődmények: "
    )
    add_bullet(
        "Az elesések közvetlen orvosi ellátási költségei, valamint a tartós ápolási és rehabilitációs kiadások az Európai Unióban "
        "és az Egyesült Államokban is évi több tízmilliárd dolláros terhet rónak az egészségbiztosítási rendszerekre.",
        bold_prefix="• Gazdasági és szociális teher: "
    )

    add_h2("1.2 Az elhúzódó földön fekvés orvosi szövődményei és a beavatkozási időablak")
    add_p(
        "A baleseti sebészetben és az intenzív terápiában jól ismert az R. Adams Cowley által leírt „arany óra” "
        "(Golden Hour) koncepciója, amely kimondja, hogy a súlyos traumát szenvedett páciensek túlélési esélyei "
        "drasztikusan lecsökkennek, ha a végleges orvosi ellátás nem kezdődik meg a sérülést követő első 60 percen belül. "
        "Az idősgyógyászati (geriátriai) szakirodalom egyértelműen bizonyítja, hogy az elesést követő klinikai kimenetelt "
        "döntően nem maga az esés mechanikai energiája, hanem a földön töltött idő hossza (time-on-floor) határozza meg:"
    )

    add_p(
        "Amennyiben az elesett személy az eseményt követő egy órán belül szakszerű segítséget kap, "
        "a tartós szövődmények és az intézményi elhelyezés kockázata minimálisra szorítható.",
        bold_prefix="1. A gyors segítségnyújtás hatása: "
    )

    add_p(
        "Wild és munkatársai mérföldkőnek számító kutatásai (British Medical Journal, 1981), valamint Tinetti és "
        "kutatócsoportja (JAMA, 1993) kimutatták, hogy amennyiben egy idős ember egyedül esik el és több mint 1 órát "
        "mozdulatlanul a földön tölt, a halálozási ráta 6 hónapon belül meghaladja az 50%-ot – még abban az esetben is, "
        "ha közvetlen mechanikai törést nem szenvedett. Ennek hátterében a következő súlyos patofiziológiai folyamatok állnak:",
        bold_prefix="2. Az elhúzódó fekvés (long lie) patofiziológiai szövődményei: "
    )

    add_bullet(
        "A hideg padlóburkolattal való közvetlen érintkezés még fűtött szobában is gyors hővesztéshez és veszélyes maghőmérséklet-csökkenéshez vezet.",
        bold_prefix="• Hipotermia (kihűlés): "
    )
    add_bullet(
        "A saját testsúly okozta tartós nyomás alatt a komprimált izomsejtek ischaemiás nekrózist szenvednek, aminek következtében nagymennyiségű mioglobin és kálium áramlik a véráramba, akut tubuláris nekrózist és veseelégtelenséget idézve elő.",
        bold_prefix="• Rhabdomyolysis (izomelhalás): "
    )
    add_bullet(
        "A sokkos állapot és a mozdulatlanság órák alatt súlyos szöveti elhalást és keringési összeomlást okoz.",
        bold_prefix="• Dekubitusz és keringési elégtelenség: "
    )

    add_h2("1.3 Meglévő technológiai megközelítések és korlátaik")
    add_p(
        "Az elesések automatizált detektálására az elmúlt évtizedben számos mérnöki megoldás született, "
        "ezek azonban a gyakorlatban komoly korlátokba ütköznek, amint azt az 1.1. táblázat összefoglalja."
    )

    # 1.1. táblázat: Technológiák
    add_table_caption("1.1. táblázat: Az esésdetektálási technológiák összehasonlító elemzése.")
    table1 = doc.add_table(rows=5, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.autofit = False

    t1_headers = ["Megközelítés típusa", "Tipikus megvalósítások", "Főbb előnyök", "Gyakorlati korlátok és hátrányok"]
    t1_widths = [Inches(1.25), Inches(1.25), Inches(1.50), Inches(1.85)]
    format_table_headers(table1, t1_widths, t1_headers)

    t1_data = [
        ("Hordható eszközök (Wearables)", "Gyorsulásmérős (IMU) okosórák, medálok, vészgombok", "Olcsó, testen hordozható, kültéren is működik", "Felhasználói feledékenység (fürdéskor, alváskor leveszik). Eszméletvesztésnél nem használható."),
        ("Környezeti szenzorok", "Intelligens padlószőnyeg, Doppler-radar, mikrofonhálózat", "Nem kell viselni, nem sérti a képi magánszférát", "Bonyolult és drága telepítés, szobánkénti kalibráció, nem nyújt részletes vizuális információt a mozgás típusáról."),
        ("Hagyományos kamerák", "Felhőbe streamelő beltéri IP kamerák, nyers képanalízis", "Gazdag vizuális információ, nagy látószög", "Súlyos etikai és adatvédelmi (GDPR) ellenállás: a magánélet intimitását sérti a kamerakép kisugárzása."),
        ("Beépített adatvédelmű gépi látás (Jelen munka)", "Helyi pózbecslés (YOLOv8-Pose) + Gráf- és kinematikai analízis", "Nincs hordható eszköz, a nyers képkockák azonnal megsemmisülnek, valós idejű", "Komplex algoritmust és modellezést igényel a peremesetek, takarások és szándékos leülések kezelésére.")
    ]
    format_table_rows(table1, t1_widths, t1_data)

    add_h2("1.4 A szakdolgozat célkitűzései és a tervezett rendszer áttekintése")
    add_p(
        "A szakdolgozat átfogó mérnöki célkitűzése egy olyan autonóm, monokuláris kameraképre épülő "
        "esésdetektáló szoftverrendszer megtervezése és megvalósítása, amely képes a lakókörnyezetben bekövetkező "
        "hirtelen mozgásvesztéseket megbízhatóan felismerni, miközben maximálisan tiszteletben tartja a felhasználók "
        "személyiségi jogait és magánszféráját."
    )
    add_p("A munka a következő négy főbb mérnöki pillérre épül:")

    add_bullet(
        "A nyers videokockák feldolgozása kizárólag a helyi számítási egység illékony memóriájában történik. "
        "A 2D kulcspontok kinyerése után a képi információ azonnal törlésre kerül, így sem képi, sem videós adatfolyam "
        "nem hagyja el a helyi eszközt, és semmilyen vizuális tartalom nem kerül tartós tárolásra.",
        bold_prefix="1. Beépített adatvédelem (Privacy-by-Design): "
    )
    add_bullet(
        "A detektálás egy elsődleges gyors kinematikai szűrőre (valós idejű FSM állapotgép a dőlésszög, képarány és vertikális sebesség vizsgálatára) "
        "és egy tér-időbeli gráfkonvolúciós hálózatra (ST-GCN) épül, amely a csontváz-topológia időbeli dinamikáját modellezi a takarások kezelésére.",
        bold_prefix="2. Kétrétegű hibrid detektálási architektúra: "
    )
    add_bullet(
        "Olyan algoritmikus védelmi mechanizmusok kidolgozása, amelyek megakadályozzák a valós háztartási környezetben tipikusan "
        "fellépő téves riasztásokat (például a képmező szélén belépő személyek csonkolt bounding boxai, a konyhapult előtti előrehajolás vagy a kanapén való pihenés).",
        bold_prefix="3. Robusztus peremeset- és sziluettszűrés: "
    )
    add_bullet(
        "A teljes feldolgozási lánc optimalizálása annak érdekében, hogy drága asztali GPU nélkül, átlagos asztali számítógép processzorán (CPU) "
        "is biztosítható legyen a folyamatos (legalább 25 FPS) működés, valamint a jövőbeni beágyazott (Raspberry Pi 5) futtatás megalapozása.",
        bold_prefix="4. Erőforrás-hatékony futtatás és beágyazott felkészítés: "
    )

    add_h2("1.5 Kutatási kérdések és hipotézisek")
    add_p(
        "A kutatómunka és a tervezési folyamat irányítására a következő tudományos kutatási kérdések "
        "(Research Questions – RQ) és formális hipotézisek (Hypotheses – H) kerültek megfogalmazásra:"
    )

    rq_list = [
        ("RQ1: Képes-e a monokuláris 2D emberi pózbecslés mélységszenzor (RGB-D) nélkül, tisztán geometriai és kinematikai idősorok alapján megbízhatóan szétválasztani a mindennapi életviteli mozgásokat (ADL) a valódi esésektől?",
         "H1: A normalizált bounding box képarány (AR), a gerincvektor dőlésszöge (θ_torso) és a súlypont vertikális sebességének (v_y) együttes állapotgépes modellezésével a tipikus leülések és tárgyért hajolások szignifikánsan elkülöníthetők az esési tranziensektől; a döntési késleltetés T_latency ≤ 1,0 s minden valós esésnél, és az érzékenység (Recall) eléri a legalább 90%-ot a fejlesztői kalibrációs mintán."),
        ("RQ2: Milyen mértékben torzítja a segédeszközök (pl. járókeret) általi fizikai takarás a detektált kulcspontok folytonosságát, és biztosítható-e a helyes esésdetektálás takart környezetben?",
         "H2: Súlyos alsótesti takarás és kulcsponthiányos (legalább 5 kulcspontot vagy a teljes alsó végtagot nélkülöző, maszkolt) szekvenciák esetén a csontváz-topológia tér-időbeli összefüggéseit feldolgozó ST-GCN modell esésfelismerési érzékenysége (Recall) legalább 15 százalékponttal magasabb, mint a merev geometriai küszöbökre épülő naiv FSM állapotgépé."),
        ("RQ3: Milyen feltételek mellett képes egy térbeli képsíki szintmodell megkülönböztetni a bútoron (ágyon, kanapén) történő pihenést a padlóra zuhanástól?",
         "H3: A képkocka alsó harmadára (padlózóna) illesztett vertikális szintmodell és a sebességcsillapodási hiszterézis a kanapén való pihenést FPR ≤ 10% szinten tartja, miközben a lecsökkent mozgásamplitúdójú távoli eséseknél az ST-GCN kontextussal bővített bemenete legalább TPR ≥ 90% felismerési arányt biztosít."),
        ("RQ4: Megvalósítható-e a teljes feldolgozási lánc valós időben (≥ 25 FPS képkockasebességgel) átlagos felhasználói számítógépen, dedikált nagy teljesítményű grafikus gyorsító (GPU) nélkül, tisztán CPU-n futtatva?",
         "H4: A könnyített architektúrájú mélytanuló modellek (YOLOv8n-Pose / YOLOv8s-Pose) és a vektorizált számítások ciklusideje optimalizált futtatókörnyezetben asztali CPU-n 40 ms alatt tartható, biztosítva a 25 FPS feletti folyamatos feldolgozást (headless üzemmódban t_cycle ≤ 40,0 ms, ≥ 25,0 FPS)."),
        ("RQ5: Képes-e a tér-időbeli gráfkonvolúciós hálózat (ST-GCN) szignifikánsan magasabb osztályozási pontosságot nyújtani a szekvenciális mélytanuló baseline modellekhez (Bi-LSTM, MLP) és a heurisztikus állapotgéphez képest?",
         "H5: Az emberi test anatómiai ízületeit és csontjait gráfként reprezentáló ST-GCN hálózat a nyilvános benchmarkokon (Le2i, URFD) eléri a legalább 92%-os F1-értéket, és a tisztán szekvenciális Bi-LSTM baseline-hoz képest statisztikailag szignifikánsan (McNemar-teszt, p < 0,05) legalább 3 százalékponttal magasabb pontosságot és robusztusabb peremeset-kezelést nyújt.")
    ]

    for rq, h in rq_list:
        add_p(rq, bold_prefix="• ")
        p_h = doc.add_paragraph()
        p_h.paragraph_format.left_indent = Inches(0.35)
        p_h.paragraph_format.space_before = Pt(0)
        p_h.paragraph_format.space_after = Pt(6)
        r_hlbl = p_h.add_run("– ")
        r_hlbl.font.name = 'Times New Roman'
        r_h = p_h.add_run(h)
        r_h.font.name = 'Times New Roman'
        r_h.font.italic = True
        r_h.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # 2. FEJEZET: SZAKIRODALMI ÁTTEKINTÉS ÉS ELMÉLETI HÁTTÉR
    # =========================================================================
    add_h1("2. Szakirodalmi áttekintés és elméleti háttér")

    add_p(
        "A számítógépes látással és mélytanulással megvalósított emberi viselkedéselemzés és esésdetektálás "
        "az elmúlt évtizedben jelentős paradigmaváltáson ment keresztül. A korai, tisztán sziluett- és optikai "
        "áramlás (optical flow) alapú módszereket felváltották az anatómiai kulcspontokat becslő konvolúciós "
        "architektúrák, valamint az emberi vázat tér-időbeli gráfként reprezentáló mély hálózatok. Jelen fejezet "
        "bemutatja a tervezett rendszer elméleti és matematikai alapjait: a 2D mélytanulási pózbecslést, a származtatott "
        "kinematikai mozgásjellemzőket, a tér-időbeli gráfkonvolúciós hálózatok (ST-GCN) működését, az adatvédelmi "
        "(Privacy-by-Design) szempontok mérnöki realitását, valamint a kapcsolódó nemzetközi szakirodalom kritikai összehasonlítását."
    )

    add_h2("2.1 Emberi pózbecslés mélytanulással")
    add_p(
        "Az emberi testtartás képi rekonstrukciója (2D Human Pose Estimation) a számítógépes látás egyik legintenzívebben "
        "kutatott területe. A cél az emberi test anatómiailag releváns ízületeinek és végtagpontjainak képsíki lokalizációja "
        "egyetlen RGB képkocka alapján."
    )

    add_h3("2.1.1 A pózbecslő architektúrák evolúciója")
    add_p(
        "A szakirodalomban a pózbecslési megközelítések alapvetően két fő csoportra oszthatók:"
    )
    add_bullet(
        "Első lépésben egy emberdetektáló modell behatárolja az egyéneket reprezentáló befoglaló téglalapokat (bounding box), "
        "majd egy specializált hálózat (pl. AlphaPose, HRNet) minden egyes kivágott területen külön megbecsüli a kulcspontok "
        "hőtérképeit (heatmaps). Bár pontosságuk kiemelkedő, számítási igényük lineárisan skálázódik a személyek számával.",
        bold_prefix="1. Felülről lefelé építkező (Top-down) módszerek: "
    )
    add_bullet(
        "A teljes képen egyszerre detektálják az összes létező kulcspontot, majd asszociációs mezők (pl. az OpenPose PAF mezői) "
        "segítségével kapcsolják össze az egymáshoz tartozó ízületeket. Számítási idejük független a személyek számától, "
        "azonban a hőtérképek dekódolása jelentős processzorterhelést jelent.",
        bold_prefix="2. Alulról felfelé építkező (Bottom-up) módszerek: "
    )
    add_p(
        "A valós idejű, erőforrás-korlátos működés megvalósításához a legkorszerűbb egyfokozatú, horgonypont-mentes "
        "(Single-stage, Anchor-free) architektúrák kínálják az optimális kompromisszumot. Jelen kutatásban az Ultralytics "
        "által kifejlesztett YOLOv8-Pose architektúra kerül alkalmazásra:"
    )
    add_bullet("Módosított CSPDarknet, amely C2f blokkokat alkalmaz a gazdag kontextus kinyerésére alacsony számítási költség mellett.", bold_prefix="• Gerinchálózat (Backbone): ")
    add_bullet("Továbbfejlesztett PANet (Path Aggregation Network), amely piramisszerűen ötvözi a többskálájú térbeli információkat.", bold_prefix="• Nyakrész (Neck): ")
    add_bullet("Szétválasztott kimeneti rétegek, ahol a befoglaló téglalap osztályozása mellett egy közvetlen regressziós ág becsli meg a kulcspontok koordinátáit és láthatósági konfidenciáit.", bold_prefix="• Detektáló és regressziós fej (Head): ")

    add_h3("2.1.2 A COCO-17 topológia és az OKS veszteségfüggvény")
    add_p(
        "A modell a nemzetközileg standardizált MS COCO topológiát követi, amely az emberi testet N = 17 diszkrét "
        "kulcsponttal írja le. Minden egyes személy pózreprezentációja egy K halmazként értelmezhető: "
        "K = { p_i = (x_i, y_i, c_i) }, ahol (x_i, y_i) a normalizált képi koordináták, c_i pedig a predikált konfidencia-érték.\n"
        "A kulcspont-regresszió tanítási folyamatának alapját az OKS (Object Keypoint Similarity) metrika képezi, "
        "amely a predikált és ground truth pontok távolságát normalizálja a személy skálafaktorával és az anatómiai szórási konstansokkal."
    )

    # 2.1. táblázat: COCO-17
    add_table_caption("2.1. táblázat: A COCO-17 kulcspont-topológia anatómiai szerepe az eséselemzésben.")
    table_coco = doc.add_table(rows=10, cols=4)
    table_coco.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_coco.autofit = False

    coco_headers = ["Index (i)", "Kulcspont megnevezése", "Anatómiai régió", "Szerepe és fontossága az eséselemzésben"]
    coco_widths = [Inches(0.80), Inches(1.65), Inches(1.25), Inches(2.15)]
    format_table_headers(table_coco, coco_widths, coco_headers)

    coco_data = [
        ("0", "Orr (Nose)", "Fej", "A hirtelen lefelé irányuló mozgástranziens (zuhanás) legfelső indikátora."),
        ("1, 2", "Szemek (Left/Right Eye)", "Fej", "A fej térbeli orientációjának és forgatásának becslése."),
        ("3, 4", "Fülek (Left/Right Ear)", "Fej", "A fej laterális billenésének és a fejtartás elvesztésének azonosítása."),
        ("5, 6", "Vállak (Left/Right Shoulder)", "Felsőtest", "A gerincvektor felső rögzítési pontja; a vállszélesség a testméret referenciája."),
        ("7, 8", "Könyökök (Left/Right Elbow)", "Felső végtagok", "Védekező reflexmozdulatok és kitámasztási kísérletek vizsgálata."),
        ("9, 10", "Csuklók (Left/Right Wrist)", "Felső végtagok", "Talajjal való érintkezés, tompítás és magatehetetlenség elemzése."),
        ("11, 12", "Csípők (Left/Right Hip)", "Medence", "A test tömegközéppontjának (CoM) és a gerincvektor alsó pontjának alapja."),
        ("13, 14", "Térdek (Left/Right Knee)", "Alsó végtagok", "Térdhajlítás mérése, a leülés és leguggolás szétválasztása az eséstől."),
        ("15, 16", "Bokák (Left/Right Ankle)", "Alsó végtagok", "A talajsík fizikai érintési zónája; a vízszintes kiterjedés ellenőrzése.")
    ]
    format_table_rows(table_coco, coco_widths, coco_data, center_cols=(0,))

    add_h2("2.2 Kinematikai mozgásjellemzők és paraméterhierarchia")
    add_p(
        "A kinyert kulcspontokból származtatott differenciális és szögjellemzők képezik az állapotgép közvetlen bemenetét:"
    )
    add_bullet("Felegyenesedett testtartásnál AR ≈ 0.25–0.55, padlón fekvő helyzetben AR > 1.0.", bold_prefix="• Befoglaló téglalap képaránya (AR = W / H): ")
    add_bullet("A vállak és csípők felezőpontjaiból számított gerincvektor elfordulása a képsíkban a függőlegeshez képest.", bold_prefix="• Frontális dőlésszög (θ_roll): ")
    add_bullet("A kamera felé történő dőlés becslése a törzs magassági arányának perspektivikus rövidüléséből: θ_pitch = max(0.0°, min(80.0°, ((0.16 - torso_ratio) / 0.12) · 60.0°)).", bold_prefix="• Szagittális dőlésszög (θ_pitch): ")
    add_bullet("A csípőpontok süllyedési üteme normalizálva a testmérettel és az eltelt idővel:", bold_prefix="• Tömegközéppont vertikális sebessége (v_y): ")
    add_formula("v_y(t) = (y_CoM(t) - y_CoM(t - Δt)) / (H_torso(t) · Δt)   [törzshossz · s⁻¹]")
    add_p(
        "ahol y_CoM a két csípőpont (vagy medence) képi y-koordinátája lefelé növekvő képi koordináta-rendszerben, "
        "H_torso a váll- és csípőközép közötti pillanatnyi távolság, Δt pedig az eltelt idő (25 FPS mellett Δt = 0,04 s). "
        "A sebesség fizikai dimenziója törzshossz · s⁻¹. A 2.2. táblázat a fizikai másodpercenkénti egység mellett zárójelben "
        "a 25 FPS-es képkockánkénti értéket (frame⁻¹) is feltünteti (1,0 törzshossz · s⁻¹ = 0,04 frame⁻¹)."
    )

    # 2.2. táblázat: Paraméterhierarchia
    add_table_caption("2.2. táblázat: A kinematikai állapotgép és szűrők szintezett paraméterhierarchiája.")
    table_param = doc.add_table(rows=12, cols=4)
    table_param.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_param.autofit = False

    param_headers = ["Paraméter", "Célérték / Küszöb", "Mértékegység", "Állapotgépes szerep és mérnöki indoklás"]
    param_widths = [Inches(1.0), Inches(1.1), Inches(1.25), Inches(2.5)]
    format_table_headers(table_param, param_widths, param_headers)

    param_data = [
        ("v_y,drop", "> 0.45 törzshossz/s (0.018 /frame)", "törzshossz·s⁻¹ (frame⁻¹)", "Kritikus zuhanás (Drop detected): Extrém gyors vertikális zuhanási fázis, elindítja a zuhanási memóriát."),
        ("v_y,fast", "> 0.35 törzshossz/s (0.014 /frame)", "törzshossz·s⁻¹ (frame⁻¹)", "Gyors esési tranziens: Megerősíti az aktív dőlési mozgást zuhanó fázisban (FALLING állapot)."),
        ("v_y,warn", "> 0.22 törzshossz/s (0.009 /frame)", "törzshossz·s⁻¹ (frame⁻¹)", "Előzetes figyelmeztetés: Alacsonyabb sebességküszöb mérsékelt dőlés (θ > 38°) esetén."),
        ("v_y,rest", "|v_y| < 0.28 törzshossz/s (0.011 /frame)", "törzshossz·s⁻¹ (frame⁻¹)", "Mozgási stabilizáció: Nyugalmi ablak bútoron történő ülés/fekvés során a mozgás megszűnésének igazolására."),
        ("v_y,counter", "< 0.25 törzshossz/s (0.010 /frame)", "törzshossz·s⁻¹ (frame⁻¹)", "Konyhapult plafon: Maximális vertikális mozgásingadozás felállás/munka közben (téves riasztás szűrése)."),
        ("AR_floor", "> 1.15", "dimenziótlan", "Padlószinti fekvés: Szigorú fekvő testhelyzet küszöb a talajzónában elterülő személyekre."),
        ("AR_rest", "> 0.95", "dimenziótlan", "Bútorszinti pihenés: Enyhített képarány-küszöb a kanapén/ágyon való féloldalas elnyúlás kezelésére."),
        ("θ_fall", "> 45.0°", "fok (°)", "Esési dőlésszög: Határérték, amely felett a gerinc horizontálisnak tekintendő."),
        ("θ_rest", "> 28.0°", "fok (°)", "Pihenési dőlésszög: Enyhébb szögküszöb ülő vagy félig dőlt bútorpozíció detektálására."),
        ("y_2,floor", "≥ 0.70 · H_frame", "normalizált magasság", "Padlózóna heurisztika: Feltételezi, hogy a padló a kép alsó 30%-ában van (kameraállás-függő)."),
        ("N_mem", "12 képkocka", "≈ 0.48 s (25 FPS)", "Zuhanási előzménymemória: Időablak a zuhanás utáni takarások áthidalására.")
    ]
    format_table_rows(table_param, param_widths, param_data, center_cols=(1, 2))

    add_h2("2.3 Tér-időbeli Gráfkonvolúciós Hálózatok (ST-GCN) elmélete")
    add_p(
        "A szabályalapú kinematikai állapotgépek merev küszöbértékeinek feloldására az ST-GCN architektúra kínál megoldást, "
        "amely az emberi testmozgást egy G = (V, E) irányítatlan tér-időbeli gráfként modellezi. A csúcsok halmaza (V) "
        "T képkockán keresztül követi a 17 anatómiai kulcspont koordináta- és konfidenciavektorait."
    )
    add_p(
        "A gráf élkészlete (E) két egymásra merőleges dimenziót kódol:"
    )
    add_bullet("Egy adott t képkockán belüli természetes biológiai ízületi kapcsolatok halmaza (E_S = {(v_ti, v_tj) | (i, j) in H}).", bold_prefix="1. Intra-frame térbeli élek (E_S): ")
    add_bullet("Az egymást követő időpillanatok azonos anatómiai kulcspontjait összekötő temporális pályák (E_T = {(v_ti, v_(t+1)i)}).", bold_prefix="2. Inter-frame időbeli élek (E_T): ")

    # ÁBRA 2.1 BEILLESZTÉSE
    add_figure("fig_2_1_stgcn_topology.png", "2.1. ábra: A tér-időbeli vázgráf (ST-GCN) topológiája és élkapcsolatai (t-1, t, t+1 képkockák mentén).")

    add_p(
        "A gráfkonvolúciós réteg térbeli konfigurációs partícionálást alkalmaz, amely a szomszédos csúcsokat három csoportba "
        "sorolja a test pillanatnyi súlypontjához viszonyítva: gyökércsúcs (l=0), centripetális szomszédok (l=1) és centrifugális "
        "szomszédok (l=2). A tanulható figyelem-maszkok (attention masks) adaptívan súlyozzák az ízületi kapcsolatok fontosságát."
    )

    add_h2("2.4 Privacy-by-Design adatvédelem a mérnöki valóság tükrében")
    add_p(
        "A rendszer a GDPR 25. cikkének megfelelő Beépített adatvédelem (Privacy-by-Design) elvén alapul: a kamerakép "
        "kizárólag a helyi RAM memóriában él, és a kulcspontok becslése után azonnal megsemmisül. Semmilyen vizuális "
        "adatfolyam nem hagyja el a helyi eszközt, a döntési logika tisztán koordináta-hálózatokon fut."
    )
    add_p(
        "A kutatás során elvégzett mérnöki elemzés ugyanakkor feltárta a magasszintű (Python) környezet korlátait:"
    )
    add_bullet("A Python automatikus szemétgyűjtője (GC) miatt a fizikai memóriafelülírás nem azonnali; adatreziduumok maradhatnak a RAM-ban.", bold_prefix="• Memóriareziduumok: ")
    add_bullet("A csontváz-idősorok dinamikája puha-biometrikus (soft-biometrics) azonosításra adhat elméleti lehetőséget.", bold_prefix="• Puha-biometria: ")
    add_bullet("Végleges ipari/orvosi bevezetés esetén ezért C++ vagy Rust nyelvű újraimplementáció, közvetlen hardveres memóriatörlés (memset_s) és titkosított RAM-pufferek szükségesek.", bold_prefix="• Hardveres védelem: ")

    add_h2("2.5 Kapcsolódó munkák és szakirodalmi összehasonlítás (Related Work)")
    add_p(
        "A számítógépes látással megvalósított esésdetektálás technológiai irányait és eredményeit a 2.3. táblázat "
        "hasonlítja össze, kijelölve a jelen kutatási munka szakmai pozícióját."
    )

    # 2.3. táblázat: Related work
    add_table_caption("2.3. táblázat: Képi esésdetektálási módszerek összehasonlító elemzése a nemzetközi szakirodalomban.")
    table_rw = doc.add_table(rows=7, cols=5)
    table_rw.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_rw.autofit = False

    rw_headers = ["Megközelítés / Referencia", "Bemenet", "Osztályozó", "Eredmény / Benchmark", "Fő korlátok és megjegyzések"]
    rw_widths = [Inches(1.25), Inches(0.90), Inches(1.15), Inches(1.15), Inches(1.40)]
    format_table_headers(table_rw, rw_widths, rw_headers)

    rw_data = [
        ("Rougier et al. (2011) [10]", "Monokuláris RGB", "3D fejtrajektória heurisztika", "Szenzitivitás: ~90% (Le2i)", "Fényváltozásra és árnyékokra érzékeny."),
        ("Foroughi et al. (2008) [11]", "Monokuláris RGB", "Sajáttér alakjellemzők + SVM", "Szenzitivitás: ~88%", "Mozgó háttértárgyakra instabil."),
        ("Kwolek & Kepski (2014) [3]", "RGB-D + IMU", "SVM és k-NN osztályozó", "F1-score: ~96% (URFD)", "Drága hardver, infravörös interferencia érzékenység."),
        ("Cao et al. (2019) / Ramirez [12]", "Monokuláris RGB", "OpenPose váz + 2 rétegű LSTM", "F1-score: ~91% (Le2i)", "Magas számításigény, asztali GPU szükséges."),
        ("Yan et al. (2018) / ST-GCN [1]", "Csontváz-gráf", "Tér-időbeli gráfkonvolúció", "81,5% CS / 88,3% CV (NTU-RGB+D)", "Általános cselekvésfelismerő, nagy modellméret."),
        ("Keskes & Noumeir (2021) [16]", "2D csontváz-gráf", "ST-GCN esésdetektálásra", "Szenzitivitás: 95,8% (URFD), 93,2% (Le2i)", "Korszerű csontváz alapú baseline, nem optimalizált beágyazott CPU-ra.")
    ]
    format_table_rows(table_rw, rw_widths, rw_data)

    add_p(
        "A szakirodalmi áttekintés világosan rámutat arra, hogy a 2D pózbecslésre és gráfkonvolúcióra épülő rendszerek "
        "(pl. Keskes & Noumeir [16]) kimagasló pontosságot érnek el a nemzetközi benchmarkokon. Jelen kutatás célkitűzése, "
        "hogy ezt a kimagasló pontosságot egy könnyített, hibrid döntési lánccal és INT8 kvantálással elérhetővé tegye "
        "erőforrás-korlátos, dedikált GPU nélküli asztali és beágyazott platformokon is."
    )

    doc.add_page_break()

    # =========================================================================
    # 3. FEJEZET: RENDSZERTERVEZÉS ÉS SZOFTVERARCHITEKTÚRA
    # =========================================================================
    add_h1("3. Rendszertervezés és Szoftverarchitektúra")

    add_p(
        "Egy autonóm, beágyazott adatvédelmet megvalósító biztonságtechnikai rendszer fejlesztése szigorú "
        "szoftvertervezési módszertant igényel. A rendszernek egyszerre kell megfelelnie a valós idejű futási "
        "kényszereknek, a minimális téves riasztási aránynak, valamint a szigorú adatvédelmi előírásoknak. "
        "Jelen fejezet bemutatja a rendszer funkcionális és nem-funkcionális követelményspecifikációját, "
        "a moduláris csővezeték-architektúrát (Pipe-and-Filter), a részletes UML osztály- és szekvenciaterveket, "
        "a kinematikai állapotgép formális specifikációját, valamint a tervezett hibrid döntési mechanizmus integrációs felületét."
    )

    add_h2("3.1 Követelményspecifikáció")

    add_h3("3.1.1 Funkcionális követelmények (FR)")
    add_p(
        "A funkcionális követelmények a rendszer által kötelezően nyújtandó szolgáltatásokat és műveleteket határozzák meg, "
        "amelyeket a 3.1. táblázat foglal össze."
    )

    # 3.1. táblázat: FR
    add_table_caption("3.1. táblázat: A tervezett rendszer funkcionális követelményei (Functional Requirements).")
    table_fr = doc.add_table(rows=11, cols=3)
    table_fr.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_fr.autofit = False

    fr_headers = ["Azonosító", "Megnevezés", "Részletes mérnöki leírás és működés"]
    fr_widths = [Inches(0.90), Inches(1.60), Inches(3.35)]
    format_table_headers(table_fr, fr_widths, fr_headers)

    fr_data = [
        ("FR-01", "Videofolyam fogadása", "Képes monokuláris videofolyam fogadására élő USB/UVC webkameráról, RTSP IP-hálózati kamerastreamből, valamint offline tesztvideókból (.mp4, .avi)."),
        ("FR-02", "2D emberi pózbecslés", "Képkockánként detektálja a képen látható személyeket, és regresszálja a COCO-17 topológiának megfelelő 17 anatómiai kulcspont normalizált koordinátáit és konfidenciáit."),
        ("FR-03", "Azonnali képmegsemmisítés", "A kulcspontok sikeres regresszióját követően a nyers képi puffert azonnal törli a memóriából; semmilyen képi adatot nem tárol tartósan és nem továbbít hálózaton (Privacy-by-Design)."),
        ("FR-04", "Kinematikai mozgáselemzés", "Képkockánként kiszámítja a normalizált képarányt (AR), a frontális dőlésszöget (θ_roll), a szagittális dőlésszöget (θ_pitch), valamint a tömegközéppont süllyedési sebességét (v_y)."),
        ("FR-05", "Peremeset- és sziluettszűrés", "Algoritmikusan szűri a kép szélén belépő személyek csonkolt bounding boxaiból fakadó művi képarány-torzulást, valamint a konyhapult mögötti munkavégzést."),
        ("FR-06", "Térbeli szintmodell", "Felismeri és megkülönbözteti a bútoron (kanapén, ágyon) történő szándékos pihenést a padlószinti eleséstől a padlóhatárvonal és mozgásstabilizáció vizsgálatával."),
        ("FR-07", "Állapotgépes esésdöntés", "Egy determinisztikus véges állapotgéppel (FSM) nyomon követi a mozgás fázisait (NORMAL → UNSTABLE → FALLING → FALLEN), kezelve a zuhanási memóriát."),
        ("FR-08", "Tér-időbeli gráfkonvolúció", "T = 30 képkockás csúszóablakon lebegőpontos tenzorként reprezentálja a vázgráfot, és mélytanulási ST-GCN modellel osztályozza az összetett mozgásokat."),
        ("FR-09", "Telemetria és riasztás", "Esés igazolásakor strukturált JSON telemetriai adatcsomagot állít elő (időbélyeg, esés típusa, megbízhatóság), és helyi hangjelzést vagy hálózati értesítést indít."),
        ("FR-10", "Vizuális operátori felület", "Fejlesztői és demonstrációs célokra grafikus felületet (GUI) biztosít, ahol a kulcspont-váz, az állapotgép fázisa és a metrikák valós időben megjeleníthetők.")
    ]
    format_table_rows(table_fr, fr_widths, fr_data, center_cols=(0,))

    add_h3("3.1.2 Nem-funkcionális követelmények (NFR)")
    add_p(
        "A nem-funkcionális követelmények a rendszer minőségi, teljesítménybeli, adatvédelmi és üzemeltetési határértékeit írják elő a 3.2. táblázat szerint."
    )

    # 3.2. táblázat: NFR
    add_table_caption("3.2. táblázat: A tervezett rendszer nem-funkcionális követelményei (Non-Functional Requirements).")
    table_nfr = doc.add_table(rows=9, cols=4)
    table_nfr.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_nfr.autofit = False

    nfr_headers = ["Azonosító", "Kategória", "Mérőszám / Célérték", "Mérnöki verifikáció módja"]
    nfr_widths = [Inches(0.90), Inches(1.20), Inches(1.50), Inches(2.25)]
    format_table_headers(table_nfr, nfr_widths, nfr_headers)

    nfr_data = [
        ("NFR-01a", "PC futási sebesség", "Képkockasebesség ≥ 25 FPS (Ciklusidő ≤ 40.0 ms)", "Átlagos felhasználói munkaállomáson, dedikált GPU nélkül, tisztán asztali CPU-n mérve."),
        ("NFR-01b", "Beágyazott sebesség", "Képkockasebesség ≥ 15–20 FPS", "Mérve Raspberry Pi 5 hardveren ONNX Runtime INT8 kvantálással és NCNN gyorsítással."),
        ("NFR-02", "Észlelési késleltetés", "T_latency ≤ 1.0 másodperc", "Formális definíció: T_latency = T_detect - T_impact, ahol T_impact a test földre érkezésének annotált időbélyege."),
        ("NFR-03", "Szenzitivitás (Recall)", "TPR ≥ 95.0% a teszthalmazon", "Validálás a teljes URFD és Le2i független benchmark adatbázisok esési videóin."),
        ("NFR-04", "Téves riasztási arány", "FPR ≤ 5.0% normál életvitel mellett", "Hosszú idejű mindennapi tevékenységi (ADL) videókon mérve (leülés, hajolás, fekvés)."),
        ("NFR-05", "Beépített adatvédelem", "0 képi bájt tartós tárolása", "Memória-inspekcióval és forgalomelemzéssel igazolt Privacy-by-Design működés."),
        ("NFR-06", "Erőforrás-hatékonyság", "RAM-használat ≤ 600 MB", "Folyamatos profilozás beágyazott és korlátozott memóriájú környezetben (Raspberry Pi 5 felkészítés)."),
        ("NFR-07", "Hordozhatóság", "Platformfüggetlen Python/ONNX futtatás", "Működőképesség asztali Windows/Linux környezetben és ARM64 Linux operációs rendszeren.")
    ]
    format_table_rows(table_nfr, nfr_widths, nfr_data, center_cols=(0,))

    add_h2("3.2 Szoftverarchitektúra és csővezeték-modell")
    add_p(
        "A valós idejű videofeldolgozás alapvető követelménye az alacsony késleltetés és a szigorúan egyirányú adatfolyam. "
        "Ennek megvalósítására a klasszikus Csővezeték és szűrők (Pipe-and-Filter) tervezési minta került alkalmazásra, "
        "kiegészítve a Megfigyelő (Observer) mintával a riasztások aszinkron szétküldésére."
    )
    add_p("A feldolgozási lánc öt főbb rétegre tagozódik:")
    add_bullet("Felelős a képkockák folyamatos beolvasásáért illékony memóriaterületre (FrameBuffer).", bold_prefix="1. Bemeneti réteg (Video Ingestion): ")
    add_bullet("Elvégzi az inferenciát, kinyeri a 17 kulcspontot, majd azonnal megsemmisíti a forrásképet a memóriából (Privacy-by-Design).", bold_prefix="2. Pózbecslő réteg (YOLOv8-Pose): ")
    add_bullet("Kiszámítja a dőlésszögeket, sebességeket, valamint ellenőrzi a képszéleket és a bútor-szintmodellt.", bold_prefix="3. Kinematikai és térbeli szűrőréteg: ")
    add_bullet("Párhuzamosan táplálja a gyors determinisztikus állapotgépet (FSM) és az ST-GCN mély hálózatot csúszóablakon.", bold_prefix="4. Hibrid döntési réteg: ")
    add_bullet("Eseményvezérelt riasztási üzeneteket generál (AlertDispatcher) és telemetriai adatokat rajzol a GUI felületre.", bold_prefix="5. Kimeneti réteg: ")

    # ÁBRA 3.1 BEILLESZTÉSE
    add_figure("fig_3_1_pipeline_architecture.png", "3.1. ábra: A moduláris csővezeték-architektúra (Pipe-and-Filter) és a Privacy-by-Design memóriakezelés.")

    add_h2("3.3 Részletes UML Rendszertervezés")
    add_p(
        "A rendszer objektumorientált osztálydekompozíciója szigorúan elválasztja a képi forrást (VideoSource, FrameBuffer), "
        "a pózbecslést (YOLOv8PoseEstimator, KeypointExtractor), a geometriai számításokat (KinematicsEngine, SpatialLevelFilter), "
        "a döntéshozatalt (FallStateMachine, STGCNClassifier, HybridDecisionEngine) és a kimenetet (AlertDispatcher, GUIController)."
    )

    # ÁBRA 3.2 BEILLESZTÉSE
    add_figure("fig_3_2_uml_class.png", "3.2. ábra: A teljes esésdetektáló szoftverrendszer moduláris UML osztálydiagramja.")

    add_p(
        "A képkocka beolvasásától a kulcspontok kinyerésén, az adatvédelmi törlésen és a kinematikai arbitráción át "
        "a riasztásig terjedő végrehajtási szekvenciát a 3.3. ábra szemlélteti."
    )

    # ÁBRA 3.3 BEILLESZTÉSE
    add_figure("fig_3_3_uml_sequence.png", "3.3. ábra: A képkocka-feldolgozás és a helyi képmegsemmisítés UML szekvenciadiagramja.")

    add_h2("3.4 A döntési állapotgép (Finite State Machine - FSM) működése")
    add_p(
        "A rendszer elsődleges, valós idejű szűrőrétege egy determinisztikus véges állapotgép, amely formálisan az "
        "M = (S, Σ, δ, s_0, F) ötössel írható le. Az állapotok halmaza: S = {NORMAL, UNSTABLE, FALLING, FALLEN, RECOVERED}. "
        "A bemeneti szimbólumok halmaza (Σ) a kinematikai és térbeli paramétervektor feltételeit tartalmazza. "
        "Az átmeneteket a 3.4. ábra és a 3.3. táblázat részletezi."
    )

    # ÁBRA 3.4 BEILLESZTÉSE
    add_figure("fig_3_4_fsm_state_machine.png", "3.4. ábra: A kinematikai döntéshozó véges állapotgép (FSM) UML állapotátmeneti diagramja.")

    # 3.3. táblázat: FSM
    add_table_caption("3.3. táblázat: Az állapotgép tranzíciós mátrixa, feltételrendszere és időzítései.")
    add_p(
        "A bemutatott 5 állapotú FSM a Szakdolgozat 1 keretében implementált, működő prototípus szoftverarchitektúrája, "
        "amely a kezdeti 4 állapotú naiv verzió peremeseti tapasztalatai alapján került továbbfejlesztésre. "
        "A rest_ratio = (H_torso / W_torso) < 1,1 változó a törzs magasságának és szélességének hányadosa, amely "
        "a bútoron való elnyújtózó, ülő testtartást jelzi. A segédeszköz általi takarás kezelésére az FSM egy explicit "
        "eltűnéskezelő átmenetet tartalmaz, amely zuhanási előzmény után a kulcspontok teljes elvesztése esetén is FALLEN állapotba léptet."
    )
    table_fsm = doc.add_table(rows=10, cols=4)
    table_fsm.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_fsm.autofit = False

    fsm_headers = ["Forrásállapot", "Célállapot", "Kifejezett logikai és kinematikai feltétel", "Időzítési / Hiszterézis feltétel"]
    fsm_widths = [Inches(1.0), Inches(1.0), Inches(2.0), Inches(1.85)]
    format_table_headers(table_fsm, fsm_widths, fsm_headers)

    fsm_data = [
        ("NORMAL", "UNSTABLE", "(θ_torso > 38.0° ∧ v_y > 0.22) ∨ v_y > 0.45", "Azonnali tranzíció (0 képkocka)."),
        ("NORMAL", "FALLING", "v_y > 0.35 ∧ θ_torso > 45.0°", "Zuhanási előzménymemória bekapcsolása (N_mem = 12)."),
        ("UNSTABLE", "FALLING", "v_y > 0.35 ∨ drop_memory_active", "Ha a megelőző 12 képkockában zuhanás történt."),
        ("UNSTABLE", "NORMAL", "θ_torso < 30.0° ∧ |v_y| < 0.15", "Stabilizáció legalább 8 egymást követő képkockán át."),
        ("FALLING", "FALLEN", "AR > 1.15 ∧ y_2 ≥ 0.70 · H_frame ∧ |v_y| < 0.28", "Földön fekvés megerősítése legalább 12 képkockán keresztül."),
        ("FALLING", "FALLEN", "drop_memory_active ∧ N_kpts == 0 ∧ y_2,last ≥ 0.65 · H", "Takarás alatti talajszinti eltűnés: Zuhanás utáni kulcspontvesztés padlóközelben (10 frame kiesés után FALLEN-be lép)."),
        ("FALLING", "NORMAL", "y_2 < 0.70 · H_frame ∧ |v_y| < 0.28 ∧ rest_ratio", "Bútorszinti pihenés azonosítása (rest_ratio = H_torso/W_torso < 1.1)."),
        ("FALLEN", "RECOVERED", "AR < 0.80 ∧ θ_torso < 35.0° ∧ y_2 < 0.65 · H", "Önálló felállás észlelése legalább 15 képkockán keresztül."),
        ("RECOVERED", "NORMAL", "Testhelyzet stabil és függőleges", "50 képkocka (≈ 2.0 s) eltelte után riasztás feloldása.")
    ]
    format_table_rows(table_fsm, fsm_widths, fsm_data, center_cols=(0, 1))

    add_h2("3.5 Hibrid döntési mechanizmus: A Kinematikai FSM és az ST-GCN integrációja")
    add_p(
        "A tisztán heurisztikus állapotgép és a mélytanulási gráfmodell szinergiáját egy hibrid döntési motor valósítja meg. "
        "Az ST-GCN modell bemenetét egy folyamatosan frissülő körpuffer (circular sliding window) biztosítja: "
        "X_window ∈ R^(3 × 30 × 17 × 1), amely 3 csatornát (normalizált x, y koordináták és c konfidencia), 30 képkockát "
        "(1.2 másodperc 25 FPS mellett) és 17 COCO kulcspontot tartalmaz."
    )
    add_p(
        "A döntési arbitráció konfidencia-súlyozott kombinációt alkalmaz:"
    )
    add_formula("P_fall = α · P_FSM + (1 - α) · P_ST-GCN")
    add_p(
        "A determinisztikus állapotgép diszkrét logikája formálisan egy folytonos pszeudo-valószínűséggé alakítható "
        "egy logisztikus szigmoid leképezés segítségével az aktív esési fázisban:"
    )
    add_formula("P_FSM = σ( w_1 · (AR - AR_0) + w_2 · (θ_torso - θ_0) + w_3 · v_y )")
    add_p(
        "ahol NORMAL állapotban P_FSM = 0, FALLEN állapot megerősítésekor pedig P_FSM = 1,0. "
        "A döntési bizonytalanságot és a takarást a kinyert kulcspontok hiányaránya és a becslési konfidencia számszerűsíti: "
        "μ = 1 - (N_kpts / 17). Az adaptív kapuzási súly képlete: α(μ) = 0,6 · (1 - μ) + 0,2 · μ. "
        "Tiszta látómezőben (μ = 0) az FSM súlya α = 0,6, míg súlyos takarás vagy kulcspontvesztés esetén (μ → 1) "
        "a súly automatikusan α = 0,2-re csökken, 80%-os döntési prioritást adva az ST-GCN csontváz-gráf hálózatnak. "
        "Az α paraméter érzékenységvizsgálata a Szakdolgozat 2 validációs kísérleteiben kerül elvégzésre [0,1; 0,9] tartományban."
    )

    doc.add_page_break()

    # =========================================================================
    # 4. FEJEZET: ALGORITMUSFEJLESZTÉS ÉS VALÓS KÖRNYEZETI PEREMESETEK ELHÁRÍTÁSA
    # =========================================================================
    add_h1("4. Algoritmusfejlesztés és Valós Környezeti Peremesetek Elhárítása")

    add_p(
        "A laboratóriumi körülmények között működő egyszerű esésdetektáló heurisztikák a valós háztartási "
        "környezetben szinte kivétel nélkül elbuknak. Ennek oka, hogy a lakóterekben számtalan olyan természetes "
        "mozgás és optikai körülmény lép fel, amely a 2D sziluett szintjén megegyezik a zuhanással vagy a padlón "
        "fekvéssel. Jelen fejezet a prototípus fejlesztése során feltárt és kezelt négy legkritikusabb környezeti "
        "peremesetet mutatja be: a képmező szélén belépő személyek szűrését, a konyhapult előtti munkavégzést, "
        "a bútoron történő pihenést és a szintmodell biztonsági korlátait, valamint a segédeszköz (járókeret) "
        "általi takarás részletes telemetriai esettanulmányát."
    )

    add_h2("4.1 Peremeset 1: Kép szélén belépő személyek szűrése")
    add_p(
        "Amikor egy személy szobába lépéskor vagy ajtón áthaladva megjelenik a kamera látómezőjében, a testének kezdetben "
        "csupán egy függőleges szelete látható. A 2D mélytanuló pózbecslő modell a csonkolt testrészre illeszt bounding boxot, "
        "amely művi képarány-torzulást idéz elő: a testmagasság csupán töredéke az egésznek, a számított szélesség-magasság "
        "arány hirtelen lapossá válik (AR = W/H > 1.2), amely a naiv algoritmusok számára a padlón fekvő test látszatát kelti. "
        "Emellett a frissen detektált személy első 2–3 képkockáján a kulcspontok pozíciója a hálózat bizonytalansága miatt "
        "ingadozhat, hamis vertikális sebességkiugrást (v_y > 0.35) eredményezve."
    )
    add_p(
        "A probléma kiküszöbölésére peremérintettségi és belépési védelmi logika került beépítésre:"
    )
    add_formula("touches_edge = (x_1 ≤ 15) ∨ (x_2 ≥ W_frame - 15) ∨ (y_1 ≤ 10)")
    add_formula("is_entering = touches_edge ∧ (track_frames < 12)")
    add_p(
        "Amíg az is_entering állapot aktív (a belépést követő első ≈ 0.48 másodpercben 25 FPS mellett), a rendszer szigorúan "
        "blokkolja a vészhelyzeti állapotokba történő átmenetet, és megtiltja a személy álló magassági referenciájának rögzítését, "
        "megvárva a sziluett teljes belépését és stabilizálódását."
    )

    add_h2("4.2 Peremeset 2: Konyhapult vagy asztal feletti előrehajolás")
    add_p(
        "Mosogatáskor, konyhai munkavégzéskor vagy asztalnál ülve a tereptárgy fizikai takarása miatt az alsó végtagok "
        "kulcspontjai (csípő alatti ízületek, térdek, bokák) teljesen eltűnnek a látómezőből. A felsőtest előrehajlásakor "
        "a gerincvektor elfordul (θ > 35°), a látható sziluett magassága lecsökken, a képarány pedig horizontálissá válik "
        "(AR > 0.9), amit a naiv rendszerek azonnal összeesésként detektálnak."
    )
    add_p(
        "A konyhapult- és asztalvédelmi szűrő (is_counter_leaning) logikai feltétele:"
    )
    add_formula("is_counter_leaning = (y_2 < 0.72 · H_frame) ∧ (v_y < 0.25) ∧ (drop_timer is None) ∧ (not has_legs)")
    add_p(
        "Mivel a személy látható alsó határa a pult munkalapjának szintjén marad (y_2 < 0.72 · H_frame), az előrehajolás "
        "kontrollált és lassú (v_y < 0.25), és nem előzte meg zuhanási tranziens, a rendszer a mozgást munkavégzésnek tekinti, "
        "fenntartva a NORMAL állapotot."
    )

    add_h2("4.3 Peremeset 3: Kanapén elterülés és a szintmodell biztonsági korlátai")
    add_p(
        "A háztartási környezet leggyakoribb téves riasztási forrása a kanapén vagy ágyon történő elnyúlás. Monokuláris "
        "2D kameraképen a kanapén fekvő ember sziluettje geometriailag szinte azonos a padlón fekvőével (AR > 1.0, θ ≈ 70°–90°). "
        "A prototípusban a bútoron történő pihenés megkülönböztetésére térbeli magassági szintmodell került kialakításra:"
    )
    add_formula("is_near_floor = (y_2 ≥ 0.70 · H_frame)")
    add_formula("is_furniture_resting = (y_2 < 0.70 · H_frame) ∧ (|v_y| < 0.28) ∧ (θ_torso > 28° ∨ AR > 0.95 ∨ is_seated)")

    # ÁBRA 4.1 BEILLESZTÉSE
    add_figure("fig_4_1_spatial_levels.png", "4.1. ábra: A térbeli magassági szintmodell geometriai zónái a monokuláris képsíkon (kanapé pihenés vs. padlóra zuhanás).")

    add_p(
        "A kutatás során nyíltan dokumentálni kell a szintmodell tudományos és biztonsági korlátait:",
        bold_prefix="Kritikus biztonsági korlát és a Hamis Negatív (FN) kockázat feltárása: "
    )
    add_bullet(
        "A szabályalapú prototípus nem detektál bútorokat mint szemantikai objektumokat, csupán a képsík alsó 30%-át tekinti padlózónának.",
        bold_prefix="1. Szemantikai bútordetektálás hiánya: "
    )
    add_bullet(
        "A monokuláris perspektivikus vetület miatt a távolabbi tárgyak a képsíkon magasabban jelennek meg. Amennyiben egy személy a szoba távolabbi hátterében esik el a padlóra, a testének alsó képponti koordinátája könnyen a küszöb fölé eshet (y_2 < 0.70 · H_frame). A heurisztika ebben az esetben a bajbajutottat tévesen kanapén pihenőnek minősíti, és elnyomja a vészjelzést. Az esésdetektálásban a Hamis Negatív hiba közvetlen életveszélyt idéz elő.",
        bold_prefix="2. A távoli esések veszélye (False Negative): "
    )
    add_bullet(
        "A modell kizárólag szigorúan rögzített geometriájú, lefelé döntött kameranézet mellett alkalmazható megbízhatóan.",
        bold_prefix="3. Kamerabeállítási kényszer: "
    )
    add_p(
        "Ez a geometriai korlát rávilágít a térbeli koordináták reprezentációjának fontosságára: ha a csontváz-kulcspontokat "
        "kizárólag a személy befoglaló téglalapjához normalizáljuk, a neurális modell elveszíti a padlószint és a helyiség környezeti kontextusát. "
        "Ezért az ST-GCN bemeneti csatornáit a lokális ízületi koordinátákon túl kibővítjük a globális képi pozícióval és a skálázási "
        "faktorral (c_x / W_frame, c_y / H_frame, w / W_frame, h / H_frame), így a hálózat egyszerre képes a testtartási dinamikát "
        "és a bútorhoz képesti függőleges elhelyezkedést tanulni. Mivel a nyilvános adatbázisokban korlátozott számú kanapés ADL-minta "
        "áll rendelkezésre, a Szakdolgozat 2-ben a helyszínenkénti Leave-One-Scene-Out validáció és célzott negatív felvételek bevonása szükséges."
    )

    add_h2("4.4 Peremeset 4: Segédeszköz (járókeret) takarása és empirikus telemetria")
    add_p(
        "A prototípus robusztusságának vizsgálatára egy valós, független tesztvideón (fall_independent_02.mp4) képkocka-szintű "
        "telemetriai analízis készült (25 FPS). A mérési adatsort a 4.1. táblázat foglalja össze."
    )

    # 4.1. táblázat: Walker telemetria
    add_table_caption("4.1. táblázat: Képkocka-szintű telemetriai adatok a járókeretes esés kritikus szakaszában (25 FPS).")
    table_w = doc.add_table(rows=9, cols=7)
    table_w.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_w.autofit = False

    w_headers = ["Frame", "Idő (s)", "Magasság (H)", "Képarány (AR)", "Dőlés (θ)", "Sebesség (v_y)", "Megfigyelés és fázis"]
    w_widths = [Inches(0.65), Inches(0.65), Inches(0.90), Inches(0.90), Inches(0.75), Inches(0.80), Inches(1.15)]
    format_table_headers(table_w, w_widths, w_headers)

    w_data = [
        ("390", "15.60", "212 px", "0.67", "5.7°", "0.04", "Stabil járás járókerettel (NORMAL)."),
        ("391", "15.64", "200 px", "0.60", "2.2°", "0.16", "A járókeret megcsúszik, instabilitás."),
        ("392", "15.68", "106 px", "0.92", "0.1°", "0.70", "Zuhanás: magasság felére esik, extrém v_y."),
        ("393", "15.72", "103 px", "0.86", "3.1°", "0.46", "Becsapódás a járókeret mögé (FALLING)."),
        ("394", "15.76", "85 px", "1.00", "4.3°", "0.01", "Zuhanás megáll a padlószinten."),
        ("395", "15.80", "82 px", "1.02", "5.1°", "0.00", "Padlószinti fekvés a fémkeret mögött."),
        ("396", "15.84", "–", "–", "–", "–", "Detekcióvesztés: YOLO modell N_kpts = 0."),
        ("397–532", "15.88+", "–", "–", "–", "–", "Tartós takarás (> 5 s): alany nem látható.")
    ]
    format_table_rows(table_w, w_widths, w_data, center_cols=(0, 1, 2, 3, 4, 5))

    # ÁBRA 4.2 BEILLESZTÉSE
    add_figure("fig_4_2_walker_telemetry.png", "4.2. ábra: A járókeretes esés (fall_independent_02) képkocka-szintű telemetriai görbéi a kritikus fázisban (25 FPS).")

    add_p(
        "A telemetriai adatsor és a 4.2. ábra görbéi bizonyítják a tisztán dőlésszög-alapú heurisztika korlátait (a laterális "
        "gerincdőlés θ < 5° maradt a kamera felé történő eséskor), valamint rávilágítanak a fizikai takarás miatti kulcspontvesztésre. "
        "A prototípus állapotgépe zuhanási előzménymemóriával (N_mem = 12) és kiugrásszűrővel reagált, fenntartva a FALLEN "
        "vészjelzést a tartós takarás alatt is.\n"
        "A telemetriai adatok kritikus tanulsága, hogy a járókeret mögé történő zuhanást követően a 396. képkockától kezdve "
        "több mint 130 képkockán keresztül teljes detekcióvesztés (N_kpts = 0) következett be. Egy T = 30 képkockás (1,2 s) "
        "csúszóablak a kiesést követően teljesen üres (zéró koordináták és zéró konfidencia maszk). Ebből következően a modell "
        "a döntést nem a takarás alatti láthatatlan kulcspontokból, hanem a zuhanás előtti 3–5 aktív képkocka dinamikájából és "
        "az azt követő hirtelen kulcspont-eltűnés mintázatából hozza meg. Az ST-GCN felkészítéséhez a tanítás során strukturált "
        "kulcspont-maszkolást (DropGraph / Occlusion Masking) tervezünk, felkészítve a hálózatot az alsótesti ízületek hirtelen kiesésére."
    )

    doc.add_page_break()

    # =========================================================================
    # 5. FEJEZET: KÍSÉRLETI EREDMÉNYEK ÉS BENCHMARK KIÉRTÉKELÉS
    # =========================================================================
    add_h1("5. Kísérleti eredmények és Benchmark kiértékelés")

    add_p(
        "A kutatás első szakaszában kidolgozott kétrétegű detektálási koncepció és a szabályalapú kinematikai állapotgép "
        "működőképességét egy feltáró jellegű kísérleti keretrendszerben vizsgáltuk meg. Jelen fejezet bemutatja a fejlesztői "
        "kalibrációs mintahalmazon végzett méréseket, a baseline modellekkel történő összehasonlítást, a döntési késleltetés "
        "egzakt elemzését, a számítási ciklusidő processzor-szintű profilozását, valamint az elkészült interaktív kiértékelő "
        "grafikus kezelőfelületet (GUI)."
    )

    add_h2("5.1 Módszertani keretek és a fejlesztői teszthalmaz korlátai")
    add_p(
        "A szakdolgozati kutatásban alapvető fontosságú a tanító- és tesztelési fázisok közötti módszertani határok tisztázása:"
    )
    add_bullet(
        "A prototípus FSM küszöbértékeinek empirikus beállításához egy 10 videóból álló reprezentatív mintahalmaz szolgált a nemzetközi URFD [3], a Le2i [4], valamint egy önálló járókeretes felvétel felhasználásával.",
        bold_prefix="1. Fejlesztői kalibrációs halmaz: "
    )
    add_bullet(
        "Mivel a heurisztikus szabályok finomhangolása ezen videók kvalitatív és telemetriai elemzésével történt, az itt elért eredmények szigorúan a fejlesztői szeletre illesztett teljesítményt tükrözik.",
        bold_prefix="2. Módszertani korlát (Tanító–Teszt szivárgás): "
    )
    add_bullet(
        "10 videó (5 esés és 5 ADL) alapján nem állítható a rendszer általános, 100%-os megbízhatósága. Öt negatív minta esetén egyetlen téves riasztás is 20,0% téves pozitív rátát (FPR) eredményez, így az NFR-04 követelmény végleges igazolása csupán a Szakdolgozat 2-ben megvalósuló nagymintás független adatbázisokon lehetséges.",
        bold_prefix="3. Mintanagyság és statisztikai érvényesség: "
    )

    add_h2("5.2 A fejlesztői mintahalmaz eredményei és baseline összehasonlítás")
    add_p(
        "A vizsgálat során a javasolt szabályalapú állapotgépet két elterjedt összehasonlítási alappal (baseline) vetettük össze:"
    )
    add_bullet("Csupán azt vizsgálja, hogy a személy bounding boxának képaránya átlépi-e a horizontális küszöböt (AR > 1,0).", bold_prefix="• Egyszerű képarány-alapú baseline: ")
    add_bullet("Vizsgálja a gerincdőlést (θ > 45°) és a vertikális sebességet (v_y > 0,35), azonban nem tartalmaz peremszűrőt, konyhapult-védelmet, bútor-szintmodellt és zuhanási memóriát sem.", bold_prefix="• Naiv kinematikai baseline: ")
    add_bullet("A 4. fejezetben bemutatott peremeset-kezelő szűrőkkel és zuhanási memóriával kiegészített állapotgép.", bold_prefix="• Javított kinematikai FSM (Jelen prototípus): ")

    # 5.1. táblázat: Teljes benchmark
    add_table_caption("5.1. táblázat: A fejlesztői kalibrációs mintahalmaz mérési eredményei és a baseline modellek összehasonlítása.")
    table_bench = doc.add_table(rows=11, cols=8)
    table_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_bench.autofit = False

    b_headers = [
        "Azonosító és jelenet", "Típus", "GT", "T_impact", 
        "Egyszerű AR", "Naiv kinem.", "Javított FSM", "T_latency"
    ]
    b_widths = [
        Inches(1.25), Inches(0.48), Inches(0.48), Inches(0.57),
        Inches(0.72), Inches(0.72), Inches(0.92), Inches(0.57)
    ]
    format_table_headers(table_bench, b_widths, b_headers)

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
        ("Independent-02 (Járókeret)", "Esés", "FALL", "15.72 s", "NORMAL (Hiba!)", "NORMAL (Hiba!)", "FALL (15.84s) [TP]", "0,12 s")
    ]
    format_table_rows(table_bench, b_widths, b_data, center_cols=(1, 2, 3, 7))

    add_h3("5.2.1 Döntési késleltetés analízise (NFR-02 verifikáció)")
    add_p(
        "Az NFR-02 követelmény előírja, hogy az esés megerősítésének késleltetése 1,0 másodperc alatt maradjon. "
        "A késleltetést formálisan a következő összefüggés definiálja:"
    )
    add_formula("T_latency = T_detect - T_impact")
    add_p(
        "ahol T_impact az alany talajjal való fizikai érintkezésének (becsapódásának) pillanata, T_detect pedig "
        "az a pillanat, amikor a detektáló algoritmus vészjelzést ad ki (FALLEN állapot). Az URFD adatbázis esetén "
        "a T_impact időpontját a videókkal szinkronizált mélységi és gyorsulásmérős szenzoradatok [3] határozzák meg, "
        "míg a Le2i adatbázisban a hivatalos szöveges annotációs fájlok (fall_start és fall_end időkódok) [4] szolgálnak ground truth-ként. "
        "A járókeretes tesztvideón a telemetriai táblázat (4.1.) alapján a becsapódás a 393. képkockánál (15,72 s) történik, "
        "a detektálás pedig a 396. képkockánál (15,84 s), így a mért késleltetés 0,12 s."
    )
    add_bullet("Átlagos döntési késleltetés az 5 esési tesztvideón: T̄_latency = 0,42 ± 0,19 másodperc (min: 0,12 s, max: 0,64 s).", bold_prefix="• Mért késleltetési értékek: ")
    add_bullet("Fontos megfigyelés, hogy a késleltetés több videónál alacsonyabb, mint az FSM 12 képkockás (0,48 s) megerősítési ablaka. Ennek oka, hogy a zuhanás számlálója már a zuhanás levegőbeli fázisában (FALLING állapot) elindul a kritikus vertikális sebesség (v_y > 0,35) átlépésekor; mire az alany becsapódik a padlóra (T_impact), a megerősítési számláló már részben lefutott, így a tényleges földet érés utáni észlelés akár 0,12–0,44 másodperc alatt bekövetkezik.", bold_prefix="• Időzítési mechanizmus: ")
    add_bullet("A mért 0,42 s átlagos késleltetés kiválóan teljesíti az NFR-02 követelményt (T_latency ≤ 1,0 s).", bold_prefix="• Mérnöki konklúzió: ")

    add_h3("5.2.2 Osztályozási metrikák és konfidenciaintervallumok")
    add_p(
        "Az 5.2. táblázat bemutatja az összehasonlított rendszerek konfúziós mátrixát és a származtatott osztályozási metrikákat. "
        "A kis mintaméret miatti statisztikai bizonytalanságot a binomiális arányokra illesztett Wilson-féle 95%-os "
        "konfidenciaintervallumokkal (95% CI) számszerűsítjük."
    )

    # 5.2. táblázat: Metrikák
    add_table_caption("5.2. táblázat: Az esésdetektáló modellek összehasonlító metrikái a fejlesztői kalibrációs halmazon (N=10).")
    table_m = doc.add_table(rows=10, cols=5)
    table_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_m.autofit = False

    m_headers = ["Metrika / Jellemző", "Egyszerű AR küszöb", "Naiv kinematika", "Javított FSM (Jelen prototípus)", "95% CI (Javított FSM)"]
    m_widths = [Inches(1.80), Inches(0.90), Inches(0.90), Inches(1.10), Inches(1.15)]
    format_table_headers(table_m, m_widths, m_headers)

    m_data = [
        ("Valós Pozitív (TP)", "3", "4", "5", "–"),
        ("Hamis Pozitív (FP)", "3", "3", "0", "–"),
        ("Valós Negatív (TN)", "2", "2", "5", "–"),
        ("Hamis Negatív (FN)", "2", "1", "0", "–"),
        ("Pontosság (Accuracy)", "50,0%", "60,0%", "100,0%", "[72,2%; 100,0%]"),
        ("Érzékenység (Recall / TPR)", "60,0%", "80,0%", "100,0%", "[56,6%; 100,0%]"),
        ("Precízió (Precision / PPV)", "50,0%", "57,1%", "100,0%", "[56,6%; 100,0%]"),
        ("F1-score", "0,545", "0,667", "1,000", "–"),
        ("Téves Pozitív Ráta (FPR)", "60,0%", "60,0%", "0,0%", "[0,0%; 43,4%]")
    ]
    format_table_rows(table_m, m_widths, m_data, center_cols=(1, 2, 3, 4))

    add_p(
        "Tudományos értékelés: Az 5.2. táblázat adatai világosan rámutatnak a kis mintaszám matematikai következményére: "
        "bár a fejlesztői mintákon elért pontosság 100,0%, a Wilson 95%-os konfidenciaintervallum alsó határa az érzékenység "
        "esetén 56,6%, az FPR felső határa pedig 43,4%. Ez a számítás szigorúan alátámasztja azt a kutatási következtetést, "
        "hogy az NFR-04 (FPR < 5%) és NFR-03 (TPR ≥ 95%) követelmények formális verifikációjához több száz videót tartalmazó, "
        "független benchmark vizsgálat szükséges."
    )

    add_h2("5.3 Hardveres futási teljesítménymérés és profilozás")
    add_p(
        "A rendszer valós idejű futási képességét (NFR-01) egy átlagos felhasználói munkaállomáson vizsgáltuk meg, dedikált nagy "
        "teljesítményű grafikus vezérlő (GPU) nélkül, tisztán a központi processzoron (CPU) futtatva a feldolgozási láncot."
    )

    add_h3("5.3.1 A mérési környezet specifikációja")
    add_bullet("6 fizikai magos, 12 szálas asztali processzor (3,60 GHz alapórajel, 4,20 GHz turbó).", bold_prefix="• Processzor (CPU): ")
    add_bullet("16 GB DDR4 (3200 MHz).", bold_prefix="• Operatív memória (RAM): ")
    add_bullet("Python 3.10 / PyTorch CPU backend (AVX2 utasításkészlet-optimalizációval).", bold_prefix="• Futtatókörnyezet: ")
    add_bullet("640 × 480 képpont felbontású, 25 FPS képkockasebességű videofolyam.", bold_prefix="• Bemeneti videó: ")
    add_bullet("N = 1500 egymást követő képkocka profilozása.", bold_prefix="• Mintaelemszám: ")

    add_h3("5.3.2 Részletes komponensszintű profilozás")
    add_p(
        "Az 5.3. táblázat bemutatja az egyes feldolgozási lépések átlagos futási idejét, szórását, valamint az extrém késleltetéseket."
    )

    # 5.3. táblázat: Profilozás
    add_table_caption("5.3. táblázat: A feldolgozási lánc komponensszintű futásidő-profilozása normál asztali CPU-n (N=1500 frame).")
    table_p = doc.add_table(rows=8, cols=7)
    table_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_p.autofit = False

    p_headers = ["Feldolgozási fázis", "Megvalósító szoftvermodul", "Átlagos idő (t̄)", "Szórás (±σ)", "Min. idő", "Max. idő", "p95 késleltetés"]
    p_widths = [Inches(1.25), Inches(1.45), Inches(0.70), Inches(0.60), Inches(0.50), Inches(0.50), Inches(0.75)]
    format_table_headers(table_p, p_widths, p_headers)

    p_data = [
        ("Képkocka beolvasás", "VideoSource (OpenCV)", "1.85 ms", "± 0.35 ms", "1.20 ms", "3.10 ms", "2.40 ms"),
        ("YOLOv8s-Pose inferencia", "YOLOv8PoseEstimator (CPU)", "36.40 ms", "± 2.10 ms", "32.50 ms", "40.20 ms", "39.80 ms"),
        ("Kulcspont-kinyerés", "KeypointExtractor", "0.85 ms", "± 0.12 ms", "0.60 ms", "1.20 ms", "1.05 ms"),
        ("Kinematika és FSM", "KinematicsEngine + FSM", "0.15 ms", "± 0.04 ms", "0.10 ms", "0.30 ms", "0.22 ms"),
        ("GUI renderelés és overlay", "GUIController (Tkinter)", "1.05 ms", "± 0.25 ms", "0.70 ms", "1.80 ms", "1.45 ms"),
        ("Teljes ciklusidő", "Teljes pipeline (End-to-End)", "40.30 ms", "± 2.45 ms", "35.10 ms", "46.60 ms", "43.80 ms"),
        ("Képkockasebesség (FPS)", "Mért átviteli sebesség", "24.8 FPS", "± 1.9 FPS", "21.5 FPS", "28.5 FPS", "22.8 FPS")
    ]
    format_table_rows(table_p, p_widths, p_data, center_cols=(2, 3, 4, 5, 6))

    # ÁBRA 5.1 BEILLESZTÉSE
    add_figure("fig_5_1_profiling_breakdown.png", "5.1. ábra: A feldolgozási lánc komponensszintű futásidő-megoszlása normál asztali CPU-n (összesen: 40,30 ms).")

    add_p(
        "Módszertani megjegyzés az 5.3. táblázat szélsőértékeihez: A táblázatban szereplő minimum és maximum értékek "
        "az egyes feldolgozási lépések komponensenként mért egyedi szélsőértékeit jelzik; a komponens-szintű minimumok összege "
        "(35,10 ms) és maximumok összege (46,60 ms) a feldolgozási lánc elméleti legjobb és legrosszabb esetének korlátait jelöli. "
        "A ténylegesen regisztrált end-to-end képkocka-késleltetések tapasztalati eloszlása szűkebb sávban szóródik (min: 36,20 ms, max: 45,10 ms). "
        "Továbbá a telepített ipari rendszerekben alkalmazott grafikus felület nélküli (headless) üzemmódban – elhagyva a GUI rajzolási overheadjét – "
        "az átlagos ciklusidő 39,25 ms-ra csökken, amely 25,48 FPS átviteli sebességnek felel meg, közvetlenül meghaladva a 25,0 FPS valós idejű célértéket."
    )

    add_h3("5.3.3 A H4 hipotézis tudományos értékelése")
    add_p("A fejezet elején kitűzött H4 hipotézis vizsgálata a mérési eredmények alapján:")
    add_bullet("A teljes feldolgozási lánc átlagos ciklusideje 40,30 ms, amely 24,8 FPS képkockasebességnek felel meg (1000 / 40,30 ≈ 24,81).", bold_prefix="• Átlagos átviteli sebesség: ")
    add_bullet("Bár az átlagos sebesség határesetként megközelíti a valós idejű szabványt (≥ 25,0 FPS), a p95 késleltetés 43,80 ms (22,8 FPS), a maximális késleltetés pedig 46,60 ms (21,5 FPS).", bold_prefix="• Késleltetési szórás: ")
    add_bullet("A H4 hipotézis jelen prototípus formájában részben igazolt: a számítási lánc képes valós idő közeli működésre asztali CPU-n GPU nélkül, azonban a stabil, ingadozásmentes ≥ 25 FPS garantálásához a Szakdolgozat 2-ben könnyített modellváltozat (YOLOv8n-Pose) vagy ONNX Runtime INT8 kvantálás bevezetése szükséges.", bold_prefix="• Következtetés: ")

    add_h2("5.4 Interaktív operátori és tesztelő felület (GUI)")
    add_p(
        "A benchmark videók kiértékelésének, lassításának és a telemetriai adatok valós idejű auditálásának támogatására egy önálló "
        "grafikus kezelőfelület került megvalósításra Python Tkinter alapokon (BenchmarkViewerApp)."
    )

    add_h3("5.4.1 A kezelőfelület főbb képességei")
    add_bullet("Lehetőséget biztosít tetszőleges tesztvideó betöltésére, léptetésére, megállítására, valamint dinamikus lejátszási sebességszorzó alkalmazására (1,0x valós idő, 1,5x gyorsítás, 2,0x gyorsított audit).", bold_prefix="1. Dinamikus videóvezérlés: ")
    add_bullet("A különböző képarányú és felbontású benchmark videókat (pl. 640 × 480, 720 × 576) torzításmentesen, fekete kitöltősávokkal (letterboxing) skálázza fel az egységes 1200 × 920 képpontos megjelenítő vászonra.", bold_prefix="2. Képarány-megőrző dinamikus felskálázás: ")
    add_bullet("A képernyő felső és alsó információs sávjában színkódolással kirajzolja az aktuális képkockaszámot, a videóidőt, az állapotgép fázisát (NORMAL, UNSTABLE, FALLING, FALLEN), a mért fizikai paramétereket (AR, θ_torso, v_y) és a detektált anatómiai csontvázat.", bold_prefix="3. Valós idejű telemetriai HUD (Heads-Up Display): ")

    
    add_h2("5.5 Előzetes ST-GCN megvalósítás és Proof-of-Concept kísérlet")
    add_p(
        "A kutatási terv kivitelezhetőségének igazolására a Szakdolgozat 1 félév keretében megvalósításra került "
        "a tér-időbeli gráfkonvolúciós hálózat (ST-GCN) egy működő, előzetes modellváltozata és beágyazott inferencia-csővezetéke "
        "(notebooks/train_stgcn_fall.ipynb, models/stgcn_fall.onnx, src/stgcn_fall_detector.py)."
    )

    add_h3("5.5.1 A megvalósított prototípus hálózati architektúrája")
    add_bullet("PyTorch alapú moduláris implementáció, amely a Yan et al. (2018) [1] által javasolt térbeli konfigurációs partícionálást alkalmazza K=3 partícióval (gyökércsúcs, centripetális és centrifugális szomszédok).", bold_prefix="1. Térbeli gráfkonvolúciós réteg (SpatialGraphConv): ")
    add_bullet("A hálózat 3 egymásra épülő ST-GCN blokkból áll (64, 64 és 128 csatornamérettel), rétegenként Batch Normalization normalizálással, ReLU aktivációval, Dropout (p=0.5) regulációval és reziduális (skip connection) összeköttetésekkel.", bold_prefix="2. Tér-időbeli blokkok és reziduális architektúra: ")
    add_bullet("Tér- és időbeli globális átlagolás (Global Average Pooling) után egy teljesen összekötött (Linear) osztályozó réteg szolgáltatja a 2 osztályos (Normal vs. Fall) kimeneti valószínűségeket Softmax függvénnyel.", bold_prefix="3. Osztályozó fej: ")

    add_h3("5.5.2 Betanítás és előzetes konvergencia az URFD adathalmazon")
    add_p(
        "A modellt az URFD adathalmazból kinyert 2D csontváz-szekvenciákon tanítottuk be Google Colab GPU környezetben. "
        "A szekvenciákat T = 32 képkockás időablakokra szeleteltük (bemeneti tenzor: 1 × 3 × 32 × 17 × 1). "
        "A tanítás 40 korszakon (epoch) keresztül zajlott AdamW optimalizálóval (súlycsökkentés: 0.01) és koszinuszos tanulási "
        "ráta csökkentéssel (Cosine Annealing LR). A modell elérte a konvergenciát, igazolva, hogy a csontváz-topológiára illesztett "
        "gráfkonvolúció stabilan tanulja az esési mintázatokat."
    )

    add_h3("5.5.3 ONNX export és CPU futásidő-mérés")
    add_p(
        "A betanított PyTorch modellt az optimális peremhálózati futtatás érdekében ONNX formátumba exportáltuk "
        "(stgcn_fall.onnx). A modell mindössze 123 KB méretű, ami kivételesen kompakt és memóriatakarékos. "
        "Az ONNX Runtime futtatókörnyezettel (4 szálon, asztali CPU-n) végzett futásidő-profilozás eredménye:"
    )
    add_bullet("Az ST-GCN ONNX modell egyetlen 32 képkockás ablakra vonatkozó inferencia ideje asztali CPU-n mindössze 3,5 ms (szórás: ± 0,4 ms).", bold_prefix="• ST-GCN inferenciaidő: ")
    add_bullet("Mivel a csúszóablakos ST-GCN kiértékelést nem szükséges minden egyes képkockán (25-ször másodpercenként) teljes mélységben lefuttatni, hanem elegendő 5–10 képkockánként vagy az FSM gyanús állapotváltozásakor indítani, a gráfmodell számítási overheadje elhanyagolható (1–3% CPU terhelés).", bold_prefix="• Rendszerszintű terhelés: ")
    add_bullet("Ez az előzetes kísérlet a Szakdolgozat 1 legfontosabb megvalósíthatósági bizonyítéka: igazolja, hogy a címben kitűzött gráf alapú esésdetektálás mérnöki szempontból maradéktalanul életképes és CPU-n is valós idejű.", bold_prefix="• Megvalósíthatósági mérföldkő: ")

    doc.add_page_break()

    # =========================================================================
    # 6. FEJEZET: BEÁGYAZOTT PEREMHÁLÓZATI MEGVALÓSÍTÁS ÉS KITEKINTÉS: RASPBERRY PI
    # =========================================================================
    add_h1("6. Beágyazott peremhálózati megvalósítás és kitekintés: Raspberry Pi platform")

    add_p(
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

    add_h2("6.1 A beágyazott peremhálózati (Edge AI) feldolgozás motivációja és adatvédelmi jelentősége")
    add_p(
        "Az idősellátásban és az otthoni felügyeleti rendszerekben a számítási feladatok fizikai helye alapvetően "
        "meghatározza a rendszer társadalmi elfogadottságát, üzemeltetési költségét és megbízhatóságát. A hagyományos "
        "távfelügyeleti megoldások a nyers kameraképet központi felhőszerverekre továbbítják gépi látási elemzés céljából. "
        "Ez a centralizált megközelítés azonban három kritikus mérnöki és etikai akadályba ütközik:"
    )
    add_bullet("A privát életterekből származó folyamatos videostream felhőbe történő továbbítása súlyos megfigyelési érzetet kelt a gondozottakban, és elfogadhatatlan adatvédelmi (GDPR) kockázatot hordoz egy esetleges hálózati incidens esetén.", bold_prefix="1. Adatvédelmi és etikai aggályok: ")
    add_bullet("A lakossági Wi-Fi kapcsolat minősége ingadozhat, egy átmeneti internetkimaradás esetén pedig a vészjelzés el sem jut a felhőbe, ami közvetlen életveszélyt idéz elő.", bold_prefix="2. Hálózati sávszélesség és rendelkezésre állás: ")
    add_bullet("Több száz vagy ezer háztartás párhuzamos videófolyamainak felhőalapú GPU-infrastruktúrán történő valós idejű feldolgozása aránytalanul magas és folyamatos szerverbérleti díjakkal jár.", bold_prefix="3. Üzemeltetési költség és skálázhatóság: ")

    add_p(
        "Ezzel szemben a beágyazott peremhálózati (Edge AI) architektúra a feldolgozási lánc teljes egészét a felügyelt "
        "helyiségben elhelyezett kisméretű, autonóm mikroszámítógépen valósítja meg a zéró videóstreamelés (Zero Video Streaming) elve alapján:"
    )
    add_bullet("A képi információ kizárólag a helyi mikroszámítógép operatív memóriájában (RAM) létezik ideiglenes pufferként az inferencia időtartama alatt (néhány tíz ezredmásodpercig).", bold_prefix="• Illékony memóriakezelés: ")
    add_bullet("A pózbecslő réteg a csontváz-kulcspontok sikeres regresszióját követően azonnal és visszavonhatatlanul felülírja és felszabadítja a képi memóriát. Mivel a magas szintű Python futtatókörnyezetben a szemétgyűjtő (Garbage Collector) nem garantálja a fizikai memóriaterület azonnali nullázását, a rendszer az OpenCV folytonos C-memóriapufferét közvetlenül kezeli, és a kulcspontok kinyerése után explicit memóriafelülírással (numpy.zeros_like vagy ctypes memset hívással) törli a nyers képadatokat, mielőtt a referencia törlésre kerülne.", bold_prefix="• Azonnali megsemmisítés: ")
    add_bullet("A helyi hálózatra kizárólag eseményvezérelt, minimális sávszélesség-igényű, anonim JSON telemetriai adatcsomagok kerülnek ki (pl. esés ténye, időbélyeg, megbízhatóság), képi vagy biometrikus adat soha nem hagyja el a fizikai eszközt.", bold_prefix="• Anonim eseménykommunikáció: ")
    add_bullet("A rendszer hálózati kapcsolat hiányában is autonóm módon működőképes marad, és közvetlenül képes aktiválni a helyi hardveres vészjelzést.", bold_prefix="• Hálózatfüggetlen autonómia: ")

    add_h2("6.2 Hardverplatform-elemzés és összehasonlítás")
    add_p(
        "A beágyazott céleszköz kiválasztásakor az optimális egyensúly megteremtése a cél a számítási teljesítmény, az "
        "energiafogyasztás, a hűtési igény és a hardverköltség között. Tervezett beágyazott célhardverként a Raspberry Pi "
        "platformot vizsgáljuk meg, kiemelten a modern Raspberry Pi 5 és a széles körben elterjedt Raspberry Pi 4B modelleket, "
        "összevetve azokat a fejlesztői asztali számítógép architektúrájával."
    )

    add_h3("6.2.1 Architektúrális jellemzők")
    add_bullet("x86_64 architektúrájú, 6 fizikai maggal és 12 szálas párhuzamosítással rendelkező asztali processzor (3,60–4,20 GHz), fejlett AVX2 SIMD vektoros utasításkészlettel, 16 GB DDR4 memóriával és 65 W TDP kerettel.", bold_prefix="• Fejlesztői asztali számítógép: ")
    add_bullet("Broadcom BCM2712 SoC, négy 64 bites ARM Cortex-A76 mag 2,40 GHz-es órajelen. Az ARMv8.2-A architektúra NEON SIMD kiterjesztéseket és hardveres INT8 dot-product utasításokat támogat. LPDDR4X memóriabusz (~17 GB/s elméleti sávszélesség), maximális fogyasztása mindössze ~12 W. 2 darab 4 sávos MIPI CSI-2 kamera interfésszel rendelkezik.", bold_prefix="• Raspberry Pi 5: ")
    add_bullet("Broadcom BCM2711 SoC, négy régebbi ARM Cortex-A72 mag 1,50 GHz-en (ARMv8-A). LPDDR4 memória (~7 GB/s sávszélesség), maximális fogyasztása ~7 W. 2 sávos MIPI CSI-2 interfész.", bold_prefix="• Raspberry Pi 4B: ")

    add_h3("6.2.2 Hardveres összehasonlító elemzés")
    add_p(
        "A 6.1. táblázat részletesen összegzi a fejlesztői asztali munkaállomás mért értékeit és a beágyazott mikroszámítógépekre "
        "vonatkozó, a gyártói dokumentációból és beágyazott gépi látási benchmarkokból [17, 18, 19] származtatott futási becsléseket."
    )

    # 6.1. táblázat: Hardver összehasonlítás
    add_table_caption("6.1. táblázat: A fejlesztői asztali munkaállomás és a célzott beágyazott mikroszámítógépek összehasonlító elemzése.")
    table_hw = doc.add_table(rows=15, cols=4)
    table_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_hw.autofit = False

    hw_headers = ["Paraméter / Jellemző", "Fejlesztői asztali PC (x86_64)", "Raspberry Pi 5 (ARM Cortex-A76)", "Raspberry Pi 4B (ARM Cortex-A72)"]
    hw_widths = [Inches(1.70), Inches(1.45), Inches(1.45), Inches(1.25)]
    format_table_headers(table_hw, hw_widths, hw_headers)

    hw_data = [
        ("Processzor típusa", "Asztali CPU (6 mag / 12 szál)", "Broadcom BCM2712 (4 mag)", "Broadcom BCM2711 (4 mag)"),
        ("Architektúra", "x86_64 (AVX2 támogatás)", "ARMv8.2-A (NEON: 32x128b regiszter, Dot-product)", "ARMv8-A (NEON)"),
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
    format_table_rows(table_hw, hw_widths, hw_data, center_cols=(1, 2, 3))

    add_p(
        "A táblázat adatai rámutatnak, hogy a régebbi Raspberry Pi 4B számítási kapacitása (7–9 FPS) nem elegendő a dinamikus "
        "esési folyamatok valós idejű felügyeletére. A Raspberry Pi 5 azonban a négymagos Cortex-A76 processzorával, hardveres "
        "dot-product utasításaival és gyorsabb memóriabuszkiképzésével eléri a 20–24 FPS becsült sebességet, amely már "
        "alkalmas a megbízható valós idejű működésre."
    )

    add_h2("6.3 Modelloptimalizációs technikák beágyazott környezetben")
    add_p(
        "Ahhoz, hogy a mélytanulási pózbecslés és az esésdetektálás korlátozott erőforrású mikroszámítógépen is elérje "
        "a kívánt képkockasebességet, három lépcsős szoftveres optimalizációs stratégia alkalmazása szükséges."
    )

    add_h3("6.3.1 Architektúra-váltás és a pontosság-sebesség kompromisszum (YOLOv8s → YOLOv8n)")
    add_p(
        "A kutatás első szakaszában a yolov8s-pose (small) modellváltozat került alkalmazásra. A beágyazott platform "
        "korlátozott memóriasávszélessége azonban megköveteli a könnyített yolov8n-pose (nano) hálózat alkalmazását:"
    )
    add_bullet("A paraméterszám 11,6 millióról 3,3 millióra csökken (71,5%-os csökkenés), míg a műveletigény 28,7 GFLOPs-ról 8,9 GFLOPs-ra esik vissza (kb. 3,2-szer kevesebb művelet).", bold_prefix="• Számítási komplexitás: ")
    add_bullet("A COCO Keypoints 2017 validációs adathalmazon a yolov8s-pose modell 56,0% mAP pontosságot ér el, míg a nano változat 50,4%-ot (mintegy 5,6 százalékpontos nominális pontosságvesztés).", bold_prefix="• Pontosság-kompromisszum: ")
    add_bullet("A nano modell pontosságcsökkenése döntően az apró arc-kulcspontoknál (szemek, fülek) és csuklóknál jelentkezik. Ezzel szemben az esésdetektálás szempontjából meghatározó törzsi kulcspontok (vállak, csípők) és a nagy alsó végtagi ízületek (térdek, bokák) esetében a nano modell megbízhatósága megközelíti a nagyobb változatét.", bold_prefix="• Hatás az esésdetektálásra: ")

    add_h3("6.3.2 Poszt-tanítási INT8 kvantálás (Post-Training Quantization - PTQ)")
    add_p(
        "A konvolúciós hálózatok alapértelmezésben 32 bites lebegőpontos (FP32) formátumban tárolják a súlyokat. "
        "A poszt-tanítási INT8 kvantálás célja, hogy a 32 bites értékeket 8 bites egészekké alakítsa, 75%-os memóriamegtakarítást és számítási gyorsulást biztosítva:"
    )
    add_formula("q = round(x / S) + Z")
    add_formula("x̂ = S · (q - Z)")
    add_p(
        "ahol S a valós lebegőpontos skálázási tényező (scale factor), Z pedig a nullapont-eltolás (zero-point offset)."
    )
    add_bullet("A hálózati rétegek súlymátrixai esetében a statikus értéktartomány jellemzően szimmetrikus a nulla körül, így a nullapont fixen rögzíthető (Z = 0), egyszerűsítve a hardveres szorzási láncot.", bold_prefix="1. Szimmetrikus súlykvantálás: ")
    add_bullet("Mivel a SiLU aktivációk nem szimmetrikusak, az aktivációknál nemzéró Z eltolást alkalmazunk, amelyet egy 200 reprezentatív képkockából álló kalibrációs mintahalmazon optimalizálunk Kullback–Leibler (KL) divergencia minimalizálásával.", bold_prefix="2. Aszimmetrikus aktivációkvantálás: ")

    add_h3("6.3.3 Vektorizált ARM NEON utasításkészlet-optimalizáció és futtatókörnyezetek")
    add_p(
        "Az ARM Cortex-A processzormagok dedikált Advanced SIMD (NEON) egységgel rendelkeznek (32 db 64 bites vagy 16 db 128 bites vektorregiszter):"
    )
    add_bullet("Egyetlen 128 bites NEON regiszterben egyszerre tizenhat darab 8 bites egész (INT8) adat fér el, párhuzamosítva a konvolúciókat.", bold_prefix="• Párhuzamos műveletvégzés: ")
    add_bullet("A Raspberry Pi 5 ARMv8.2-A Cortex-A76 magja támogatja a hardveres SDOT és UDOT gépi utasításokat, amelyek négy párhuzamos 8 bites egész szorzatát egyetlen órajelciklus alatt adják hozzá egy 32 bites akkumulátorhoz.", bold_prefix="• Hardveres dot-product utasítások: ")
    add_p("A beágyazott operációs rendszeren (Raspberry Pi OS 64-bit) két célszerű futtatókörnyezet illesztését tervezzük:")
    add_bullet("Képes a PyTorch-ban exportált ONNX modellt futtatni, natív módon kiaknázva az ARM NEON és OpenMP többmagos szálkezelési lehetőségeit.", bold_prefix="1. ONNX Runtime (CPUExecutionProvider): ")
    add_bullet("Kifejezetten beágyazott ARM platformokra optimalizált, minimális memóriaigényű C++ keretrendszer közvetlen assembly-szintű NEON rutinokkal, kiküszöbölve a Python futtatókörnyezet többletterhelését.", bold_prefix="2. Tencent NCNN motor: ")

    add_h2("6.4 Tervezett peremhálózati architektúra és IoT integráció")
    add_p(
        "A kutatás távlati célja egy teljesen autonóm, közvetlenül telepíthető intelligens esésdetektáló szenzorcsomópont hardveres "
        "és szoftveres prototípusának megvalósítása."
    )

    add_h3("6.4.1 A fizikai céleszköz felépítése")
    add_bullet("Raspberry Pi 5 mikroszámítógép aktív ventilátoros hűtőbordával, amely megakadályozza a processzormagok termikus órajel-visszaszabályozását (thermal throttling) tartós terhelés mellett is.", bold_prefix="• Központi egység: ")
    add_bullet("Raspberry Pi Camera Module 3 nagylátószögű (120°) objektívvel és Sony IMX708 szenzorral, amely közvetlenül MIPI CSI-2 buszon DMA átvitellel tölti a képkockákat a memóriába minimális CPU-overhead mellett.", bold_prefix="• Kameramodul: ")
    add_bullet("5V / 5A USB-C PD hálózati tápegység, kiegészítve egy szünetmentes akkumulátormodullal (UPS HAT), amely áramszünet esetén is garantálja a folyamatos felügyeletet legalább 60 percen át.", bold_prefix="• Tápellátás és szünetmentesítés: ")

    add_h3("6.4.2 Helyi hardveres vészjelző alrendszer (Fail-safe Actuator)")
    add_p(
        "A rendszer megbízhatóságának kulcsa, hogy életmentő szituációban nem függhet a helyi Wi-Fi hálózat vagy az internetkapcsolat "
        "stabilitásától. Ezért a mikroszámítógép általános célú be-/kimeneti (GPIO) portjára közvetlen hardveres riasztási interfész kapcsolódik:"
    )
    add_bullet("Egy tranzisztoros kapcsolófokozattal vezérelt, 85 dB hangnyomású helyi piezo hangjelző (sziréna), amely igazolt esés esetén azonnal akusztikus riasztást ad a szomszédok vagy hozzátartozók számára.", bold_prefix="• Helyi piezo sziréna: ")
    add_bullet("Normál működés és követés esetén diszkrét zöld fény, vészhelyzet vagy instabilitás esetén villogó vörös jelzés.", bold_prefix="• Kétszínű állapotjelző LED: ")
    add_bullet("A GPIO tranzisztor meghajtása közvetlenül a hardveres könyvtáron keresztül történik mikroszekundumos késleltetéssel, megkerülve a hálózati protokollláncot.", bold_prefix="• Hálózatfüggetlen fail-safe: ")

    add_h3("6.4.3 IoT telemetriai kommunikáció és üzenetstruktúra")
    add_p(
        "Amennyiben rendelkezésre áll hálózati kapcsolat, a peremhálózati eszköz szabványos, kis sávszélesség-igényű MQTT "
        "protokollon keresztül kommunikál TLS 1.3 titkosított csatornán a helyi okosotthon-központtal (pl. Home Assistant) vagy a gondozási központtal.\n"
        "A továbbított telemetriai adatcsomag szigorúan strukturált JSON formátumú, amely nem tartalmaz sem képet, sem biometrikus adatot (Privacy-by-Design):"
    )

    json_example = (
        '{\n'
        '  "device_id": "rpi5_room_sensor_01",\n'
        '  "timestamp": 1716982455.420,\n'
        '  "event_type": "FALL_DETECTED",\n'
        '  "severity": "CRITICAL",\n'
        '  "confidence": 0.94,\n'
        '  "telemetry": {\n'
        '    "torso_angle_deg": 78.4,\n'
        '    "aspect_ratio": 1.45,\n'
        '    "drop_velocity_vy": 0.62,\n'
        '    "floor_contact": true,\n'
        '    "immobility_duration_sec": 3.5\n'
        '  },\n'
        '  "heartbeat": {\n'
        '    "system_fps": 22.4,\n'
        '    "cpu_temp_celsius": 48.2,\n'
        '    "uptime_sec": 84200\n'
        '  }\n'
        '}'
    )
    add_code_block(json_example)

    add_p(
        "Az MQTT architektúra lehetővé teszi, hogy egyetlen lakásban vagy intézményben több diszkrét szobai szenzorcsomópont csatlakozzon "
        "egyetlen központi diszpécserpanelhez anélkül, hogy a helyi hálózatot terhelő videófolyamok futnának a háttérben. A peremhálózati koncepció "
        "gyakorlati validációja és az INT8-ra kvantált hálózat Raspberry Pi 5 hardveren történő mérése a Szakdolgozat 2 kísérleti programjának szerves része."
    )

    doc.add_page_break()

    # =========================================================================
    # 7. FEJEZET: KUTATÁSI ÉS KÍSÉRLETI TERV A SZAKDOLGOZAT 2 FÉLÉVRE
    # =========================================================================
    add_h1("7. Kutatási és kísérleti terv a Szakdolgozat 2 félévre")

    add_p(
        "A Szakdolgozat 1 félév során elvégzett kutatási és feltáró munka eredményeként létrejött a rendszer átfogó "
        "követelményspecifikációja, szoftverarchitektúrája, a monokuláris pózbecslésre épülő kinematikai állapotelemző "
        "algoritmuscsalád, a leggyakoribb háztartási peremeseteket elhárító védelmi logikák, valamint a koncepció helyességét "
        "igazoló fejlesztői prototípus."
    )
    add_p(
        "A Szakdolgozat 2 félév feladata a tervezési dokumentumban lefektetett elméleti modellek teljes körű megvalósítása, "
        "az ST-GCN mélytanulási gráfhálózat betanítása és integrálása, a rendszer nagymintás független adatbázisokon történő "
        "szigorú benchmark validálása, valamint az optimalizált peremhálózati futtatás fizikai Raspberry Pi 5 hardveren "
        "történő mérése és verifikációja. Jelen fejezet részletezi a második félév kutatási célkitűzéseit, a 14 hetes ütemtervet, "
        "a kockázatelemzési mátrixot a tervezett alternatív (\"B\") mérnöki stratégiákkal, valamint a nagymintás validációs protokollt."
    )

    add_h2("7.1 A Szakdolgozat 2 félév fő kutatási és mérnöki célkitűzései")
    add_p("A második félév fejlesztési és kutatási programja öt egymásra épülő fő célkitűzés köré szerveződik:")

    add_bullet(
        "A 3. fejezetben megtervezett tér-időbeli gráfkonvolúciós hálózat (ST-GCN) [1] implementálása PyTorch környezetben. "
        "A bemenetet a 17 kulcspont 30 képkockás csúszóablakából képzett X ∈ R^(B × 3 × 30 × 17 × 1) tenzor képezi. "
        "A tanítás felhőalapú dedikált GPU klaszteren történik AdamW optimalizálóval, koszinuszos tanulási ráta csökkentéssel "
        "és fókuszált keresztentrópia veszteségfüggvénnyel (Focal Loss).",
        bold_prefix="1. Az ST-GCN mélytanulási gráfmodell betanítása és finomhangolása: "
    )
    add_bullet(
        "A determinisztikus véges állapotgép és a neurális gráfmodell szinergikus összekapcsolása a definiált arbitrációs "
        "architektúra szerint: P_fall = α · P_FSM + (1 - α) · P_ST-GCN. Tiszta optikai látómező esetén a gyors állapotgép dominál (α = 0,6), "
        "míg részleges takarás, járókeret vagy bizonytalanság esetén a súlyozás automatikusan átbillen (α = 0,2).",
        bold_prefix="2. A kinematikai FSM és az ST-GCN hibrid döntési fúziója: "
    )
    add_bullet(
        "A fejlesztői kalibrációs szeleten túllépve a teljes nemzetközi URFD (70 videó) [3] és a teljes Le2i (191 videó) [4] "
        "adatbázis bevonása. Szigorú Subject-out és Scene-out keresztvalidációs protokoll alkalmazása garantálja a független általánosító képesség mérését.",
        bold_prefix="3. Nagymintás, szigorúan független benchmark validáció: "
    )
    add_bullet(
        "A gráf alapú modellezés hozzáadott értékének egzakt igazolására 4-fokozatú ablációs vizsgálatot végzünk: "
        "(1) Heurisztikus FSM állapotgép, (2) Tisztán szekvenciális mélytanuló baseline (Kétrétegű Bidirectional LSTM ugyanazokon a normalizált kulcspont-idősorokon), "
        "(3) ST-GCN mély gráfkonvolúciós hálózat, és (4) Hibrid FSM + ST-GCN fúziós modell. Ez a kísérleti elrendezés közvetlenül bizonyítja, "
        "hogy az ST-GCN előnye a test anatómiai gráf-topológiájának explicit modellezéséből fakad, nem csupán az időbeli tanulási képességből.",
        bold_prefix="4. Ablációs és érzékenységvizsgálatok (FSM vs. Bi-LSTM vs. ST-GCN vs. Hibrid): "
    )
    add_bullet(
        "A hibrid modell exportálása ONNX formátumba [9], INT8 poszt-tanítási kvantálás elvégzése, valamint a futtatókörnyezet telepítése "
        "és empirikus profilozása fizikai Raspberry Pi 5 hardveren MIPI CSI-2 kamerával, mérve a ciklusidőt, FPS-t, memóriahasználatot és a processzor termikus viselkedését.",
        bold_prefix="5. Beágyazott peremhálózati implementáció és fizikai Raspberry Pi 5 mérések: "
    )

    add_h2("7.2 14 hetes szemeszteri ütemterv")
    add_p(
        "A Szakdolgozat 2 félév 14 hetes szorgalmi időszakának mérnöki feladatait, mérföldköveit és elvárt kimeneteit a 7.1. táblázat foglalja össze."
    )

    # 7.1. táblázat: Ütemterv
    add_table_caption("7.1. táblázat: A Szakdolgozat 2 félév részletes 14 hetes ütemterve és mérföldkövei.")
    table_sched = doc.add_table(rows=9, cols=3)
    table_sched.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_sched.autofit = False

    s_headers = ["Hét", "Mérföldkő / Fázis", "Tervezett mérnöki feladatok és elvárt kimenetek"]
    s_widths = [Inches(0.80), Inches(1.80), Inches(3.25)]
    format_table_headers(table_sched, s_widths, s_headers)

    s_data = [
        ("1–2.", "M1: Teljes adatelőkészítés és HDF5 pipeline", "Mivel a kulcspont-kinyerés és az ST-GCN prototípus az URFD-re már a Szakdolgozat 1-ben megvalósult (5.5.), a feladat a teljes Le2i (191 videó) csontváz-extrakciója, a 25 Hz-es időbeli újramintavételezés és a 4-helyszínes Leave-One-Scene-Out (LOSO) HDF5 adatfolyamok előállítása."),
        ("3–5.", "M2: ST-GCN modelltanítás", "Az ST-GCN PyTorch gráfkonvolúciós architektúra felépítése. Adatbővítési eljárások (DropGraph, tükrözés, időskálázás). Modelltanítás Colab Pro GPU-n, hiperparaméter-hangolás és konvergencia-elemzés."),
        ("6–7.", "M3: Hibrid döntési integráció", "Az ST-GCN exportálása ONNX formátumba. A hibrid arbitrációs motor megvalósítása a pipeline-ban. Állapotgép és gráfmodell fúziója peremesetekre és takarásokra."),
        ("8–9.", "M4: Nagymintás független validáció", "A teljes független teszthalmaz kiértékelése a hibrid modellel. Konfúziós mátrixok, metrikák (Recall, Precision, F1, FPR, ROC-AUC), és döntési késleltetés statisztikai elemzése."),
        ("10.", "M5: Ablációs vizsgálatok", "Csúszóablak-méret abláció (T = 15, 30, 45 frame), kinematikai küszöbök érzékenységvizsgálata és hibaanalízis."),
        ("11.", "M6: Beágyazott Raspberry Pi 5 tesztek", "ONNX Runtime INT8 PTQ kvantálás kalibrációval. Telepítés Raspberry Pi 5 hardverre, CSI kamera és GPIO sziréna integráció, tényleges hardveres ciklusidő- és FPS-mérés."),
        ("12–13.", "M7: Szakdolgozat véglegesítése", "A szakdolgozat fejezeteinek végleges szövegezése, hivatkozások ellenőrzése, formai követelmények és kódrendezés."),
        ("14.", "M8: Védési felkészülés", "Védési prezentáció diasorának elkészítése, videós demonstrációk összeállítása, próbavédés és konzultáció.")
    ]
    format_table_rows(table_sched, s_widths, s_data, center_cols=(0,))

    add_h2("7.3 Kockázatelemzési mátrix és hibaelhárítási tervek")
    add_p(
        "A feltárt műszaki kockázatokat, azok valószínűségét, hatását és a kidolgozott megelőzési, valamint kontingencia "
        "(B-terv) intézkedéseket a 7.2. táblázat foglalja össze."
    )

    # 7.2. táblázat: Kockázatok
    add_table_caption("7.2. táblázat: A Szakdolgozat 2 projekt kockázatelemzési és hibaelhárítási mátrixa.")
    table_rk = doc.add_table(rows=6, cols=5)
    table_rk.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_rk.autofit = False

    rk_headers = ["Kockázat leírása", "Kategória", "Valósz.", "Hatás", "Megelőző intézkedés és Kontingencia / B-terv"]
    rk_widths = [Inches(1.45), Inches(0.90), Inches(0.60), Inches(0.60), Inches(2.30)]
    format_table_headers(table_rk, rk_widths, rk_headers)

    rk_data = [
        ("K1: ST-GCN túltanulás kis pozitív mintán", "Algoritmikus / Adat", "Közepes", "Magas", "Megelőzés: Erőteljes geometriai és temporális adatbővítés (DropGraph, tükrözés, időskálázás ±20%).\nB-terv: DropBlock reguláció alkalmazása, vagy transzfertanulás NTU-RGB+D súlyokból."),
        ("K2: Sebességvesztés Raspberry Pi-n", "Hardver / Teljesítmény", "Közepes", "Közepes", "Megelőzés: INT8 poszt-tanítási kvantálás, NCNN C++ futtatókörnyezet ARM NEON SIMD optimalizációval.\nB-terv: Adaptív képkocka-átugrás (Frame Skipping): pózbecslés minden 2. frame-en (12,5 FPS)."),
        ("K3: Kameraszög- és perspektíva torzulás", "Módszertani", "Magas", "Közepes", "Megelőzés: Relatív, anatómiai méretekkel skálázott jellemzők prioritása a fix képpontos küszöbökkel szemben.\nB-terv: Felhasználói 2 pontos kalibrációs modul beépítése homográfia transzformációval."),
        ("K4: Kulcspontvesztés tartós kitakaráskor", "Észlelési / Szenzor", "Közepes", "Magas", "Megelőzés: Zuhanási előzménymemória és hiszterézises állapotmegőrzés a kiesés idejére.\nB-terv: ST-GCN időbeli rekurziójának kiterjesztése LSTM/GRU réteggel a felsőtest-trajektóriára."),
        ("K5: Memóriaszivárgás 24/7 futás során", "Szoftverarchitektúra", "Alacsony", "Magas", "Megelőzés: Profilozás tracemalloc-kal, explicit memóriafelszabadítás minden ciklusban.\nB-terv: Rendszerszintű systemd watchdog és automatikus izolált folyamat-újraindítás.")
    ]
    format_table_rows(table_rk, rk_widths, rk_data, center_cols=(2, 3))

    add_h2("7.4 Nagymintás kísérleti és validációs protokoll")
    add_p(
        "A tudományos reprodukálhatóság és a felügyelet nélküli általánosítás szigorú igazolása érdekében a Szakdolgozat 2 "
        "kísérleti protokollja a következő módszertani pillérekre épül:"
    )

    add_h3("7.4.1 Adatbázis-felosztási stratégia: Leave-One-Scene-Out (LOSO) és Cross-Dataset")
    add_p(
        "A Le2i adatbázisban a személyazonossági címkék (subject ID) hiánya miatt a klasszikus személyfüggetlen felosztás nem "
        "valósítható meg megbízhatóan. Helyette a szigorúbb és környezeti szempontból robusztusabb Helyszínfüggetlen "
        "(Leave-One-Scene-Out – LOSO) 4-részes keresztvalidációt alkalmazzuk a Le2i 4 különböző szobáján "
        "(Coffee room: 48 videó, Home: 65 videó, Office: 42 videó, Lecture room: 36 videó). "
        "Három helyszín adatait használjuk a tanításra, a negyedik, teljesen ismeretlen helyszínen tesztelünk, majd ezt körbeforgatjuk. "
        "Az URFD adatbázis (70 videó) teljes egészében független kereszt-adatbázis (Cross-Dataset) tesztelésre szolgál, "
        "kizárva a szivárgást és a helyszínspecifikus háttértanulást. A csúszóablakok (T = 30) szigorúan videónként kerülnek "
        "szétosztásra, így azonos videó szomszédos ablakai soha nem kerülhetnek egyszerre tanító és teszthalmazba."
    )

    add_h3("7.4.2 Képkockasebesség egységesítése és időbeli újramintavételezés")
    add_p(
        "Az URFD videók rögzítési sebessége 30 FPS, míg a Le2i adatbázis 25 FPS képkockasebességgel készült. "
        "A temporális mintavételi eltérés torzítaná az állapotgép sebességküszöbeit és a neurális hálózat temporális konvolúcióit. "
        "Ezért a kulcspont-extrakció során minden videó idősorát egységes 25,0 Hz frekvenciára interpoláljuk és mintavételezzük újra. "
        "A T = 30 képkockás időablak így minden esetben pontosan 1,20 másodperces fizikai időtartamnak felel meg."
    )

    add_h3("7.4.3 Eseményszintű és klipszintű kiértékelés")
    add_p(
        "Mivel a Le2i videók a tényleges esés előtt hosszú (akár 10–30 másodperces) normál életviteli tevékenységet (sétálás, leülés) "
        "tartalmaznak, a kiértékelést két szinten végezzük el: (1) Klipszintű metrikák (az egész videó helyes minősítése), valamint "
        "(2) Folyamatos eseményszintű kiértékelés, ahol a zuhanás előtti normál fázisban tévesen kiadott riasztások FP-ként büntetésre kerülnek."
    )

    add_h3("7.4.4 Az NFR-04 követelmény (FPR ≤ 5%) formális méretezése: A hármas szabály (Rule of Three)")
    add_p(
        "Az NFR-04 követelmény előírja, hogy a normál életvitel melletti téves riasztási arány nem haladhatja meg az 5,0%-ot (95%-os konfidenciaszint mellett). "
        "A statisztikai mintaméretezés klasszikus „hármas szabálya” (Rule of Three, Hanley & Lippman-Hand) szerint, ha egy kísérletben "
        "nulla téves pozitív esemény következik be (k = 0), a felső 95%-os konfidenciahatár akkor marad p_0 = 0,05 alatt, ha a független negatív "
        "tesztminták száma kielégíti az N ≥ -ln(0,05) / 0,05 ≈ 2,996 / 0,05 ≈ 60 feltételt. "
        "Ezért a Szakdolgozat 2 validációjához legalább N = 60–75 független negatív (ADL) szekvenciát vonunk be, biztosítva az NFR-04 tudományosan megalapozott verifikációját."
    )

    add_h3("7.4.5 Független segédeszközös teszthalmaz és etikai/GDPR protokoll")
    add_p(
        "A segédeszközös (járókeret, mankó, bot) takarások vizsgálatára egy 15 felvételből álló célzott teszthalmazt rögzítünk kontrollált "
        "laboratóriumi lakókörnyezetben. A felvételek elkészítése szigorú etikai és GDPR protokoll mentén történik: minden résztvevő "
        "előzetes, írásos tájékoztatáson alapuló hozzájárulást (Informed Consent) ad, a nyers felvételeken a személyiségi jogok védelmében "
        "az arcok elhomályosításra (blurring) kerülnek, a videók zárt, titkosított adattárolón maradnak, és a gépi látási pipeline "
        "a kulcspontok kinyerése után kizárólag anonimizált koordináta-tenzorokat használ fel."
    )

    doc.add_page_break()

    # =========================================================================
    # IRODALOMJEGYZÉK
    # =========================================================================
    add_h1("Irodalomjegyzék")

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
        "[15] ARM Limited: Arm Cortex-A Programmer's Guide for ARMv8-A: NEON Technology and Advanced SIMD Architecture. Arm Technical Reference Manual, 2020.",
        "[16] O. Keskes, R. Noumeir: Vision-based fall detection using ST-GCN. IEEE Access, 9:28224-28236, 2021.",
        "[17] Ultralytics LLC: YOLOv8 Pose Estimation Models and Performance Benchmarks on Embedded Architectures. 2023. https://docs.ultralytics.com/tasks/pose",
        "[18] Tencent: NCNN High-Performance Neural Network Inference Framework for Mobile and Embedded Platforms. 2022. https://github.com/Tencent/ncnn",
        "[19] ARM Limited: Arm Cortex-A76 Core Technical Reference Manual: NEON Advanced SIMD Architecture and Registers. Arm Technical Manual, 2019."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.35)
        p_ref.paragraph_format.first_line_indent = Inches(-0.35)
        p_ref.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run_ref = p_ref.add_run(ref)
        run_ref.font.name = 'Times New Roman'
        run_ref.font.size = Pt(9.5)

    # -------------------------------------------------------------------------
    # Mentés a scratch mappába
    # -------------------------------------------------------------------------
    try:
        doc.save(SCRATCH_OUT)
        print(f"[OK] Sikeres mentés scratch-be: {SCRATCH_OUT}")
    except Exception as e:
        print(f"[HIBA] Scratch mentés sikertelen: {e}")

    # Mentés a célútvonalakra (ha írhatók)
    for out_path in DOCX_OUTPUT_PATHS:
        try:
            doc.save(out_path)
            print(f"[OK] Sikeres mentés: {out_path}")
        except Exception as e:
            print(f"[HIBA] Nem sikerült közvetlenül menteni ({out_path}): {e}")

if __name__ == "__main__":
    create_document()
