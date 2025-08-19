import json
import os

# Load metadata
with open("output/metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

def get_entities(label=None, page=None):
    """
    Retrieve entities from metadata by label or page.
    :param label: "Table", "Figure", "Text", etc. (optional)
    :param page: page number (optional)
    :return: list of matched entities
    """
    results = []
    for block in metadata:
        if (label is None or block["label"].lower() == label.lower()) and \
           (page is None or block["page"] == page):
            results.append(block)
    return results

def search_text(keyword):
    """
    Search all text blocks for a keyword.
    :param keyword: word to search
    :return: list of matches with page, path, snippet
    """
    results = []
    for block in metadata:
        if block["label"].lower() == "text":  # only search text blocks
            try:
                with open(block["file_path"], "r", encoding="utf-8") as f:
                    content = f.read()
                if keyword.lower() in content.lower():
                    snippet = content[:100].replace("\n", " ") + "..."
                    results.append({
                        "page": block["page"],
                        "file": block["file_path"],
                        "snippet": snippet
                    })
            except Exception as e:
                continue
    return results

# --- Example queries ---
print("\n📌 All Tables in the document:")
for block in get_entities(label="Table"):
    print(f" Page {block['page']} → {block['file_path']}")

print("\n📌 All Figures in Page 3:")
for block in get_entities(label="Figure", page=3):
    print(f" Page {block['page']} → {block['file_path']}")

print("\n📌 Search keyword: 'cement'")
matches = search_text("cement")
for m in matches:
    print(f" Page {m['page']} → {m['file']}")
    print(f"   Snippet: {m['snippet']}")
