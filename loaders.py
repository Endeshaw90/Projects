# loaders.py - Structure-Aware Document Loader with Overlapping Chunks
import os
import glob
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_documents(path: str = "BSS_docs", chunk_size: int = 800, chunk_overlap: int = 150) -> List[Document]:
    raw_docs: List[Document] = []
    
    if not os.path.isabs(path):
        path = os.path.join(BASE_DIR, path)

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        print(f"[Loader] Directory {path} created.")

    pdf_files = glob.glob(os.path.join(path, "**/*.pdf"), recursive=True)
    for f in pdf_files:
        try:
            loader = PyPDFLoader(f)
            pages = loader.load()
            filename = os.path.basename(f)
            for p in pages:
                page_num = p.metadata.get("page", 0) + 1
                p.metadata["source_filename"] = filename
                p.metadata["page_number"] = page_num
                p.metadata["full_path"] = f
                p.metadata["doc_type"] = "PDF"
            raw_docs.extend(pages)
        except Exception as e:
            print(f"[Loader Error] Failed loading PDF {f}: {e}")

    docx_files = glob.glob(os.path.join(path, "**/*.docx"), recursive=True)
    for f in docx_files:
        try:
            loader = Docx2txtLoader(f)
            docs = loader.load()
            filename = os.path.basename(f)
            for d in docs:
                d.metadata["source_filename"] = filename
                d.metadata["page_number"] = 1
                d.metadata["full_path"] = f
                d.metadata["doc_type"] = "DOCX"
            raw_docs.extend(docs)
        except Exception as e:
            print(f"[Loader Error] Failed loading DOCX {f}: {e}")

    txt_files = glob.glob(os.path.join(path, "**/*.txt"), recursive=True)
    for f in txt_files:
        try:
            loader = TextLoader(f, encoding="utf-8")
            docs = loader.load()
            filename = os.path.basename(f)
            for d in docs:
                d.metadata["source_filename"] = filename
                d.metadata["page_number"] = 1
                d.metadata["full_path"] = f
                d.metadata["doc_type"] = "TXT"
            raw_docs.extend(docs)
        except Exception as e:
            print(f"[Loader Error] Failed loading TXT {f}: {e}")

    json_files = glob.glob(os.path.join(path, "**/*.json"), recursive=True)
    for f in json_files:
        try:
            filename = os.path.basename(f)
            loader = JSONLoader(
                file_path=f,
                jq_schema=".info // .item[]? // .",
                text_content=False
            )
            json_docs = loader.load()
            for d in json_docs:
                if isinstance(d.page_content, dict):
                    d.page_content = str(d.page_content)
                d.metadata["source_filename"] = filename
                d.metadata["page_number"] = 1
                d.metadata["full_path"] = f
                d.metadata["doc_type"] = "JSON"
            raw_docs.extend(json_docs)
        except Exception as e:
            print(f"[Loader Error] Failed loading JSON {f}: {e}")

    print(f"[Loader] Loaded {len(raw_docs)} raw document pages/sections.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunked_docs = text_splitter.split_documents(raw_docs)
    
    for idx, doc in enumerate(chunked_docs):
        doc.metadata["chunk_id"] = f"{doc.metadata.get('source_filename', 'doc')}_p{doc.metadata.get('page_number', 1)}_c{idx}"
        
    print(f"[Loader] Created {len(chunked_docs)} overlapping chunks (size={chunk_size}, overlap={chunk_overlap}).")
    return chunked_docs

import hashlib
import json

def get_chunk_hash(doc: Document) -> str:
    content = doc.page_content + doc.metadata.get("source_filename", "") + str(doc.metadata.get("page_number", 1))
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def filter_new_documents(docs: List[Document], registry_file: str = "faiss_index/ingested_registry.json"):
    """
    Checks each chunk against the persisted SHA256 hash registry.
    Returns only NEW document chunks that have not been ingested yet.
    """
    dir_name = os.path.dirname(registry_file)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    existing_hashes = set()
    if os.path.exists(registry_file):
        try:
            with open(registry_file, "r") as f:
                existing_hashes = set(json.load(f))
        except Exception:
            existing_hashes = set()
            
    new_docs = []
    updated_hashes = set(existing_hashes)
    
    for doc in docs:
        chash = get_chunk_hash(doc)
        doc.metadata["chunk_hash"] = chash
        if chash not in existing_hashes:
            new_docs.append(doc)
            updated_hashes.add(chash)
            
    if new_docs:
        with open(registry_file, "w") as f:
            json.dump(list(updated_hashes), f)
            
    return new_docs, len(existing_hashes)
