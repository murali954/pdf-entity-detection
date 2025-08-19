import fitz  # PyMuPDF
import json

def classify_block(x0, y0, x1, y1, text, page_height):
    text = text.strip()
    # Header if at the very top
    if y0 < 100:
        return "Header"
    # Footer if near bottom
    elif y1 > page_height - 100:
        return "Footer"
    # Short text in top quarter could be a Title
    elif len(text.split()) <= 6 and y0 < page_height * 0.25:
        return "Title"
    # If it has table-like keywords
    elif any(word in text.lower() for word in ["table", "row", "column", "sacks", "ft3", "yield"]):
        return "Table"
    else:
        return "Body"

doc = fitz.open(r"C:\Users\user\Downloads\assignment\Workbook.pdf")
output = []

for page_num, page in enumerate(doc, start=1):
    page_height = page.rect.height
    page_data = {"page": page_num, "blocks": []}

    # Text blocks
    blocks = page.get_text("blocks")
    for b in blocks:
        x0, y0, x1, y1, text, block_no, block_type = b
        label = classify_block(x0, y0, x1, y1, text, page_height)
        page_data["blocks"].append({
            "type": "text",
            "label": label,
            "bbox": [x0, y0, x1, y1],
            "content": text.strip()
        })

    # Images
    images = page.get_images(full=True)
    for img in images:
        xref = img[0]
        width, height = img[2], img[3]
        page_data["blocks"].append({
            "type": "image",
            "label": "Figure",
            "xref": xref,
            "size": [width, height]
        })

    output.append(page_data)

# Save JSON with classification
with open("classified_layout.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)
