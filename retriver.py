# retriver.py - Searches ChromaDB for most relevant chunks

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sentence_transformers import SentenceTransformer
import chromadb

DB_FOLDER = "db"

model = SentenceTransformer("all-MiniLM-L6-v2")


def get_retriever():
    client     = chromadb.PersistentClient(path=DB_FOLDER)
    collection = client.get_collection("latvian_laws")
    return collection


def retrieve(question, top_k=5):
    collection      = get_retriever()
    question_vector = model.encode(question).tolist()

    results = collection.query(
        query_embeddings = [question_vector],
        n_results        = top_k
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text"  : results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "page"  : results["metadatas"][0][i]["page"]
        })

    return chunks