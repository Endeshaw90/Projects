# loaders.py
import glob, os
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(path="data/BSS_Safaricom"):
    docs = []

    # Load all DOCX files
    for file in glob.glob(os.path.join(path, "**/*.docx"), recursive=True):
        docs.extend(Docx2txtLoader(file).load())

    # Load all PDFs
    for file in glob.glob(os.path.join(path, "**/*.pdf"), recursive=True):
        docs.extend(PyPDFLoader(file).load())

    # Load all TXT files
    for file in glob.glob(os.path.join(path, "**/*.txt"), recursive=True):
        docs.extend(TextLoader(file).load())

    # Load all JSON files (Postman collections)
    for file in glob.glob(os.path.join(path, "**/*.json"), recursive=True):
        json_loader = JSONLoader(
            file_path=file,
            jq_schema=".info, .item[]?.name, .item[]?.request?.url, .item[]?.request?.description",
            text_content=False   # prevents crash on dicts
        )
        postman_docs = json_loader.load()

        # Flatten dicts into strings for embeddings
        for d in postman_docs:
            if isinstance(d.page_content, dict):
                d.page_content = str(d.page_content)
        docs.extend(postman_docs)

    # Split into chunks with overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # try 500, 800, or 1000
        chunk_overlap=50 # overlap preserves context
    )
    return text_splitter.split_documents(docs)

