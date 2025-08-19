import streamlit as st
import json
import os

# Load metadata
with open("output/metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# --- Helper functions ---
def get_entities(label=None, page=None):
    results = []
    for block in metadata:
        if (label is None or block["label"].lower() == label.lower()) and \
           (page is None or block["page"] == page):
            results.append(block)
    return results

def search_text(keyword):
    results = []
    for block in metadata:
        if block["label"].lower() == "text":
            try:
                with open(block["file_path"], "r", encoding="utf-8") as f:
                    content = f.read()
                if keyword.lower() in content.lower():
                    snippet = content[:200].replace("\n", " ") + "..."
                    results.append({
                        "page": block["page"],
                        "file": block["file_path"],
                        "snippet": snippet
                    })
            except:
                continue
    return results

# --- Streamlit UI ---
st.set_page_config(page_title="PDF Entity Retrieval", layout="wide")
st.title("📄 PDF Entity Retrieval System")

query_type = st.sidebar.radio("Choose Query Type", ["By Entity", "Search Keyword"])

if query_type == "By Entity":
    label = st.selectbox("Select Entity Type", ["Table", "Figure", "Text", "Header", "Footer"])
    page = st.number_input("Page Number (optional)", min_value=1, value=1)
    if st.button("Retrieve"):
        results = get_entities(label=label, page=page if page else None)
        if results:
            st.success(f"Found {len(results)} {label}(s)")
            for r in results:
                st.write(f"📌 Page {r['page']} → {r['file_path']}")
                if label == "Text":
                    with open(r["file_path"], "r", encoding="utf-8") as f:
                        st.text(f.read()[:500] + "...")
                if label == "Figure":
                    st.image(r["file_path"])
        else:
            st.warning("No results found.")

elif query_type == "Search Keyword":
    keyword = st.text_input("Enter keyword")
    if st.button("Search"):
        results = search_text(keyword)
        if results:
            st.success(f"Found {len(results)} matches for '{keyword}'")
            for r in results:
                st.write(f"📌 Page {r['page']} → {r['file']}")
                st.text(r['snippet'])
        else:
            st.warning("No matches found.")
