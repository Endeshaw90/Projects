# app.py - ChatGPT-Style Streamlit UI with Dual Mode Switch & Document Viewer
import os
import glob
import streamlit as st

from loaders import load_documents, filter_new_documents
from vectorstore import create_vectorstore, load_vectorstore, update_vectorstore
from sparse_search import BM25SearchEngine
from hybrid_retriever import hybrid_retrieve
from rag_pipeline import execute_rag

st.set_page_config(
    page_title="BSS_RAG | Grounded Knowledge Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Glassmorphism CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    /* Custom Card */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
    }
    
    /* Fix Chat Input Container with Green Boundary Line & White Font */
    div[data-testid="stChatInput"] {
        background-color: #1e293b !important;
        border: 2px solid #22c55e !important; /* Glowing green boundary line */
        border-radius: 12px !important;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.35) !important;
    }
    
    div[data-testid="stChatInput"] * {
        background-color: transparent !important;
    }
    
    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important; /* Crisp white typed text font */
        background-color: transparent !important;
        font-size: 1rem !important;
    }
    
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important; /* Dark/muted placeholder text */
        opacity: 1 !important;
    }

    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background-color: #1e293b !important;
        border: 2px solid #22c55e !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="input"] input {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    
    /* Mode Pill Switch */
    .stRadio > div {
        flex-direction: row;
        background: #1e293b;
        border: 1px solid #38bdf8;
        border-radius: 30px;
        padding: 4px;
    }
    
    .stRadio label {
        color: #e2e8f0 !important;
        font-weight: 600;
    }

    /* Citation badge */
    .citation-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid #38bdf8;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.82rem;
        font-weight: 500;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "active_doc" not in st.session_state:
    st.session_state.active_doc = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = load_vectorstore("faiss_index")
if "bm25_engine" not in st.session_state:
    st.session_state.bm25_engine = BM25SearchEngine()

# Auto Indexing check on startup
if st.session_state.vectorstore and not st.session_state.bm25_engine.documents:
    # Build BM25 index from loaded docs (scans BSS_docs first)
    target_path = "BSS_docs" if os.path.exists("BSS_docs") else "data/BSS_Safaricom"
    raw_docs = load_documents(target_path, chunk_size=800, chunk_overlap=150)
    st.session_state.bm25_engine.index_documents(raw_docs)

# -------------------------------------------------------------
# SIDEBAR: Control Panel & Navigation
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #22c55e, #38bdf8); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">B</div>
        <div>
            <div style="font-size: 0.75rem; color: #22c55e; font-weight: 700; letter-spacing: 1px;">KNOWLEDGE BASE CHAT</div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #f8fafc;">BSS_RAG</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Ask across indexed corpus with grounded answers & verifiable citations.")

    # Category Navigator
    st.markdown("### 📂 Corpus Categories")
    cat = st.radio("Select Category", ["📁 BSS Documentation", "📜 AI Engineering Specs", "🛡️ Compliance & SOPs", "🕒 Recent Sessions"], label_visibility="collapsed")

    st.markdown("---")

    # Ingestion Panel
    st.markdown("### ⚙️ Corpus Composer")
    default_dir = "BSS_docs" if os.path.exists("BSS_docs") else "data/BSS_Safaricom"
    corpus_path = st.text_input("Corpus Directory", value=default_dir)
    
    if st.button("🔄 Ingest New Documents", use_container_width=True):
        with st.spinner(f"Scanning '{corpus_path}' for new documents..."):
            all_docs = load_documents(corpus_path, chunk_size=800, chunk_overlap=150)
            if all_docs:
                new_docs, existing_count = filter_new_documents(all_docs, "faiss_index/ingested_registry.json")
                if new_docs:
                    st.session_state.vectorstore = update_vectorstore(new_docs, "faiss_index")
                    st.session_state.bm25_engine.add_documents(new_docs)
                    st.success(f"✨ Successfully ingested {len(new_docs)} NEW document chunks from {corpus_path}!")
                else:
                    st.info(f"⚡ All documents in {corpus_path} are up-to-date! No new data found.")
            else:
                st.warning(f"No PDF, DOCX, TXT, or JSON files found in '{corpus_path}'. Please check the folder path.")

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    
    # Stats Card
    doc_count = len(st.session_state.bm25_engine.documents) if st.session_state.bm25_engine else 0
    st.markdown(f"""
    <div style="display: flex; gap: 12px; margin-top: 10px;">
        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px; flex: 1; text-align: center;">
            <div style="font-size: 1.4rem; font-weight: 700; color: #38bdf8;">{doc_count}</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Indexed Chunks</div>
        </div>
        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px; flex: 1; text-align: center;">
            <div style="font-size: 1.4rem; font-weight: 700; color: #4ade80;">{len(st.session_state.chat_history)}</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Assistant Turns</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# MAIN INTERFACE
# -------------------------------------------------------------
col_chat, col_viewer = st.columns([1.3, 1.0])

with col_chat:
    st.markdown("""
    <div style="font-size: 0.8rem; font-weight: 700; color: #38bdf8; letter-spacing: 1px; margin-bottom: 4px;">GROUNDED KNOWLEDGE ASSISTANT</div>
    <h2 style="margin-top: 0; font-weight: 700;">Ask your documents</h2>
    """, unsafe_allow_html=True)

    mode_choice = st.radio(
        "Response Mode",
        options=["📄 Direct Source Extraction", "🤖 AI Synthesized Notes"],
        horizontal=True,
        help="Direct Source Extraction provides verbatim zero-hallucination facts. AI Synthesized Notes summarizes and formats insights."
    )

    selected_mode = "direct_source" if "Direct Source" in mode_choice else "generative_ai"

    # Interactive Initial Greeting & Starter Prompts
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("""
        👋 **Hello! Welcome to BSS_RAG | Grounded Knowledge Assistant.**
        
        I am your interactive AI assistant for **BSS Systems**, **AI Engineering specs**, and **Enterprise SOPs**.
        Ask any question or pick a starter prompt below:
        """)

    # Starter Prompt Pills
    st.markdown("##### 🚀 Starter Prompts:")
    p_col1, p_col2 = st.columns(2)
    prompt_query = None
    with p_col1:
        if st.button("📘 What are the key concepts in AI Engineering?", use_container_width=True):
            prompt_query = "What are the key concepts in AI Engineering?"
    with p_col2:
        if st.button("⚡ What is BSS and its applications?", use_container_width=True):
            prompt_query = "What is BSS and its core applications?"

    for msg in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(msg["query"])
            
        with st.chat_message("assistant"):
            st.markdown(msg["response"]["answer"])
            
            # Citation Badges
            if msg["response"]["citations"]:
                st.markdown("<div style='margin-top: 10px; font-weight: 600; color: #94a3b8; font-size: 0.85rem;'>VERIFIED SOURCES:</div>", unsafe_allow_html=True)
                for cit in msg["response"]["citations"]:
                    if st.button(f"📄 Source: {cit['filename']} (Page {cit['page']})", key=f"cit_{cit['chunk_id']}_{hash(msg['query'])}"):
                        st.session_state.active_doc = cit

    # Chat Input Box
    user_input = st.chat_input("Ask about APIs, flows, tables, error codes, or roles...")
    query = prompt_query or user_input
    
    if query:
        # Retrieve docs via RRF Hybrid Search
        retrieved_docs = hybrid_retrieve(
            query=query,
            vectorstore=st.session_state.vectorstore,
            bm25_engine=st.session_state.bm25_engine,
            top_k=4
        )
        
        # Execute Dual Mode RAG Generation
        response = execute_rag(query, retrieved_docs, mode=selected_mode)
        
        # Save to chat history
        st.session_state.chat_history.append({"query": query, "response": response})
        
        # Auto-set top citation for side document viewer
        if response["citations"]:
            st.session_state.active_doc = response["citations"][0]
            
        st.rerun()

# -------------------------------------------------------------
# RIGHT PANEL: Direct Document Viewer
# -------------------------------------------------------------
with col_viewer:
    st.markdown("""
    <div style="font-size: 0.8rem; font-weight: 700; color: #38bdf8; letter-spacing: 1px; margin-bottom: 4px;">VERIFIABLE EVIDENCE</div>
    <h3 style="margin-top: 0; font-weight: 700;">Document Inspector</h3>
    """, unsafe_allow_html=True)

    if st.session_state.active_doc:
        doc_info = st.session_state.active_doc
        
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #38bdf8;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: 700; color: #f8fafc; font-size: 1.1rem;">📄 {doc_info['filename']}</div>
                <div style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 2px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 600;">Page {doc_info['page']}</div>
            </div>
            <div style="margin-top: 12px; font-size: 0.82rem; color: #94a3b8;">
                <div><b>Freshness:</b> <span style="color: #4ade80;">✔ Verified Active Document</span></div>
                <div><b>Chunk ID:</b> <code>{doc_info['chunk_id']}</code></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🎯 Highlighted Source Chunk")
        st.markdown(f"""
        <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid #38bdf8; border-radius: 10px; padding: 16px; color: #e2e8f0; font-family: monospace; font-size: 0.88rem; line-height: 1.6;">
            <span style="background: #fde047; color: #000; font-weight: bold; padding: 2px 4px; border-radius: 4px;">MATCHED EXCERPT</span><br/><br/>
            {doc_info['full_content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px; background: rgba(30,41,59,0.2); border-radius: 16px; border: 1px dashed #334155;">
            <div style="font-size: 2rem; margin-bottom: 10px;">📄</div>
            <div style="color: #94a3b8; font-size: 0.9rem;">No document page selected.<br/>Ask a question to auto-render the exact source page snippet here.</div>
        </div>
        """, unsafe_allow_html=True)
