# evaluate_rag.py
from rag_pipeline import build_rag
from vectorstore import load_vectorstore

def run_tests():
    vectorstore = load_vectorstore("faiss_index")
    if not vectorstore:
        print("No FAISS index found. Run rebuild_index.py first.")
        return

    qa = build_rag(vectorstore)

    # Define test queries
    test_queries = [
        "What is BSS?",
        "List the BSS applications.",
        "Steps to onboard a customer.",
        "Who approves user access requests?",
        "Explain the employee information section."
    ]

    # Open log file
    with open("evaluation_results.txt", "w") as f:
        for query in test_queries:
            print(f"\nQuery: {query}")
            result = qa.invoke({"query": query})
            answer = result["result"]

            # Print to console
            print("Answer:", answer)

            # Save to file
            f.write(f"Query: {query}\n")
            f.write(f"Answer: {answer}\n")
            f.write("="*60 + "\n")

    print("\nEvaluation complete. Results saved to evaluation_results.txt")

if __name__ == "__main__":
    run_tests()

