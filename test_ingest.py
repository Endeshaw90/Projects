import os
from loaders import load_documents, filter_new_documents
from vectorstore import update_vectorstore

docs = load_documents('BSS_docs', chunk_size=800, chunk_overlap=150)
print('Loaded chunks from BSS_docs:', len(docs))

if docs:
    new_docs, existing_count = filter_new_documents(docs, 'faiss_index/ingested_registry.json')
    print('Found new chunks to index:', len(new_docs))
    if new_docs:
        update_vectorstore(new_docs, 'faiss_index')
        print('Successfully updated FAISS index!')
