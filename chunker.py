# chunker.py - Splits pages into smaller overlapping chunks

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from loader import load_pdfs

def chunk_documents(documents, chunk_size=500, overlap=50):
    all_chunks = []

    for doc in documents:
        text   = doc["text"]
        page   = doc["page"]
        source = doc["source"]

        start = 0
        while start < len(text):
            end        = start + chunk_size
            chunk_text = text[start:end]

            all_chunks.append({
                "text"  : chunk_text,
                "page"  : page,
                "source": source
            })

            start += chunk_size - overlap

    return all_chunks