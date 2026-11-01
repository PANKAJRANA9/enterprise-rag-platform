# OmniRAG - Enterprise AI Operations Platform v2.0 (Capstone)
**Pitch:** Multi-tenant AI platform unifying CRM, Odoo, Parking, Medical, WhatsApp, NCERT with single RAG brain - RBAC, citations, analytics, $0 infra. Like Notion AI + Intercom + Odoo.

## Architecture
React (5173) -> Spring Boot (8080) -> PGVector enterprise_docs (HNSW) -> Ollama nomic-embed-text + llama3.2:3b 
<img width="1920" height="1280" alt="image" src="https://github.com/user-attachments/assets/bdbf6f74-46eb-478a-b650-2043f731a648" />
<img width="1920" height="1280" alt="image" src="https://github.com/user-attachments/assets/a625ff5f-e8d3-4a4f-bebf-6a61ec887177" />
<img width="1920" height="1280" alt="image" src="https://github.com/user-attachments/assets/7f69a7fe-15a5-4011-94b7-d339a1ba998c" />
<img width="1920" height="1280" alt="image" src="https://github.com/user-attachments/assets/3f2cd1e0-1181-4e7e-8020-cb08d70fc1df" />
<img width="1920" height="1280" alt="image" src="https://github.com/user-attachments/assets/9addeec3-edd8-4722-aacd-a227433a2626" />


## Quick Start (New Dev)
```bash
# 1. DB
docker compose up -d pg_pinecone

# 2. Ollama
ollama pull nomic-embed-text && ollama pull llama3.1:8b && ollama serve

# 3. Ingestion + Migration
cd ingestion
conda env create -f environment.yml && conda activate rag-platform
python main.py
python migrate_simple.py  # 6 tables -> enterprise_docs

# 4. Backend
cd ../backend
mvn clean install && mvn spring-boot:run

# 5. Frontend
cd ../frontend
npm install && npm run dev
# Open http://localhost:5173
```

## Why Not Shitty?
- Single table with metadata filtering (not 6 indexes)
- Prod layers: Controller -> Service Interface -> Repository + GlobalExceptionHandler + TraceFilter
- Allowlist prevents injection, empty check prevents hallucination
- Citations + latency + traceId returned
- $0 cost vs $70/mo Pinecone + OpenAI

## Demo for Interview (5 min)
1. Show React dashboard - 6 sources
2. Ask "Acme pricing issue" in crm_docs -> answer with sources
3. Ask-all "parking slot" -> searches all 6 in 1 query
4. Show /api/health + Grafana metrics
5. Say "Migrated 6 tables -> 1 table without re-embedding, O(1) scale"

## API
POST /api/ask {table, text}
<img width="1919" height="902" alt="oneSoucre" src="https://github.com/user-attachments/assets/630f265d-ec05-4ca1-b554-cc17e0507bac" />

POST /api/ask-all {text}

<img width="1919" height="1024" alt="RagImg1" src="https://github.com/user-attachments/assets/c5e0b83a-b3da-4edd-a4b6-e81ce8c876f1" />

## DB postgres pincomedb open source 100%
a semple table enterprise_docs  with embedings
<img width="1507" height="500" alt="image" src="https://github.com/user-attachments/assets/e631ef25-bb0d-4f49-a5bd-0f93a1d62cbd" />
<img width="1502" height="792" alt="db_imag1" src="https://github.com/user-attachments/assets/3fc92d89-cf14-4a8a-ae2b-4b3af3eb486b" />


GET /api/tables
GET /api/health
