import os
import tempfile
import streamlit as st
from core import DocumentAgent
from loader import load_data

# ── Page config ──────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Doc Intelligence Agent",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# ── Custom CSS ───────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
#   @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

#   html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#   h1, h2, h3 { font-family: 'Space Mono', monospace; }

#   .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
#   .badge {
#     display: inline-block;
#     padding: 2px 10px;
#     border-radius: 999px;
#     font-size: 11px;
#     font-weight: 600;
#     letter-spacing: 0.5px;
#     margin-right: 6px;
#   }
#   .badge-pdf  { background: #dbeafe; color: #1e40af; }
#   .badge-csv  { background: #dcfce7; color: #166534; }
#   .badge-txt  { background: #fef9c3; color: #854d0e; }

#   footer { visibility: hidden; }
# </style>
# """, unsafe_allow_html=True)


# # ── Session state ─────────────────────────────────────────────────────────────
# if "agent" not in st.session_state:
#     st.session_state.agent = DocumentAgent()
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "file_loaded" not in st.session_state:
#     st.session_state.file_loaded = False
# if "file_info" not in st.session_state:
#     st.session_state.file_info = {}


# # ── Sidebar ──────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("## 🧠 Doc Intelligence Agent")
#     st.markdown("*Agentic RAG — upload a doc, ask anything.*")
#     st.divider()

#     uploaded_file = st.file_uploader(
#         "Upload a document",
#         type=["pdf", "csv", "txt"],
#         help="Supports PDF, CSV, and plain text files.",
#     )

#     if uploaded_file:
#         if st.button("⚡ Process Document", type="primary", use_container_width=True):
#             with st.spinner("Chunking, embedding, indexing…"):
#                 suffix = "." + uploaded_file.name.split(".")[-1]
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#                     tmp.write(uploaded_file.read())
#                     tmp_path = tmp.name

#                 try:
#                     data = load_data(tmp_path)
#                     st.session_state.agent.load(data)
#                     st.session_state.file_loaded = True
#                     st.session_state.file_info = {
#                         "name": uploaded_file.name,
#                         "type": data["type"],
#                         "chunks": data.get("chunks", "—"),
#                     }
#                     st.session_state.messages = []
#                     st.success("Ready! Start asking questions below.")
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                 finally:
#                     os.unlink(tmp_path)

#     if st.session_state.file_loaded:
#         info = st.session_state.file_info
#         file_type = info["type"].upper()
#         badge_class = f"badge-{info['type']}"
#         st.markdown(f"""
#         **Loaded:** `{info['name']}`  
#         <span class='badge {badge_class}'>{file_type}</span>
#         {"Chunks: **" + str(info['chunks']) + "**" if info['chunks'] != "—" else ""}
#         """, unsafe_allow_html=True)
#         st.divider()

#         if st.button("🗑️ Clear Chat", use_container_width=True):
#             st.session_state.messages = []
#             st.session_state.agent.chat_history = []
#             st.rerun()

#     st.divider()
#     st.markdown("""
#     **Stack**  
#     LangChain · FAISS · HuggingFace · Groq (llama3)

#     [GitHub](https://github.com/) · [LinkedIn](https://linkedin.com/)
#     """)


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("# Autonomous Document Intelligence Agent")
st.markdown("Upload a **PDF, CSV, or TXT** file, then chat with your document using agentic RAG.")

if not st.session_state.file_loaded:
    st.info("👈 Upload a file in the sidebar to get started.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📄 PDF")
        st.markdown("Research papers, contracts, reports — ask anything.")
    with col2:
        st.markdown("### 📊 CSV")
        st.markdown("Upload tabular data and get instant analytical answers.")
    with col3:
        st.markdown("### 📝 TXT")
        st.markdown("Logs, notes, raw text - ask queries.")

else:
    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    if prompt := st.chat_input("Ask a question about your document…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Agent thinking…"):
                response = st.session_state.agent.run(prompt)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})