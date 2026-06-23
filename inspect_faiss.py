# inspect_faiss.py
from vectorstore import load_vectorstore

def inspect_index():
    # Load the existing FAISS index
    vectorstore = load_vectorstore("faiss_index")
    if not vectorstore:
        print("No FAISS index found. Run main.py first to build it.")
        return

    # Show how many chunks are stored
    print("Total chunks stored:", len(vectorstore.index_to_docstore_id))

    # Preview a few chunks
    for i in range(min(5, len(vectorstore.index_to_docstore_id))):  # show up to 5
        doc_id = vectorstore.index_to_docstore_id[i]
        doc = vectorstore.docstore.search(doc_id)
        print(f"\nChunk {i+1}:")
        print(doc.page_content[:300])  # show first 300 characters of the chunk

if __name__ == "__main__":
    inspect_index()

