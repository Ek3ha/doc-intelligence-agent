# Autonomous Document Intelligence Agent

This project builds a step-by-step agentic AI system that can:
- Read PDFs/ CSV/ text
- Understand content using embeddings (RAG)
- Answer questions using LLM reasoning
- Decide when to use tools

---

> **Agentic RAG pipeline** — upload any PDF, CSV, or text file and interrogate it with a local or cloud LLM. The agent decides which tool to invoke based on your query, maintains conversation memory, and surfaces precise answers using vector search.
 

## 🚀 Features

- 📄 PDF ingestion
- ✂️ Intelligent chunking
- 🧠 Embeddings + Vector Search (FAISS)
- 🤖 Agent with decision-making
- 💬 Conversation memory
- 🔧 Modular tool-based architecture

---

## 🧠 Architecture

User Query  
→ Agent decides  
→ Retrieve Context (RAG)  
→ Process Document (LLM)  
→ Final Answer  

```
User Query
    │
    ▼
┌─────────────────────────────┐
│        DocumentAgent        │  ← decides which tool to invoke
│  (chat memory + routing)    │
└──────────┬──────────────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
[PDF / TXT]    [CSV]
    │             │
    ▼             ▼
FAISS Vector   DataFrame
   Search       Analysis
    │             │
    └──────┬──────┘
           ▼
    LLM (Ollama)
           │
           ▼
      Final Answer
```
---

🧠 Autonomous Document Intelligence Agent

Agentic RAG pipeline — upload any PDF, CSV, or text file and interrogate it with a local or cloud LLM. The agent decides which tool to invoke based on your query, maintains conversation memory, and surfaces precise answers using vector search.

## 🛠️ Setup

### 1. Install dependencies

```bash
git clone https://github.com/YOUR_USERNAME/doc-intelligence-agent.git
cd doc-intelligence-agent
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```


### 2. Install and run Ollama

Download from:
https://ollama.com

```bash
ollama pull llama3

### Run the project
streamlit run app.py
 
Open [http://localhost:8501](http://localhost:8501), upload a file, start asking questions.
 
---
## 🐳 Docker
 
```bash
docker compose up --build
```
 
---

## 📄 License
 
MIT © 2025