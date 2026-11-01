import psycopg2, json
from pgvector.psycopg2 import register_vector
from src.config.settings import settings

class VectorStoreService:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=settings.DB_NAME, user=settings.DB_USER,
            password=settings.DB_PASSWORD, host=settings.DB_HOST, port=settings.DB_PORT
        )
        # FIRST create extension, THEN register
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        self.conn.commit()
        
        # NOW register - vector type exists
        register_vector(self.conn)
        
        print(f"[VectorStore] Connected to {settings.DB_NAME}")

    def create_table(self, table_name: str, dim: int = 768):
        self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                meta JSONB,
                embedding vector({dim})
            );
        """)
        self.conn.commit()

    def truncate_table(self, table_name: str):
        try:
            self.cur.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY;")
            self.conn.commit()
        except Exception:
            self.conn.rollback()

    def insert_documents(self, table_name: str, docs):
        self.create_table(table_name, dim=settings.VECTOR_DIM)
        self.truncate_table(table_name)
        for doc in docs:
            self.cur.execute(
                f"INSERT INTO {table_name} (content, meta, embedding) VALUES (%s, %s, %s)",
                (doc.content, json.dumps(doc.meta), doc.embedding)
            )
        self.conn.commit()
        print(f"[OK] Inserted {len(docs)} into {table_name}")

    def close(self):
        self.cur.close()
        self.conn.close()