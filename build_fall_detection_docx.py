# -*- coding: utf-8 -*-
r"""
Szakdolgozati Terv DOCX Generátor (Esésdetektálás Téma)
Bemenet: C:\uni_stuff\anti_thesis\szakdolgozati_kutatasi_terv_esesdetektalas.md
Kimenet: C:\uni_stuff\anti_thesis\szakdolgozati_kutatasi_terv_esesdetektalas.docx
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

MD_PATH = r"C:\uni_stuff\anti_thesis\szakdolgozati_kutatasi_terv_esesdetektalas.md"
DOCX_PATH = r"C:\Users\bbger\.gemini\antigravity\scratch\szakdolgozati_kutatasi_terv_esesdetektalas.docx"

with open(MD_PATH, "r", encoding="utf-8") as f:
    full_md = f.read()

doc = docx.Document()

# Page Setup: A4, 2.5 cm margins
section = doc.sections[0]
section.page_width = Inches(8.27)
section.page_height = Inches(11.69)
section.top_margin = Inches(0.98)
section.bottom_margin = Inches(0.98)
section.left_margin = Inches(0.98)
section.right_margin = Inches(0.98)

# Styles setup
styles = doc.styles
normal_style = styles['Normal']
normal_style.font.name = 'Calibri'
normal_style.font.size = Pt(11)
normal_style.font.color.rgb = RGBColor(45, 55, 72)
normal_style.paragraph_format.line_spacing = 1.15
normal_style.paragraph_format.space_after = Pt(4)
normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# Colors
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

# ----------------- COVER PAGE -----------------
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(40)
title_p.paragraph_format.space_after = Pt(6)
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_inst = title_p.add_run("EÖTVÖS LORÁND TUDOMÁNYEGYETEM / BUDAPESTI MŰSZAKI ÉS GAZDASÁGTUDOMÁNYI EGYETEM\nSZÁMÍTÁSTUDOMÁNYI ÉS INFORMÁCIÓS RENDSZEREK TANSZÉK")
run_inst.font.name = 'Calibri'
run_inst.font.size = Pt(11)
run_inst.font.bold = True
run_inst.font.color.rgb = COLOR_MUTED

line_p = doc.add_paragraph()
line_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
line_p.paragraph_format.space_after = Pt(45)
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
run_sub = sub_title_p.add_run("Valós idejű esésdetektálás és kritikus mozgáselemzés emberi pózbecsléssel és tér-időbeli gráfkonvolúciós hálózatokkal (YOLOv8-Pose, ST-GCN, PyTorch)")
run_sub.font.name = 'Calibri'
run_sub.font.size = Pt(13)
run_sub.font.bold = True
run_sub.font.color.rgb = COLOR_SECONDARY

en_title_p = doc.add_paragraph()
en_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
en_title_p.paragraph_format.space_after = Pt(50)
run_en = en_title_p.add_run("Graph-Based Models on Visual Information for Behavior Analysis: Real-Time Fall Detection via ST-GCN")
run_en.font.name = 'Calibri'
run_en.font.size = Pt(11)
run_en.font.italic = True
run_en.font.color.rgb = COLOR_MUTED

meta_table = doc.add_table(rows=4, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Készítette / Szerző:", "Szakdolgozó Hallgató (BSc Mérnökinformatikus)"),
    ("Hivatalos témakiírás:", "Gráf alapú modellek detektálása vizuális információn"),
    ("Konzulens / Témavezető:", "Tanszéki Oktató / Szakértő"),
    ("Készítés tanéve és féléve:", "2026/2027. tanév, Őszi félév (Szakdolgozat 1)")
]
for row_idx, (label, val) in enumerate(meta_data):
    c0 = meta_table.cell(row_idx, 0)
    c1 = meta_table.cell(row_idx, 1)
    c0.width = Inches(2.5)
    c1.width = Inches(4.0)
    set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
    set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r0 = p0.add_run(label)
    r0.font.bold = True
    r0.font.size = Pt(10.5)
    r0.font.color.rgb = COLOR_PRIMARY
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p1.add_run(val)
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = COLOR_DARK

doc.add_page_break()

# Setup Header and Footer
header = section.header
header_p = header.paragraphs[0]
header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
header_run = header_p.add_run("Szakdolgozati Kutatási Terv | Váz-alapú esésdetektálás (YOLOv8-Pose + ST-GCN)")
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

lines = full_md.split('\n')
i = 0
in_code = False
code_lines = []

while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # Code block handling
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
            run_c.font.size = Pt(9)
            run_c.font.color.rgb = RGBColor(30, 41, 59)
            sp_p = doc.add_paragraph()
            sp_p.paragraph_format.space_after = Pt(4)
            i += 1
            continue

    if in_code:
        code_lines.append(line)
        i += 1
        continue

    # Skip empty lines
    if not stripped:
        i += 1
        continue

    # Divider line
    if stripped in ['---', '***', '___']:
        div_p = doc.add_paragraph()
        div_p.paragraph_format.space_before = Pt(6)
        div_p.paragraph_format.space_after = Pt(6)
        r_div = div_p.add_run("—" * 55)
        r_div.font.color.rgb = RGBColor(226, 232, 240)
        i += 1
        continue

    # Markdown Table detection
    if stripped.startswith('|') and stripped.endswith('|'):
        table_rows = []
        while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
            row_content = lines[i].strip()
            # check if separator row
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
                    set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
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

    # Headings
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
        r.font.size = Pt(15)
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
        r.font.size = Pt(12.5)
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
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_SECONDARY
        i += 1
        continue

    # Bullet / numbered list
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

    # Regular Paragraph
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    add_formatted_runs(p, stripped)
    i += 1

doc.save(DOCX_PATH)
print(f"[OK] Szakdolgozati Terv Sikeresen Létrehozva:")
print(f"     DOCX: {DOCX_PATH}")
