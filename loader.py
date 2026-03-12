# loader.py - Reads all PDFs and extracts text page by page

import fitz  # PyMuPDF - for reading PDFs
import os    # for working with files and folders


def load_pdfs(data_folder):
    """
    Reads all PDFs from a folder.
    Returns list of dicts with text, page number and source filename.
    """

    documents = []  # will store all pages from all PDFs

    all_files = os.listdir(data_folder)  # get all files in folder
    print(f" Found {len(all_files)} files in '{data_folder}'\n")

    for filename in all_files:

        # skip non-PDF files
        if not filename.endswith(".pdf"):
            continue

        # build full path e.g. "data/constitution.pdf"
        filepath = os.path.join(data_folder, filename)
        print(f"📄 Loading: {filename}")

        pdf = fitz.open(filepath)  # open the PDF

        for page_index in range(len(pdf)):
            page = pdf[page_index]
            text = page.get_text()  # extract text from page

            # skip empty pages
            if not text.strip():
                continue

            # store page text with its source info
            documents.append({
                "text"  : " ".join(text.split()),  # clean whitespace
                "page"  : page_index + 1,           # human readable page number
                "source": filename
            })

        pdf.close()
        print(f"   ✅ Done\n")

    print(f"✅ Total pages loaded: {len(documents)}")
    return documents


if __name__ == "__main__":
    docs = load_pdfs("data")

    # print sample of first loaded page
    print(f"\n--- Sample ---")
    print(f"Source : {docs[0]['source']}")
    print(f"Page   : {docs[0]['page']}")
    print(f"Text   : {docs[0]['text'][:300]}")
