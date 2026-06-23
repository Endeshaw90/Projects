# rag_pipeline.py
import logging
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_classic.chains import RetrievalQA

logging.basicConfig(level=logging.INFO)

def build_rag(vectorstore):
    logging.info("Starting RAG pipeline build...")

    generator = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",   # ✅ lightweight model for CPU
        tokenizer="google/flan-t5-small",
        max_length=128,
        device_map="auto"
    )
    logging.info("HuggingFace pipeline created successfully.")

    llm = HuggingFacePipeline(pipeline=generator)
    logging.info("Wrapped HuggingFace pipeline into LangChain LLM.")

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type="stuff"
    )
    logging.info("RetrievalQA chain built successfully.")

    return qa

def answer_query(query, qa):
    enriched_query = f"Based on the document, {query}. Please explain step by step with SQL examples and detailed notes."
    try:
        result = qa.invoke({"query": enriched_query})
        answer = result.get("result", "").strip()

        # Sanitize malformed output (like arrow spam)
        if not answer or all(ch in "→-" for ch in answer):
            answer = "Sorry, I couldn’t generate a proper answer. Please rephrase your question."

        return answer
    except Exception as e:
        return f"An error occurred while answering: {e}"

