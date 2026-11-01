import sys
from pathlib import Path

# FIX: Add ingestion folder to Python path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from src.pipeline.ingestion_pipeline import IngestionPipeline
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enterprise RAG Ingestion")
    parser.add_argument("--table", type=str, help="Table name: crm_docs/odoo_docs/parking_docs/medical_kb/whatsapp_docs or all")
    args = parser.parse_args()

    pipeline = IngestionPipeline()
    
    if args.table:
        data_map = {
            "odoo_docs": pipeline.data_gen.get_odoo_data(),
            "crm_docs": pipeline.data_gen.get_crm_data(),
            "parking_docs": pipeline.data_gen.get_parking_data(),
            "medical_kb": pipeline.data_gen.get_medical_data(),
            "whatsapp_docs": pipeline.data_gen.get_whatsapp_data(),
        }
        if args.table in data_map:
            pipeline.ingest_table(args.table, data_map[args.table])
            pipeline.vector_store.close()
            print(f"Done {args.table}")
        else:
            print(f"Unknown table {args.table}. Choose from {list(data_map.keys())}")
    else:
        pipeline.run_all()