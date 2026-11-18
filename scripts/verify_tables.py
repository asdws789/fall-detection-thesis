import docx
from docx.shared import Inches

doc = docx.Document(r'C:\uni_stuff\anti_thesis\docs\szakdolgozati_kutatasi_terv.docx')
MAX_W = 5.91  # usable inches

print(f'Tables: {len(doc.tables)}')
print(f'Paragraphs: {len(doc.paragraphs)}')
print()

overflow_count = 0
for i, table in enumerate(doc.tables):
    ncols = len(table.columns)
    total_w = 0
    for row in table.rows:
        row_w = sum(cell.width.inches if cell.width else 0 for cell in row.cells[:ncols])
        if row_w > 0:
            total_w = row_w
            break
    if total_w > MAX_W + 0.01:
        overflow_count += 1
        status = f'OVERFLOW +{total_w - MAX_W:.2f}"'
    elif total_w == 0:
        status = 'width=0 (auto)'
    else:
        status = 'OK'
    print(f'  T{i+1}: {ncols} cols, {len(table.rows)} rows, width={total_w:.2f}" [{status}]')

print()
if overflow_count == 0:
    print('All tables fit within page width!')
else:
    print(f'WARNING: {overflow_count} tables still overflow!')
