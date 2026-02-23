"""
input:
- texts: 文本列表

output:
- List[List[float]]: 本地模型向量列表

pos:
- 位于 embedding/providers 层
- 负责调用本地 sentence-transformers 模型

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from typing import List
from embedding.base import BaseEmbedder


class LocalEmbedder(BaseEmbedder):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        return self.embed([text])[0]
