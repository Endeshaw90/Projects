import streamlit as st
from rag_pipeline import build_rag, answer_query
from vectorstore import load_vectorstore

st.set_page_config(page_title="Safaricom BSS RAG Assistant", layout="centered")
st.title("Safaricom BSS RAG Assistant")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load FAISS index and build RAG pipeline
if "qa" not in st.session_state:
    vectorstore = load_vectorstore("faiss_index")
    if vectorstore is None:
        st.warning("No FAISS index found. Please create one first.")
    else:
        st.session_state.qa = build_rag(vectorstore)

# Function to format responses
def format_response(raw_answer: str) -> str:
    if "INSERT INTO" in raw_answer:
        return (
            "### Step 1: Retrieve Channel Information\n"
            "Obtain Channel ID and Channel Name from UPC.\n\n"
            "### Step 2: Insert into COM_CHANNELS_CONFIG\n"
            "```sql\nINSERT INTO COM_CHANNELS_CONFIG (CHANNEL_ID, CHANNEL_NAME) VALUES (33, 'DASHEN_BANK');\n```\n\n"
            "### Step 3: Map External Channel\n"
            "```sql\nINSERT INTO COM_EXT_CHANNEL_MAPPING (CHANNEL_NAME, CHANNEL_ID, INSTANCE_ID) VALUES ('DASHEN_BANK', '33', 'INSTANCE_1');\n```\n\n"
            "### Step 4: Map SDP Channel\n"
            "```sql\nINSERT INTO COM_SDP_CHANNEL_MAPPING (CHANNEL_NAME, CHANNEL_ID, INSTANCE_ID) VALUES ('DASHEN_BANK', '33', 'INSTANCE_1');\n```\n\n"
            "Replace values with actual Channel ID, Channel Name, and Instance ID."
        )
    else:
        return f"Here’s a structured version:\n\n- {raw_answer}"

# ✅ Polite placeholder for new questions
new_query = st.text_input("Hi, Dear. What can I assist you please?")

if new_query.strip() and "qa" in st.session_state:
    raw_answer = answer_query(new_query, st.session_state.qa)
    st.session_state.chat_history.append({
        "answer": raw_answer,
        "formatted": format_response(raw_answer)
    })

# Display only useful information (answers + follow-ups)
for idx, entry in enumerate(st.session_state.chat_history):
    st.subheader("Original Response")
    st.write(entry["answer"])
    st.subheader("Formatted Response")
    st.markdown(entry["formatted"])

    # ✅ Polite follow-up placeholder
    follow_up = st.text_input("Do you have any other questions or need further details?", key=f"followup_{idx}")
    if follow_up.strip() and "qa" in st.session_state:
        enriched_followup = f"Based on the previous answer: {entry['answer']}\n\nFollow-up: {follow_up}"
        follow_up_answer = answer_query(enriched_followup, st.session_state.qa)
        st.markdown(f"**Response:** {follow_up_answer}")
    st.markdown("---")

