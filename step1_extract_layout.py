import fitz  # PyMuPDF

# Open PDF
doc = fitz.open(r"C:\Users\user\Downloads\assignment\Workbook.pdf")

# Loop through pages
for page_num, page in enumerate(doc, start=1):
    print(f"\n--- Page {page_num} ---")

    # Extract text blocks
    blocks = page.get_text("blocks")
    for b in blocks:
        x0, y0, x1, y1, text, block_no, block_type = b
        print(f"Text Block: {text.strip()} | BBox: ({x0}, {y0}, {x1}, {y1})")

    # Extract images
    images = page.get_images(full=True)
    for img in images:
        xref = img[0]
        width, height = img[2], img[3]
        print(f"Image found with XREF={xref}, size=({width}x{height})")
import json

output = []

for page_num, page in enumerate(doc, start=1):
    page_data = {"page": page_num, "blocks": []}

    blocks = page.get_text("blocks")
    for b in blocks:
        x0, y0, x1, y1, text, block_no, block_type = b
        page_data["blocks"].append({
            "type": "text",
            "bbox": [x0, y0, x1, y1],
            "content": text.strip()
        })

    images = page.get_images(full=True)
    for img in images:
        xref = img[0]
        width, height = img[2], img[3]
        page_data["blocks"].append({
            "type": "image",
            "xref": xref,
            "size": [width, height]
        })

    output.append(page_data)

# Save all results to JSON
with open("layout.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

