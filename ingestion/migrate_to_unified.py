import psycopg2

conn = psycopg2.connect(dbname="pinecone_db", user="postgres", password="secret123", host="localhost", port=5433)
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
conn.commit()

cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS enterprise_docs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(768)
);
""")
conn.commit()
print("enterprise_docs ready")

tables = ["crm_docs","odoo_docs","parking_docs","medical_kb","whatsapp_docs","ncert_docs"]
for table in tables:
    cur.execute("SELECT to_regclass(%s);", (f"public.{table}",))
    exists = cur.fetchone()[0]
    if not exists:
        print(f"SKIP {table} - not exists")
        continue
    
    cur.execute(f"SELECT COUNT(*) FROM {table};")
    count = cur.fetchone()[0]
    print(f"{table}: {count} rows")
    if count == 0:
        continue
    
    # FIXED: Don't read old metadata column, just create new one with source
    cur.execute(f"""
        INSERT INTO enterprise_docs (content, metadata, embedding)
        SELECT content, jsonb_build_object('source', %s)::jsonb, embedding FROM {table}
        ON CONFLICT DO NOTHING;
    """, (table,))
    conn.commit()
    print(f" -> Migrated {table}")

cur.execute("CREATE INDEX IF NOT EXISTS idx_enterprise_docs_embedding ON enterprise_docs USING hnsw (embedding vector_cosine_ops);")
conn.commit()

cur.execute("SELECT metadata->>'source' as source, COUNT(*) FROM enterprise_docs GROUP BY 1;")
print("Final counts:")
for r in cur.fetchall():
    print(r)

cur.close()
conn.close()
print("✅ DONE")