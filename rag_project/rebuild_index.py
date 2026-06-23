# rebuild_index.py
import os
from loaders import load_documents
from vectorstore import create_vectorstore

def rebuild_index():
    data_path = "data/BSS_Safaricom"
    persist_path = "faiss_index"

    # Remove old index if exists
    if os.path.exists(persist_path):
        print("Deleting old FAISS index...")
        import shutil
        shutil.rmtree(persist_path)

    print("Loading documents from:", data_path)
    docs = load_documents(data_path)

    print("Creating new FAISS index...")
    vectorstore = create_vectorstore(docs, persist_path)

    print("Rebuild complete. Total chunks stored:", len(vectorstore.index_to_docstore_id))

if __name__ == "__main__":
    rebuild_index()

