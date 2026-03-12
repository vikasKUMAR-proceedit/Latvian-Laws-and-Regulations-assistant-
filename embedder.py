# embedder.py - Embeds chunks into vectors and stores in ChromaDB

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sentence_transformers import SentenceTransformer
import chromadb
from loader import load_pdfs
from chunker import chunk_documents

DB_FOLDER   = "db"
DATA_FOLDER = "data"

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_and_store(chunks):
    client = chromadb.PersistentClient(path=DB_FOLDER)

    existing = [c.name for c in client.list_collections()]
    if "latvian_laws" in existing:
        client.delete_collection("latvian_laws")

    collection = client.create_collection("latvian_laws")

    print(f"🔢 Embedding {len(chunks)} chunks...")

    texts     = [chunk["text"] for chunk in chunks]
    vectors   = model.encode(texts, show_progress_bar=True)
    ids       = [str(i) for i in range(len(chunks))]
    metadatas = [{"source": c["source"], "page": c["page"]} for c in chunks]

    collection.add(
        ids        = ids,
        documents  = texts,
        embeddings = vectors.tolist(),
        metadatas  = metadatas
    )

    print(f"\n✅ Stored {len(chunks)} chunks in ChromaDB!")
    return collection