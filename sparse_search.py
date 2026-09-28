# sparse_search.py - BM25 Keyword Search for Exact Telecom Identifiers
import re
from typing import List, Tuple
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document

class BM25SearchEngine:
    def __init__(self):
        self.bm25 = None
        self.documents: List[Document] = []

    def _tokenize(self, text: str) -> List[str]:
        # Preserve alphanumeric codes (e.g. COM_CHANNELS_CONFIG, ORA-00942, 33)
        return re.findall(r'\b[A-Za-z0-9_\-]+\b', text.lower())

    def index_documents(self, documents: List[Document]):
        self.documents = documents
        corpus = [self._tokenize(doc.page_content) for doc in documents]
        if corpus:
            self.bm25 = BM25Okapi(corpus)
            print(f"[BM25] Indexed {len(documents)} document chunks for exact keyword search.")

    def add_documents(self, new_documents: List[Document]):
        if not new_documents:
            return
        self.documents.extend(new_documents)
        corpus = [self._tokenize(doc.page_content) for doc in self.documents]
        if corpus:
            self.bm25 = BM25Okapi(corpus)
            print(f"[BM25] Updated BM25 index. Total chunks: {len(self.documents)}")

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        if not self.bm25 or not self.documents:
            return []
        
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Sort documents by BM25 score
        scored_docs = list(zip(self.documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # Filter docs with score > 0
        results = [item for item in scored_docs[:top_k] if item[1] > 0]
        return results
