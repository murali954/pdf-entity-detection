# PDF Entity Detection & Retrieval System

This project was built as part of an internship assignment.  
The goal is to detect, recognize, store, and retrieve entities from digital PDFs such as **Headers, Footers, Tables, Figures, Charts, Equations, and Text**.  

---

## 📑 Workflow

### Step 1 – Detection (Layout Extraction)
- Extract bounding boxes for all PDF entities using **PyMuPDF**.
- Output: `layout.json`

### Step 2 – Recognition (Classification)
- Classify detected blocks into:
  - **Header**
  - **Footer**
  - **Title**
  - **Body**
  - **Table**
  - **Figure**
- Output: `classified_layout.json`

### Step 3 – Storage & Linking
- Store each entity separately:
  - **Text →** `.txt` files
  - **Tables →** `.csv` files
  - **Figures/Charts →** `.png` images
- Generate a `metadata.json` linking entities with:
  - Page number
  - Bounding box
  - Label
  - File path

### Step 4 – Retrieval & Querying
- Query metadata by:
  - Entity type (Table, Figure, Text, etc.)
  - Page number
  - Keyword search across text blocks
- Demonstrates efficient retrieval of stored entities.

### Step 5 – Visual Retrieval (Streamlit App)
- Browser interface for searching and retrieving entities.
- Features:
  - Retrieve entities by **type + page**
  - **Keyword search** across document
  - Preview text and figures

Run with:
```bash
streamlit run app.py
