from loaders import load_documents
from vectorstore import create_vectorstore
from sparse_search import BM25SearchEngine
from hybrid_retriever import hybrid_retrieve
from rag_pipeline import execute_rag

docs = load_documents('data/BSS_Safaricom', chunk_size=800, chunk_overlap=150)
print('Total loaded chunks:', len(docs))

if docs:
    vs = create_vectorstore(docs, 'faiss_index')
    bm25 = BM25SearchEngine()
    bm25.index_documents(docs)
    
    results = hybrid_retrieve('What is BSS?', vs, bm25, top_k=3)
    print('Hybrid Search Results:', len(results))
    
    res = execute_rag('What is BSS?', results, mode='direct_source')
    print('Mode A Answer Preview:')
    print(res['answer'][:300])
