# retriever.py - Searches ChromaDB for most relevant chunks

import sys
import os

sys.path.append(os.path.dirname(__file__))

from sentence_transformers import SentenceTransformer
import chromadb

DATA_FOLDER = r"D:\Rag_project\data"
DB_FOLDER   = r"D:\Rag_project\db"

# same model we used in embedder.py
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_retriever():
    # connect to our existing ChromaDB
    client     = chromadb.PersistentClient(path=DB_FOLDER)
    collection = client.get_collection("latvian_laws")
    return collection


def retrieve(question, top_k=5):
    """
    Takes a question, finds top_k most relevant chunks.
    
    top_k : how many chunks to return (5 is a good default)
    """

    collection = get_retriever()

    # convert question to vector
    question_vector = model.encode(question).tolist()

    # search ChromaDB for similar vectors
    results = collection.query(
        query_embeddings = [question_vector],
        n_results        = top_k
    )

    # format results nicely
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text"  : results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "page"  : results["metadatas"][0][i]["page"]
        })

    return chunks


if __name__ == "__main__":
    # test with a real question
    question = "What are the fundamental rights of citizens in Latvia?"

    print(f"❓ Question: {question}")
    print(f"🔍 Searching...\n")

    chunks = retrieve(question)

    print(f"📚 Top {len(chunks)} relevant chunks found:\n")
    for i, chunk in enumerate(chunks):
        print(f"--- Result {i+1} ---")
        print(f"📁 Source : {chunk['source']}")
        print(f"📄 Page   : {chunk['page']}")
        print(f"📝 Text   : {chunk['text'][:200]}")
        print()