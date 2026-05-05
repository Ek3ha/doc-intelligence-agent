import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def detect_file_type(file_path: str) -> str:
    ext = file_path.lower()
    if ext.endswith(".pdf"):
        return "pdf"
    elif ext.endswith(".csv"):
        return "csv"
    elif ext.endswith(".txt"):
        return "txt"
    else:
        return "unknown"


def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    return loader.load()


def load_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def load_txt(file_path: str):
    from langchain_community.document_loaders import TextLoader
    loader = TextLoader(file_path)
    return loader.load()


def chunk_documents(documents, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


def create_vector_db(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(chunks, embeddings)


def load_data(file_path: str) -> dict:
    file_type = detect_file_type(file_path)

    if file_type == "pdf":
        docs = load_pdf(file_path)
        chunks = chunk_documents(docs)
        vector_db = create_vector_db(chunks)
        return {"type": "pdf", "vector_db": vector_db, "chunks": len(chunks)}

    elif file_type == "csv":
        df = load_csv(file_path)
        return {"type": "csv", "df": df}

    elif file_type == "txt":
        docs = load_txt(file_path)
        chunks = chunk_documents(docs)
        vector_db = create_vector_db(chunks)
        return {"type": "txt", "vector_db": vector_db, "chunks": len(chunks)}

    else:
        raise ValueError(f"Unsupported file type: {file_path}")