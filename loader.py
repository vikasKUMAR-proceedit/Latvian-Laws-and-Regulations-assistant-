# loader.py - Reads all PDFs and extracts text page by page

import fitz
import os

DATA_FOLDER = "data"

def load_pdfs(data_folder=DATA_FOLDER):
    documents = []
    all_files = os.listdir(data_folder)
    print(f"📁 Found {len(all_files)} files in 'data'\n")

    for filename in all_files:
        if not filename.endswith(".pdf"):
            continue

        filepath = os.path.join(data_folder, filename)
        print(f"📄 Loading: {filename}")

        pdf = fitz.open(filepath)

        for page_index in range(len(pdf)):
            page = pdf[page_index]
            text = page.get_text()

            if not text.strip():
                continue

            documents.append({
                "text"  : " ".join(text.split()),
                "page"  : page_index + 1,
                "source": filename
            })

        pdf.close()
        print(f"   ✅ Done\n")

    print(f"✅ Total pages loaded: {len(documents)}")
    return documents