# chunker.py - Splits long page texts into smaller overlapping chunks

def chunk_documents(documents, chunk_size=500, overlap=50):
    """
    Takes our loaded pages and splits them into smaller chunks.
    
    Why? Pages are too long for the AI to process efficiently.
    Smaller chunks = better search results.
    
    chunk_size : max number of characters per chunk
    overlap    : how many characters to repeat between chunks
                 (so we don't lose context at boundaries)
    """

    all_chunks = []  # will store all chunks from all pages

    for doc in documents:
        text   = doc["text"]
        page   = doc["page"]
        source = doc["source"]

        # split text into chunks with overlap
        start = 0
        while start < len(text):
            end = start + chunk_size  # end of this chunk

            # extract the chunk
            chunk_text = text[start:end]

            all_chunks.append({
                "text"  : chunk_text,
                "page"  : page,
                "source": source
            })

            # move start forward but overlap a little
            start += chunk_size - overlap

    return all_chunks


if __name__ == "__main__":
    # import loader to test with real data
    from loader import load_pdfs

    docs   = load_pdfs("data")
    chunks = chunk_documents(docs)

    print(f"📄 Total pages  : {len(docs)}")
    print(f"🧩 Total chunks : {len(chunks)}")
    print(f"\n--- Sample Chunk ---")
    print(f"Source : {chunks[0]['source']}")
    print(f"Page   : {chunks[0]['page']}")
    print(f"Text   : {chunks[0]['text'][:300]}")