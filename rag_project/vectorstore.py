# vectorstore.py
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize embeddings once
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vectorstore(docs, persist_path="faiss_index"):
    """
    Create a FAISS vectorstore from documents and save it locally.
    """
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(persist_path)
    return vectorstore

def load_vectorstore(persist_path="faiss_index"):
    """
    Load a FAISS vectorstore if it exists, otherwise return None.
    """
    if os.path.exists(persist_path):
        return FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)
    else:
        return None

def update_vectorstore(new_docs, persist_path="faiss_index"):
    """
    Incrementally update the FAISS index with new documents.
    If index exists, load and add new docs; otherwise create fresh index.
    """
    if os.path.exists(persist_path):
        vectorstore = FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)
        vectorstore.add_documents(new_docs)
        vectorstore.save_local(persist_path)
    else:
        vectorstore = FAISS.from_documents(new_docs, embeddings)
        vectorstore.save_local(persist_path)
    return vectorstore

