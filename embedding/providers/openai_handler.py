"""
input:
- texts: 文本列表

output:
- List[List[float]]: OpenAI 向量列表

pos:
- 位于 embedding/providers 层
- 负责调用 OpenAI Embeddings API

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from typing import List, Optional
from embedding.base import BaseEmbedder
from openai import OpenAI


class OpenAIEmbedder(BaseEmbedder):
    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [item.embedding for item in response.data]
    
    def embed_query(self, text: str) -> List[float]:
        return self.embed([text])[0]
