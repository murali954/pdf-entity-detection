import fitz  # PyMuPDF
import json
import os
import re

# Input PDF
pdf_path = r"C:\Users\user\Downloads\assignment\Workbook.pdf"
doc = fitz.open(pdf_path)

# Create output folders
os.makedirs("output/text", exist_ok=True)
os.makedirs("output/tables", exist_ok=True)
os.makedirs("output/images", exist_ok=True)

metadata = []

def is_table_like(text):
    """Heuristic: detect if block looks like a table"""
    keywords = ["table", "row", "column", "sacks", "ft3", "yield"]
    return any(word in text.lower() for word in keywords) or bool(re.search(r"\d+\s+\d+", text))

for page_num, page in enumerate(doc, start=1):
    page_height = page.rect.height

    # Extract text blocks
    blocks = page.get_text("blocks")
    for i, b in enumerate(blocks, start=1):
        x0, y0, x1, y1, text, *_ = b
        clean_text = text.strip()
        if not clean_text:
            continue

        block_id = f"page{page_num}_block{i}"
        bbox = [x0, y0, x1, y1]

        if is_table_like(clean_text):
            # Save as CSV-like text (assignment style)
            file_path = f"output/tables/{block_id}.csv"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(clean_text.replace(" ", ","))
            label = "Table"
        else:
            # Save as text
            file_path = f"output/text/{block_id}.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(clean_text)
            label = "Text"

        metadata.append({
            "id": block_id,
            "page": page_num,
            "label": label,
            "bbox": bbox,
            "file_path": file_path
        })

    # Extract images (figures/charts)
    for j, img in enumerate(page.get_images(full=True), start=1):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        block_id = f"page{page_num}_image{j}"
        file_path = f"output/images/{block_id}.png"

        if pix.n - pix.alpha < 4:  # RGB or Gray
            pix.save(file_path)
        else:  # CMYK
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.save(file_path)
            pix1 = None
        pix = None

        metadata.append({
            "id": block_id,
            "page": page_num,
            "label": "Figure",
            "file_path": file_path
        })

# Save metadata JSON
with open("output/metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4)

print("✅ Entities stored successfully! Check 'output/' folder.")
