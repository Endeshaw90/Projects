# vectorstore.py - FAISS Dense Vector Store

import os
import ssl
import urllib3
from pathlib import Path

# ---------------------------------------------------------
# SSL configuration for model downloads in WSL
# ---------------------------------------------------------

os.environ["HF_HUB_DISABLE_SSL_VERIFY"] = "1"
os.environ["PYTHONHTTPSVERIFY"] = "0"
os.environ["CURL_CA_BUNDLE"] = ""

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_INDEX_PATH = PROJECT_ROOT / "faiss_index"


# ---------------------------------------------------------
# Embedding model
# ---------------------------------------------------------

try:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"local_files_only": False}
    )
except Exception:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"local_files_only": True}
    )


# ---------------------------------------------------------
# Resolve FAISS path
# ---------------------------------------------------------

def resolve_index_path(persist_path="faiss_index"):
    """
    Convert the FAISS persistence path into an absolute path.

    Relative paths are resolved from the project directory,
    not from the current working directory.
    """

    path = Path(persist_path)

    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


# ---------------------------------------------------------
# Create vector store
# ---------------------------------------------------------

def create_vectorstore(docs, persist_path="faiss_index"):

    if not docs:
        print("[VectorStore] No documents provided to index.")
        return None

    index_path = resolve_index_path(persist_path)

    index_path.mkdir(parents=True, exist_ok=True)

    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    vectorstore.save_local(str(index_path))

    print(
        f"[VectorStore] FAISS index saved to: {index_path}"
    )

    return vectorstore


# ---------------------------------------------------------
# Load vector store
# ---------------------------------------------------------

def load_vectorstore(persist_path="faiss_index"):

    index_path = resolve_index_path(persist_path)

    index_file = index_path / "index.faiss"
    metadata_file = index_path / "index.pkl"

    # Both files are required for a valid LangChain FAISS store
    if not index_file.exists() or not metadata_file.exists():

        print(
            f"[VectorStore] FAISS index not found at: {index_path}"
        )

        return None

    print(
        f"[VectorStore] Loading FAISS index from: {index_path}"
    )

    return FAISS.load_local(
        str(index_path),
        embeddings,
        allow_dangerous_deserialization=True
    )


# ---------------------------------------------------------
# Incrementally update vector store
# ---------------------------------------------------------

def update_vectorstore(new_docs, persist_path="faiss_index"):
    """
    Incrementally add only new document chunks
    to the existing FAISS index.
    """

    index_path = resolve_index_path(persist_path)

    index_file = index_path / "index.faiss"
    metadata_file = index_path / "index.pkl"

    # -----------------------------------------------------
    # No new documents
    # -----------------------------------------------------

    if not new_docs:

        print(
            "[VectorStore] No new documents to add."
        )

        return load_vectorstore(persist_path)


    # -----------------------------------------------------
    # Existing FAISS index
    # -----------------------------------------------------

    if index_file.exists() and metadata_file.exists():

        print(
            f"[VectorStore] Existing index found: {index_path}"
        )

        vectorstore = FAISS.load_local(
            str(index_path),
            embeddings,
            allow_dangerous_deserialization=True
        )

        vectorstore.add_documents(new_docs)

        vectorstore.save_local(
            str(index_path)
        )

        print(
            f"[VectorStore] Added {len(new_docs)} "
            f"new chunks to existing FAISS index."
        )

    # -----------------------------------------------------
    # Missing / incomplete FAISS index
    # -----------------------------------------------------

    else:

        print(
            "[VectorStore] No valid FAISS index found."
        )

        print(
            f"[VectorStore] Creating new index at: {index_path}"
        )

        index_path.mkdir(
            parents=True,
            exist_ok=True
        )

        vectorstore = FAISS.from_documents(
            new_docs,
            embeddings
        )

        vectorstore.save_local(
            str(index_path)
        )

        print(
            f"[VectorStore] Created fresh FAISS index "
            f"with {len(new_docs)} chunks."
        )

    return vectorstore
