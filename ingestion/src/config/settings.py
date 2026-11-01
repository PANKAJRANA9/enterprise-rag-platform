import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_NAME = os.getenv("POSTGRES_DB", "pinecone_db")
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret123")
    DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
    DB_PORT = os.getenv("POSTGRES_PORT", "5433")
    
    OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1:8b")
    VECTOR_DIM = int(os.getenv("VECTOR_DIM", "768"))

settings = Settings()