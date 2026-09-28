# hybrid_retriever.py - Reciprocal Rank Fusion (RRF) Hybrid Search Engine
from typing import List
from langchain_core.documents import Document
from sparse_search import BM25SearchEngine

def hybrid_retrieve(query: str, vectorstore, bm25_engine: BM25SearchEngine, top_k: int = 5, k_rrf: int = 60) -> List[Document]:
    """
    Combines FAISS Dense Search + BM25 Sparse Search using Reciprocal Rank Fusion (RRF).
    RRF Score(d) = 1/(k + Rank_dense(d)) + 1/(k + Rank_sparse(d))
    """
    rrf_scores = {}
    doc_map = {}

    # 1. Dense Search (FAISS)
    dense_results = []
    if vectorstore:
        try:
            dense_results = vectorstore.similarity_search(query, k=top_k * 2)
        except Exception as e:
            print(f"[Hybrid Search Error] FAISS search failed: {e}")

    for rank, doc in enumerate(dense_results):
        doc_id = doc.metadata.get("chunk_id", str(hash(doc.page_content)))
        doc_map[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k_rrf + rank + 1))

    # 2. Sparse Search (BM25)
    sparse_results = bm25_engine.search(query, top_k=top_k * 2)
    for rank, (doc, score) in enumerate(sparse_results):
        doc_id = doc.metadata.get("chunk_id", str(hash(doc.page_content)))
        doc_map[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k_rrf + rank + 1))

    # Sort documents by RRF score
    sorted_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
    
    final_docs = [doc_map[did] for did in sorted_ids[:top_k]]
    return final_docs
