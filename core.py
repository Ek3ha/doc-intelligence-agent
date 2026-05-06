import os
from typing import Optional
import streamlit as st

# GET API KEY
def get_api_key():
    # Streamlit Cloud
    if "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    # Local .env
    return os.getenv("GROQ_API_KEY")

# ── LLM factory ─────────────────────────────────────────────────────────────
# def get_llm():
#     from langchain_community.chat_models import ChatOllama
#     return ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3"))
def get_llm():
    """Return the appropriate LLM based on available env vars."""
    groq_key=get_api_key()
    if groq_key:
        from langchain_groq import ChatGroq
        return ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=groq_key,
            temperature=0.2,
        )
    # Fallback to local Ollama
    from langchain_community.chat_models import ChatOllama
    return ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3"))

# ── Tools ────────────────────────────────────────────────────────────────────
def retrieve_context(query: str, vector_db, k: int = 3) -> str:
    results = vector_db.similarity_search(query, k=k)
    return "\n\n".join([r.page_content for r in results])


def process_document(text: str, task: str, llm,memory_context:str) -> str:
    response = llm.invoke(f"""You are a helpful assistant answering questions about a document.
        
                            Conversation so far:
                            {memory_context}
                            
                            Use the context below to answer the question. If the answer is not in the context, say so.
                            
                            Context:
                            {text}
                            
                            Question: {task}
                            """)
    return response.content


def analyze_csv(df, query: str, llm, memory_context: str) -> str:
    response = llm.invoke(f"""You are a data analyst. Answer the question based strictly on the data.
 
                            Conversation so far:
                            {memory_context}
                            
                            Data:
                            {df.tostring()}
                            
                            Question: {query}
                            """)
    return response.content
 


# ── Agent ────────────────────────────────────────────────────────────────────
class DocumentAgent:
    def __init__(self):
        self.llm = get_llm()
        self.chat_history: list[str] = []
        self.data: Optional[dict] = None

    def load(self, data: dict):
        self.data = data
        self.chat_history = []

    def run(self, user_query: str) -> str:
        if not self.data:
            return {"answer": "⚠️ No document loaded.", "chunks": []}
        self.chat_history.append(f"User: {user_query}")
        memory_context = "\n".join(self.chat_history)

        if self.data["type"] == "csv":
            result = analyze_csv(self.data["df"], user_query, self.llm,memory_context)
            chunks = []

        elif self.data["type"] in ("pdf", "txt"):
            context = retrieve_context(user_query, self.data["vector_db"])
            result = process_document(context, user_query, self.llm,memory_context)

        else:
            result = self.llm.invoke(f"""Conversation so far:
                                        {memory_context}
 
                                        Question: {user_query}
                                        """).content
            chunks = []

        self.chat_history.append(f"Agent: {result}")
        return {"answer": result, "chunks": chunks}