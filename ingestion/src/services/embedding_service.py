import ollama
from typing import List

class EmbeddingService:
    def __init__(self, model: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        self.model = model
        self.client = ollama.Client(host=base_url)
        print(f"[EmbeddingService] Using Ollama model: {self.model} at {base_url}")

    def embed_text(self, text: str) -> List[float]:
        try:
            resp = self.client.embeddings(model=self.model, prompt=text)
            return resp['embedding']
        except Exception as e:
            print(f"Embedding failed: {e}")
            raise

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]