import os
from typing import Optional

# ── LLM factory ─────────────────────────────────────────────────────────────
def get_llm():
    from langchain_community.chat_models import ChatOllama
    return ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3"))


# ── Tools ────────────────────────────────────────────────────────────────────
def retrieve_context(query: str, vector_db, k: int = 3) -> str:
    results = vector_db.similarity_search(query, k=k)
    return "\n\n".join([r.page_content for r in results])


def process_document(text: str, task: str, llm) -> str:
    return "HI"
#     response = llm.invoke(f"""Perform the following task on the given text.

# Task: {task}

# Text:
# {text}
# """)
#     return response.content


def analyze_csv(df, query: str, llm) -> str:
#     response = llm.invoke(f"""You are a data analyst. Answer the question based strictly on the data.

# Data:
# {df.to_string(max_rows=50)}

# Question: {query}
# """)
#     return response.content
    return "Hello"


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
            return "⚠️ No document loaded. Please upload a file first."

        self.chat_history.append(f"User: {user_query}")
        memory_context = "\n".join(self.chat_history[-6:])

        if self.data["type"] == "csv":
            result = analyze_csv(self.data["df"], user_query, self.llm)

        elif self.data["type"] in ("pdf", "txt"):
            context = retrieve_context(user_query, self.data["vector_db"])
            print("---------------------------------CONTEXT",context)
            result = process_document(context, user_query, self.llm)

        else:
            result = self.llm.invoke(user_query).content

        self.chat_history.append(f"Agent: {result}")
        return result