# 📚 Local NCERT RAG System (Production-Ready)

A locally hosted, open-source Retrieval-Augmented Generation (RAG) pipeline designed to ingest, embed, and retrieve NCERT textbook content. Built with **PostgreSQL**, **pg_pinecone**, and **Qwen-compatible embeddings**, this project runs entirely on your machine for free.

## ✨ Production Features
- **Idempotent Ingestion**: Uses chunk hashing to prevent duplicate data if the script crashes or runs twice.
- **Resilient Retries**: Implements exponential backoff for embedding model calls to handle temporary network/model failures.
- **Connection Pooling**: Thread-safe database connections to handle concurrent queries without bottlenecks.

## 🛠️ Prerequisites
1. **Docker Desktop** installed and running.
2. **Python 3.10+** installed.
3. **Git** (optional, for cloning).

---

## 🚀 Quick Start

### Step 1: Clone and Navigate
```bash
git clone <your-repo-url>
cd local-pinecone

```
## step 2 : run pgpinecone in local pod

docker compose up -d

### create index  


CREATE TABLE IF NOT EXISTS parking_docs (id SERIAL, content TEXT, meta JSONB, embedding vector(768));
CREATE TABLE IF NOT EXISTS whatsapp_docs (id SERIAL, content TEXT, meta JSONB, embedding vector(768));
CREATE TABLE IF NOT EXISTS test_vec (id SERIAL, embedding vector(768));

SELECT table_name FROM information_schema.tables WHERE table_schema='public';

### delete old data if needed

# Inside ingestion folder
rm -rf src/__pycache__ src/*/__pycache__ src/*/*/__pycache__

# Drop all tables from your pg_pinecone pod name pg_pinecone_local
docker exec -it pg_pinecone_local psql -U postgres -d pinecone_db -c "DROP TABLE IF EXISTS ncert_docs, crm_docs, odoo_docs, parking_docs, medical_kb, whatsapp_docs, test_vec CASCADE;"


### run data mock ingestio pipeline 
# 1. Activate env
conda activate rag-platform

# 2. Make sure Ollama + DB running
ollama serve
docker compose up pg_pinecone -d

# 3. Create .env from example
cp .env.example .env

# 4. Run ALL
cd ingestion
python main.py

# 5. Run single table
python main.py --table crm_docs

# 6. Test search
python -c "from src.services.embedding_service import EmbeddingService; from src.services.vector_store_service import VectorStoreService; e=EmbeddingService(); vs=VectorStoreService(); q=e.embed_text('Acme pricing issue'); print(vs.search('crm_docs', q))"