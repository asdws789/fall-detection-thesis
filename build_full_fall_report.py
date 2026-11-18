# -*- coding: utf-8 -*-
r"""
Szakdolgozati Teljes Beszámoló Generátor Script (Esésdetektálás + Raspberry Pi Edge AI)
Összefűzi a 4 részt:
- PART1_MD (Címlap, Absztrakt, 1. Bevezetés, 2. Célok és Hipotézisek)
- PART2_MD (3. Szakirodalom: YOLOv8-Pose, ST-GCN, INT8 Kvantálás & ARM NEON)
- PART3_MD (4. Rendszerarchitektúra és UML, 5. Empirikus Esettanulmány: Törpe-osztó Anomália)
- PART4_MD (6. Adathalmazok, 7. Metrikák és Edge Profiling, 8. Kockázatok, 9. Ütemterv, 10. GDPR, 11. Vázlat, 12. Irodalomjegyzék)

Generálja:
1. C:\uni_stuff\anti_thesis\szakdolgozati_kutatasi_terv_esesdetektalas.md
2. C:\uni_stuff\anti_thesis\szakdolgozati_kutatasi_terv_esesdetektalas.docx
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from fall_report_part1 import PART1_MD
from fall_report_part2 import PART2_MD
from fall_report_part3 import PART3_MD
from fall_report_part4 import PART4_MD

OUTPUT_DIR = r"C:\uni_stuff\anti_thesis"
SCRATCH_DIR = r"C:\Users\bbger\.gemini\antigravity\scratch"
MD_PATH = os.path.join(OUTPUT_DIR, "szakdolgozati_kutatasi_terv_esesdetektalas.md")
DOCX_SCRATCH = os.path.join(SCRATCH_DIR, "szakdolgozati_kutatasi_terv_esesdetektalas.docx")

# 1. Összefűzés
FULL_MD = PART1_MD + "\n\n" + PART2_MD + "\n\n" + PART3_MD + "\n\n" + PART4_MD

print("1. Markdown fájl mentése...")
with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(FULL_MD)

word_count = len(FULL_MD.split())
char_count = len(FULL_MD)
line_count = len(FULL_MD.splitlines())
print(f"   [OK] Mentve: {MD_PATH}")
print(f"   Sorok: {line_count}, Szavak: {word_count}, Karakterek: {char_count}")
print(f"   Becsült oldalszám (A4, 1.15 sorköz, táblázatokkal): ~{word_count // 380} - {word_count // 340} oldal")

# 2. DOCX Dokumentum generálása
print("\n2. DOCX generálás indítása...")
doc = docx.Document()

# Oldalbeállítás: A4, 2.5 cm margók
section = doc.sections[0]
section.page_width = Inches(8.27)
section.page_height = Inches(11.69)
section.top_margin = Inches(0.98)
section.bottom_margin = Inches(0.98)
section.left_margin = Inches(0.98)
section.right_margin = Inches(0.98)

# Betűtípus és stílusok
styles = doc.styles
normal_style = styles['Normal']
normal_style.font.name = 'Calibri'
normal_style.font.size = Pt(11)
normal_style.font.color.rgb = RGBColor(45, 55, 72)
normal_style.paragraph_format.line_spacing = 1.15
normal_style.paragraph_format.space_after = Pt(4)
normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

COLOR_PRIMARY = RGBColor(27, 54, 93)     # #1B365D - Navy Blue
COLOR_SECONDARY = RGBColor(43, 108, 176) # #2B6CB0 - Slate Blue
COLOR_DARK = RGBColor(45, 55, 72)        # #2D3748 - Dark Charcoal
COLOR_MUTED = RGBColor(113, 128, 150)    # #718096 - Muted Gray

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

# ----------------- CÍMLAP -----------------
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(36)
title_p.paragraph_format.space_after = Pt(6)
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_inst = title_p.add_run("EÖTVÖS LORÁND TUDOMÁNYEGYETEM / BUDAPESTI MŰSZAKI ÉS GAZDASÁGTUDOMÁNYI EGYETEM\nSZÁMÍTÁSTUDOMÁNYI ÉS INFORMÁCIÓS RENDSZEREK TANSZÉK")
run_inst.font.name = 'Calibri'
run_inst.font.size = Pt(11)
run_inst.font.bold = True
run_inst.font.color.rgb = COLOR_MUTED

line_p = doc.add_paragraph()
line_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
line_p.paragraph_format.space_after = Pt(40)
run_line = line_p.add_run("—" * 35)
run_line.font.color.rgb = COLOR_SECONDARY

main_title_p = doc.add_paragraph()
main_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
main_title_p.paragraph_format.space_after = Pt(12)
run_main = main_title_p.add_run("SZAKDOLGOZATI KUTATÁSI ÉS RENDSZER-MEGVALÓSÍTÁSI TERV")
run_main.font.name = 'Calibri'
run_main.font.size = Pt(21)
run_main.font.bold = True
run_main.font.color.rgb = COLOR_PRIMARY

sub_title_p = doc.add_paragraph()
sub_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_title_p.paragraph_format.space_after = Pt(8)
run_sub = sub_title_p.add_run("Beágyazott és peremhálózati (Edge AI) valós idejű esésdetektálás Raspberry Pi mikroszámítógépen emberi pózbecsléssel és tér-időbeli gráfkonvolúciós hálózatokkal (YOLOv8-Pose, ST-GCN, ONNX INT8)")
run_sub.font.name = 'Calibri'
run_sub.font.size = Pt(12.5)
run_sub.font.bold = True
run_sub.font.color.rgb = COLOR_SECONDARY

en_title_p = doc.add_paragraph()
en_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
en_title_p.paragraph_format.space_after = Pt(45)
run_en = en_title_p.add_run("Embedded Edge AI Real-Time Fall Detection on Raspberry Pi using Human Pose Estimation and Spatial Temporal Graph Convolutional Networks (YOLOv8-Pose, ST-GCN, ONNX INT8)")
run_en.font.name = 'Calibri'
run_en.font.size = Pt(10.5)
run_en.font.italic = True
run_en.font.color.rgb = COLOR_MUTED

meta_table = doc.add_table(rows=5, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Készítette / Szerző:", "Szakdolgozó Hallgató (BSc Mérnökinformatikus)"),
    ("Hivatalos témakiírás:", "Gráf alapú modellek detektálása vizuális információn, különös tekintettel a viselkedéselemzésre"),
    ("Belső konzulens:", "Egyetemi Adjunktus / Tanszéki Oktató"),
    ("Külső konzulens:", "Számítógépes Látás és Beágyazott Rendszerek Szakértő"),
    ("Készítés ideje és tanév:", "2026/2027. tanév, Őszi félév (Szakdolgozat 1 / Diplomamunka 1)")
]
for row_idx, (label, val) in enumerate(meta_data):
    c0 = meta_table.cell(row_idx, 0)
    c1 = meta_table.cell(row_idx, 1)
    c0.width = Inches(2.5)
    c1.width = Inches(4.0)
    set_cell_margins(c0, top=50, bottom=50, left=80, right=80)
    set_cell_margins(c1, top=50, bottom=50, left=80, right=80)
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r0 = p0.add_run(label)
    r0.font.bold = True
    r0.font.size = Pt(10)
    r0.font.color.rgb = COLOR_PRIMARY
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p1.add_run(val)
    r1.font.size = Pt(10)
    r1.font.color.rgb = COLOR_DARK

doc.add_page_break()

# Fejléc és Lábléc
header = section.header
header_p = header.paragraphs[0]
header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
header_run = header_p.add_run("Szakdolgozati Részletes Kutatási Terv | Beágyazott Esésdetektálás (Raspberry Pi + ST-GCN)")
header_run.font.name = 'Calibri'
header_run.font.size = Pt(8.5)
header_run.font.color.rgb = COLOR_MUTED

footer = section.footer
footer_p = footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
foot_left = footer_p.add_run("BSc Szakdolgozati Részletes Terv — Tanszéki Beszámoló")
foot_left.font.name = 'Calibri'
foot_left.font.size = Pt(8.5)
foot_left.font.color.rgb = COLOR_MUTED

def add_formatted_runs(paragraph, text, base_font_size=Pt(11), base_color=COLOR_DARK):
    parts = re.split(r'(\*\*.*?\*\*|`.*?`|\*.*?\*)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
            run.font.name = 'Calibri'
            run.font.size = base_font_size
            run.font.color.rgb = base_color
        elif part.startswith('*') and part.endswith('*'):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
            run.font.name = 'Calibri'
            run.font.size = base_font_size
            run.font.color.rgb = base_color
        elif part.startswith('`') and part.endswith('`'):
            run = paragraph.add_run(part[1:-1])
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(160, 40, 40)
        else:
            run = paragraph.add_run(part)
            run.font.name = 'Calibri'
            run.font.size = base_font_size
            run.font.color.rgb = base_color

lines = FULL_MD.split('\n')
i = 0
in_code = False
code_lines = []

while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Kódblokk kezelés
    if stripped.startswith('```'):
        if not in_code:
            in_code = True
            code_lines = []
            i += 1
            continue
        else:
            in_code = False
            tbl = doc.add_table(rows=1, cols=1)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = tbl.cell(0, 0)
            set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            code_text = "\n".join(code_lines)
            run_c = p.add_run(code_text)
            run_c.font.name = 'Consolas'
            run_c.font.size = Pt(8.5)
            run_c.font.color.rgb = RGBColor(30, 41, 59)
            sp_p = doc.add_paragraph()
            sp_p.paragraph_format.space_after = Pt(4)
            i += 1
            continue

    if in_code:
        code_lines.append(line)
        i += 1
        continue

    if not stripped:
        i += 1
        continue

    # Elválasztó vonal
    if stripped in ['---', '***', '___']:
        div_p = doc.add_paragraph()
        div_p.paragraph_format.space_before = Pt(6)
        div_p.paragraph_format.space_after = Pt(6)
        r_div = div_p.add_run("—" * 55)
        r_div.font.color.rgb = RGBColor(226, 232, 240)
        i += 1
        continue

    # Táblázat feldolgozás
    if stripped.startswith('|') and stripped.endswith('|'):
        table_rows = []
        while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
            row_content = lines[i].strip()
            if re.match(r'^\|[\s\:\-\|]+$', row_content):
                i += 1
                continue
            cols = [c.strip() for c in row_content.split('|')[1:-1]]
            table_rows.append(cols)
            i += 1

        if table_rows:
            num_cols = max(len(r) for r in table_rows)
            tbl = doc.add_table(rows=len(table_rows), cols=num_cols)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            for r_idx, row in enumerate(table_rows):
                for c_idx in range(num_cols):
                    cell = tbl.cell(r_idx, c_idx)
                    val = row[c_idx] if c_idx < len(row) else ""
                    val = val.replace('<br>', '\n').replace('<br/>', '\n')
                    set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    if r_idx == 0:
                        set_cell_background(cell, "1B365D")
                        r = p.add_run(val)
                        r.font.bold = True
                        r.font.size = Pt(9.5)
                        r.font.color.rgb = RGBColor(255, 255, 255)
                    else:
                        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
                        set_cell_background(cell, bg)
                        add_formatted_runs(p, val, base_font_size=Pt(9.5), base_color=COLOR_DARK)
            sp_p = doc.add_paragraph()
            sp_p.paragraph_format.space_after = Pt(6)
        continue

    # Címsorok
    if stripped.startswith('# '):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(stripped[2:])
        r.font.name = 'Calibri'
        r.font.size = Pt(18)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        i += 1
        continue

    if stripped.startswith('## '):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(stripped[3:])
        r.font.name = 'Calibri'
        r.font.size = Pt(14.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_SECONDARY
        i += 1
        continue

    if stripped.startswith('### '):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(stripped[4:])
        r.font.name = 'Calibri'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = COLOR_PRIMARY
        i += 1
        continue

    if stripped.startswith('#### '):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(stripped[5:])
        r.font.name = 'Calibri'
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = COLOR_SECONDARY
        i += 1
        continue

    # Felsorolás
    if stripped.startswith('* ') or stripped.startswith('- '):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        add_formatted_runs(p, stripped[2:])
        i += 1
        continue

    match_num = re.match(r'^(\d+)\.\s+(.*)$', stripped)
    if match_num:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        num_str, rest = match_num.groups()
        r_num = p.add_run(f"{num_str}. ")
        r_num.font.bold = True
        r_num.font.color.rgb = COLOR_PRIMARY
        add_formatted_runs(p, rest)
        i += 1
        continue

    # Normál bekezdés
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    add_formatted_runs(p, stripped)
    i += 1

doc.save(DOCX_SCRATCH)
print(f"   [OK] DOCX sikeresen elkészült a scratch mappában: {DOCX_SCRATCH}")
