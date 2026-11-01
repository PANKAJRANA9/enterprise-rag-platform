from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class Document:
    content: str
    meta: Dict[str, Any]
    embedding: List[float] = None

    def to_dict(self):
        return {"content": self.content, "meta": self.meta}