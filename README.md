# OmniRAG - Enterprise AI Operations Platform v2.0 (Capstone)

**Pitch:** Multi-tenant AI platform unifying CRM, Odoo, Parking, Medical, WhatsApp, NCERT with single RAG brain - RBAC, citations, analytics, $0 infra. Like Notion AI + Intercom + Odoo.

## Architecture
React (5173) -> Spring Boot (8080) -> PGVector enterprise_docs (HNSW) -> Ollama nomic-embed-text + llama3.1:8b

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
POST /api/ask-all {text}
GET /api/tables
GET /api/health
