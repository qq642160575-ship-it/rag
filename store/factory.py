"""
input:
- provider: 存储接口类型 (如 faiss)
- **kwargs: 传递给构造函数的参数

output:
- BaseVectorStore: 具体的存储实例

pos:
- 位于 store 层工厂类
- 负责实例化具体的存储器

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from typing import Optional
from store.base import BaseVectorStore
from store.providers.faiss import FAISSVectorStore


class VectorStoreFactory:
    @staticmethod
    def get_vector_store(provider: str = "faiss", **kwargs) -> BaseVectorStore:
        """
        获取向量存储实例
        """
        provider = provider.lower()
        if provider == "faiss":
            return FAISSVectorStore(**kwargs)
        else:
            raise ValueError(f"Unsupported vector store provider: {provider}")
