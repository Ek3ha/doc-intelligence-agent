import os
import tempfile
import streamlit as st
from loader import load_data
from core import DocumentAgent
 

st.set_page_config(page_title="RAG Document Agent", page_icon="🧠", layout="centered")

# ── Session state ─────────────────────────────────────────────────────────────
if "agent" not in st.session_state:
    st.session_state.agent = DocumentAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_loaded" not in st.session_state:
    st.session_state.file_loaded = False

# ══════════════════════════════════════════════════════════════════════════════
# LANDING SECTION 
# ══════════════════════════════════════════════════════════════════════════════
st.title("🧠 Autonomous Document Intelligence Agent")
st.caption("A demo of Retrieval-Augmented Generation (RAG) using LangChain + FAISS + LLM")

st.divider()

# ── What is this ──────────────────────────────────────────────────────────────
st.subheader("What is this?")
st.markdown("""
This is a live demo of an **Agentic RAG pipeline** — a system where an AI agent reads your document,
understands it using semantic search, and answers your questions with context-aware reasoning.

Built with **LangChain**, **FAISS vector search**, **HuggingFace embeddings**, and **Llama3**.
""")

st.divider()

# ── Use cases ─────────────────────────────────────────────────────────────────
st.subheader("Use Cases")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 📄 PDF")
    st.markdown("""
- Research paper Q&A  
- Legal contract review  
- Financial report analysis  
- Resume parsing  
""")

with col2:
    st.markdown("#### 📊 CSV")
    st.markdown("""
- Sales data queries  
- Survey result analysis  
- Inventory insights  
- Employee record lookup  
""")

with col3:
    st.markdown("#### 📝 TXT")
    st.markdown("""
- Log file investigation  
- Policy document search  
- Meeting notes Q&A  
- Knowledge base queries  
""")

st.divider()

# ── Upload ────────────────────────────────────────────────────────────────────
st.subheader("Try it yourself")
st.markdown("Upload a **PDF**, **CSV**, or **TXT** file to get started.")

uploaded_file = st.file_uploader(
    label="Choose a file",
    type=["pdf", "csv", "txt"],
    label_visibility="collapsed"
)

if uploaded_file and not st.session_state.file_loaded:
    print("---------------------------------FILE UIPLOADED---------------------",uploaded_file)
    with st.spinner("Chunking → Embedding → Storing in FAISS…"):
        suffix = "." + uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        try:
            data = load_data(tmp_path)
            print("-------------------------------DATA----------------------",data)
            st.session_state.agent.load(data)
            st.session_state.file_loaded = True
            st.session_state.messages = []
            chunks = data.get("chunks", "—")
            st.success(f"✅ `{uploaded_file.name}` ready — {chunks} chunks stored in FAISS.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            os.unlink(tmp_path)
 
# reset if user uploads a new file
if not uploaded_file and st.session_state.file_loaded:
    st.session_state.file_loaded = False
    st.session_state.messages = []
    st.session_state.agent = DocumentAgent()


# CHAT SECTION  (only shown after file is loaded)

if st.session_state.file_loaded:
    st.divider()
    st.subheader("💬 Ask your document")
 
    # display history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
 
    # input
    if prompt := st.chat_input("Type your question…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
 
        with st.chat_message("assistant"):
            with st.spinner("Retrieving context and generating answer…"):
                response = st.session_state.agent.run(prompt)
            st.markdown(response)
 
        st.session_state.messages.append({"role": "assistant", "content": response})
 
    if st.session_state.messages:
        if st.button("🗑️ Clear chat"):
            st.session_state.messages = []
            st.session_state.agent.chat_history = []
            st.rerun()