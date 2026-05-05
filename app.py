import streamlit as st

st.set_page_config(page_title="RAG Document Agent", page_icon="🧠", layout="centered")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🧠 Autonomous Document Intelligence Agent")
st.caption("A demo of Retrieval-Augmented Generation (RAG) using LangChain + FAISS + LLM")

st.divider()

# ── What is this ──────────────────────────────────────────────────────────────
st.subheader("What is this?")
st.markdown("""
This is a live demo of an **Agentic RAG pipeline** — a system where an AI agent reads your document,
understands it using semantic search, and answers your questions with context-aware reasoning.

Built with **LangChain**, **FAISS vector search**, **HuggingFace embeddings**, and **Groq (llama3)**.
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

if uploaded_file:
    st.success(f"✅ `{uploaded_file.name}` uploaded successfully! Processing coming next...")