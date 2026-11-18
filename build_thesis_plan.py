# -*- coding: utf-8 -*-
r"""
Full Builder script for Thesis Research & Implementation Plan
Reads PART1_MD, PART2_MD, PART3_MD, PART4_MD
Generates:
1. C:\uni_stuff\anti_thesis\szakdolgozati_kutatasi_es_megvalositasi_terv.md
2. C:\uni_stuff\anti_thesis\szakdolgozati_kutatasi_es_megvalositasi_terv.docx
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from plan_text_part1 import PART1_MD
from plan_text_part2 import PART2_MD
from plan_text_part3 import PART3_MD
from plan_text_part4 import PART4_MD

OUTPUT_DIR = r"C:\uni_stuff\anti_thesis"
MD_PATH = os.path.join(OUTPUT_DIR, "szakdolgozati_kutatasi_es_megvalositasi_terv.md")
DOCX_PATH = os.path.join(OUTPUT_DIR, "szakdolgozati_kutatasi_es_megvalositasi_terv.docx")

# Combine all Markdown content
FULL_MD = PART1_MD + "\n\n" + PART2_MD + "\n\n" + PART3_MD + "\n\n" + PART4_MD

print("Writing Markdown file...")
with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(FULL_MD)

print(f"Markdown file saved: {MD_PATH}")
word_count = len(FULL_MD.split())
char_count = len(FULL_MD)
print(f"Total Words: {word_count}, Total Characters: {char_count}")

# Now build the DOCX document
doc = docx.Document()

# Page Setup: A4, 2.5 cm margins
section = doc.sections[0]
section.page_width = Inches(8.27)   # A4
section.page_height = Inches(11.69) # A4
section.top_margin = Inches(0.98)   # 2.5 cm
section.bottom_margin = Inches(0.98)
section.left_margin = Inches(0.98)
section.right_margin = Inches(0.98)

# Styles setup
styles = doc.styles
normal_style = styles['Normal']
normal_style.font.name = 'Calibri'
normal_style.font.size = Pt(11)
normal_style.font.color.rgb = RGBColor(45, 55, 72) # #2D3748
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

print("Setting up cover page...")

# ----------------- COVER PAGE -----------------
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(40)
title_p.paragraph_format.space_after = Pt(6)
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_inst = title_p.add_run("EÖTVÖS LORÁND TUDOMÁNYEGYETEM / BUDAPESTI MŰSZAKI ÉS GAZDASÁGTUDOMÁNYI EGYETEM\nINFORMATIKAI KAR / VILLAMOSMÉRNÖKI ÉS INFORMATIKAI KAR\nSZÁMÍTÁSTUDOMÁNYI ÉS INFORMÁCIÓS RENDSZEREK TANSZÉK")
run_inst.font.name = 'Calibri'
run_inst.font.size = Pt(11)
run_inst.font.bold = True
run_inst.font.color.rgb = COLOR_MUTED

# Decorative line
line_p = doc.add_paragraph()
line_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
line_p.paragraph_format.space_after = Pt(50)
run_line = line_p.add_run("—" * 35)
run_line.font.color.rgb = COLOR_SECONDARY

# Main Title
main_title_p = doc.add_paragraph()
main_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
main_title_p.paragraph_format.space_after = Pt(12)
run_main = main_title_p.add_run("SZAKDOLGOZATI KUTATÁSI ÉS RENDSZER-MEGVALÓSÍTÁSI TERV")
run_main.font.name = 'Calibri'
run_main.font.size = Pt(22)
run_main.font.bold = True
run_main.font.color.rgb = COLOR_PRIMARY

# Subtitle
sub_title_p = doc.add_paragraph()
sub_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_title_p.paragraph_format.space_after = Pt(8)
run_sub = sub_title_p.add_run("Verekedés- és agresszió-megelőzés szórakozóhelyi környezetben váz-alapú viselkedéselemzéssel (YOLOv8-Pose, ST-GCN, PyTorch)")
run_sub.font.name = 'Calibri'
run_sub.font.size = Pt(13)
run_sub.font.bold = True
run_sub.font.color.rgb = COLOR_SECONDARY

# English Title
en_title_p = doc.add_paragraph()
en_title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
en_title_p.paragraph_format.space_after = Pt(50)
run_en = en_title_p.add_run("Nightclub Violence Detection and Prevention via Skeleton-Based Human Action Recognition")
run_en.font.name = 'Calibri'
run_en.font.size = Pt(11)
run_en.font.italic = True
run_en.font.color.rgb = COLOR_MUTED

# Author & Metadata Box
meta_table = doc.add_table(rows=4, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Készítette / Szerző:", "Szakdolgozó Hallgató (BSc Mérnökinformatikus)"),
    ("Témavezető:", "Egyetemi Adjunktus / Kutató"),
    ("Konzulens:", "Biztonságtechnikai és Számítógépes Látás Szakértő"),
    ("Készítés ideje és tanév:", "2026/2027. tanév, Őszi félév")
]
for row_idx, (label, val) in enumerate(meta_data):
    c0 = meta_table.cell(row_idx, 0)
    c1 = meta_table.cell(row_idx, 1)
    c0.width = Inches(2.5)
    c1.width = Inches(3.8)
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

# Setup Header and Footer for subsequent pages
body_section = doc.sections[0]
header = body_section.header
header_p = header.paragraphs[0]
header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
header_run = header_p.add_run("Szakdolgozati Kutatási Terv | Váz-alapú agresszió-megelőzés (YOLOv8-Pose + ST-GCN)")
header_run.font.name = 'Calibri'
header_run.font.size = Pt(8.5)
header_run.font.color.rgb = COLOR_MUTED

footer = body_section.footer
footer_p = footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
foot_left = footer_p.add_run("BSc Szakdolgozati Terv — Bizalmas Kutatási Dokumentum")
foot_left.font.name = 'Calibri'
foot_left.font.size = Pt(8.5)
foot_left.font.color.rgb = COLOR_MUTED

print("Cover page generated. Parsing sections into document...")

# Helper to add inline bold/italic
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

# Process full Markdown lines
lines = FULL_MD.split('\n')
i = 0
table_lines = []
in_code = False
code_lines = []
code_lang = ""

while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Handle Code Blocks
    if stripped.startswith('```'):
        if not in_code:
            in_code = True
            code_lang = stripped[3:].strip()
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
        
    # Handle Markdown Tables
    if stripped.startswith('|') and stripped.endswith('|'):
        table_lines.append(stripped)
        i += 1
        continue
    else:
        if table_lines:
            data_rows = []
            for t_line in table_lines:
                cells = [c.strip() for c in t_line.strip('|').split('|')]
                if all(re.match(r'^:?-+:?$', c) for c in cells):
                    continue
                data_rows.append(cells)
                
            if data_rows:
                num_cols = max(len(r) for r in data_rows)
                docx_table = doc.add_table(rows=len(data_rows), cols=num_cols)
                docx_table.alignment = WD_TABLE_ALIGNMENT.CENTER
                
                for r_idx, r_data in enumerate(data_rows):
                    is_header = (r_idx == 0)
                    for c_idx in range(num_cols):
                        cell = docx_table.cell(r_idx, c_idx)
                        c_text = r_data[c_idx] if c_idx < len(r_data) else ""
                        
                        if is_header:
                            set_cell_background(cell, "1B365D")
                            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
                            p = cell.paragraphs[0]
                            p.paragraph_format.space_before = Pt(0)
                            p.paragraph_format.space_after = Pt(0)
                            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                            run = p.add_run(c_text)
                            run.bold = True
                            run.font.name = 'Calibri'
                            run.font.size = Pt(10)
                            run.font.color.rgb = RGBColor(255, 255, 255)
                        else:
                            bg_color = "F8FAFC" if (r_idx % 2 == 1) else "FFFFFF"
                            set_cell_background(cell, bg_color)
                            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
                            p = cell.paragraphs[0]
                            p.paragraph_format.space_before = Pt(0)
                            p.paragraph_format.space_after = Pt(0)
                            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                            add_formatted_runs(p, c_text, base_font_size=Pt(9.5))
                            
                tblPr = docx_table._tbl.tblPr
                borders = parse_xml(f'''
                    <w:tblBorders {nsdecls("w")}>
                        <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/>
                        <w:left w:val="none"/>
                        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/>
                        <w:right w:val="none"/>
                        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                        <w:insideV w:val="none"/>
                    </w:tblBorders>
                ''')
                tblPr.append(borders)
                
                sp_p = doc.add_paragraph()
                sp_p.paragraph_format.space_after = Pt(6)
                
            table_lines = []
            
    if not stripped:
        i += 1
        continue
        
    if stripped.startswith('# '):
        i += 1
        continue
        
    if stripped.startswith('## '):
        heading_text = stripped[3:].strip()
        h_p = doc.add_paragraph()
        h_p.paragraph_format.space_before = Pt(18)
        h_p.paragraph_format.space_after = Pt(6)
        h_p.paragraph_format.keep_with_next = True
        run = h_p.add_run(heading_text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(16)
        run.font.color.rgb = COLOR_PRIMARY
        i += 1
        continue
        
    if stripped.startswith('### '):
        heading_text = stripped[4:].strip()
        h_p = doc.add_paragraph()
        h_p.paragraph_format.space_before = Pt(12)
        h_p.paragraph_format.space_after = Pt(4)
        h_p.paragraph_format.keep_with_next = True
        run = h_p.add_run(heading_text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(13)
        run.font.color.rgb = COLOR_SECONDARY
        i += 1
        continue
        
    if stripped.startswith('#### '):
        heading_text = stripped[5:].strip()
        h_p = doc.add_paragraph()
        h_p.paragraph_format.space_before = Pt(8)
        h_p.paragraph_format.space_after = Pt(2)
        h_p.paragraph_format.keep_with_next = True
        run = h_p.add_run(heading_text)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(11.5)
        run.font.color.rgb = COLOR_DARK
        i += 1
        continue
        
    if stripped == '---':
        h_p = doc.add_paragraph()
        h_p.paragraph_format.space_before = Pt(6)
        h_p.paragraph_format.space_after = Pt(6)
        h_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = h_p.add_run("—" * 25)
        r.font.color.rgb = COLOR_MUTED
        i += 1
        continue
        
    if stripped.startswith('* ') or stripped.startswith('- '):
        item_text = stripped[2:].strip()
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(1)
        bp.paragraph_format.space_after = Pt(2)
        bp.paragraph_format.line_spacing = 1.15
        add_formatted_runs(bp, item_text)
        i += 1
        continue
        
    num_match = re.match(r'^(\d+)\.\s+(.*)$', stripped)
    if num_match:
        item_text = num_match.group(2).strip()
        np_para = doc.add_paragraph(style='List Number')
        np_para.paragraph_format.space_before = Pt(1)
        np_para.paragraph_format.space_after = Pt(2)
        np_para.paragraph_format.line_spacing = 1.15
        add_formatted_runs(np_para, item_text)
        i += 1
        continue
        
    para = doc.add_paragraph()
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after = Pt(5)
    para.paragraph_format.line_spacing = 1.15
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    add_formatted_runs(para, stripped)
    i += 1

print("Saving docx file...")
doc.save(DOCX_PATH)
print(f"DOCX document successfully created: {DOCX_PATH}")
