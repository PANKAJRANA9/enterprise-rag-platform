import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from src.services.embedding_service import EmbeddingService
from src.services.vector_store_service import VectorStoreService
from src.services.data_generator_service import DataGeneratorService
from src.models.document import Document
from src.config.settings import settings
from tqdm import tqdm

class IngestionPipeline:
    def __init__(self):
        self.embed_service = EmbeddingService(model=settings.EMBED_MODEL, base_url=settings.OLLAMA_URL)
        self.vector_store = VectorStoreService()
        self.data_gen = DataGeneratorService()

    def ingest_table(self, table_name: str, raw_data: list):
        print(f"\n--- Ingesting {table_name} ---")
        self.vector_store.create_table(table_name, dim=settings.VECTOR_DIM)
        self.vector_store.truncate_table(table_name)
        
        docs = []
        for item in tqdm(raw_data):
            emb = self.embed_service.embed_text(item['text'])
            docs.append(Document(content=item['text'], meta=item['meta'], embedding=emb))
        
        self.vector_store.insert_documents(table_name, docs)

    def run_all(self):
        self.ingest_table("odoo_docs", self.data_gen.get_odoo_data())
        self.ingest_table("crm_docs", self.data_gen.get_crm_data())
        self.ingest_table("parking_docs", self.data_gen.get_parking_data())
        self.ingest_table("medical_kb", self.data_gen.get_medical_data())
        self.ingest_table("whatsapp_docs", self.data_gen.get_whatsapp_data())
        print("\n✅ All tables ingested successfully!")
        self.vector_store.close()