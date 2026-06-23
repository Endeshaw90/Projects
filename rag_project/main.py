# main.py
from loaders import load_documents
from vectorstore import create_vectorstore, load_vectorstore
from rag_pipeline import build_rag

def main():
    print("Checking for existing vectorstore...")
    vectorstore = load_vectorstore("faiss_index")

    if not vectorstore:
        print("No existing index found. Creating new one...")
        docs = load_documents("data/BSS_Safaricom")
        vectorstore = create_vectorstore(docs, "faiss_index")

    print("Building RAG pipeline...")
    qa = build_rag(vectorstore)

    while True:
        query = input("\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break

        result = qa.invoke({"query": query})
        print("\nAnswer:", result["result"])

if __name__ == "__main__":
    main()

