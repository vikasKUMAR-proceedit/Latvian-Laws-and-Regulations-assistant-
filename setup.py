# setup.py - builds ChromaDB on first startup

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from loader import load_pdfs
from chunker import chunk_documents
from embedder import embed_and_store

DB_FOLDER   = "db"
DATA_FOLDER = "."

def setup():
    if os.path.exists(DB_FOLDER) and len(os.listdir(DB_FOLDER)) > 0:
        print("✅ DB already exists, skipping setup")
        return

    print("🔨 Building ChromaDB from PDFs...")
    docs   = load_pdfs(DATA_FOLDER)
    chunks = chunk_documents(docs)
    embed_and_store(chunks)

    print("✅ DB ready!")

