# embedder.py - Embeds chunks into vectors and stores in ChromaDB

import sys
import os

sys.path.append(os.path.dirname(__file__))

from sentence_transformers import SentenceTransformer
import chromadb
from loader import load_pdfs
from chunker import chunk_documents

DATA_FOLDER = r"D:\Rag_project\data"
DB_FOLDER   = r"D:\Rag_project\db"

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_and_store(chunks):
    client = chromadb.PersistentClient(path=DB_FOLDER)

    # delete collection if exists then recreate
    existing = [c.name for c in client.list_collections()]
    if "latvian_laws" in existing:
        client.delete_collection("latvian_laws")

    collection = client.create_collection("latvian_laws")

    print(f"🔢 Embedding {len(chunks)} chunks...")
    print("   (This may take a minute...)\n")

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


if __name__ == "__main__":
    docs       = load_pdfs(DATA_FOLDER)  # pass data folder directly
    chunks     = chunk_documents(docs)
    collection = embed_and_store(chunks)

    print(f"📊 Total vectors in DB: {collection.count()}")