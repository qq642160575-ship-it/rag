"""
input:
- texts: 文本列表
- vectors: 向量列表
- metadatas: 字典列表 (可选)

output:
- search_results: 搜索结果列表

pos:
- 位于 store/providers 目录下
- 实现 FAISS 向量存储及其持久化逻辑

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
import os
import shutil
from typing import List, Dict, Any, Optional
from store.base import BaseVectorStore
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings


class FakeEmbeddings(Embeddings):
    """一个不执行任何操作的嵌入类，因为我们直接传入向量"""
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return []
    def embed_query(self, text: str) -> List[float]:
        return []


class FAISSVectorStore(BaseVectorStore):
    def __init__(self, dimension: Optional[int] = None):
        self.dimension = dimension
        self.vector_store: Optional[FAISS] = None
        self.embeddings = FakeEmbeddings()

    def add(
        self, 
        texts: List[str], 
        vectors: List[List[float]], 
        metadatas: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> List[str]:
        if not texts or not vectors:
            return []
            
        # 构造文本与向量的对应关系
        text_embeddings = list(zip(texts, vectors))
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_embeddings(
                text_embeddings=text_embeddings,
                embedding=self.embeddings,
                metadatas=metadatas
            )
        else:
            self.vector_store.add_embeddings(
                text_embeddings=text_embeddings,
                metadatas=metadatas
            )
            
        return [str(i) for i in range(len(texts))]

    def search(
        self, 
        query_vector: List[float], 
        top_k: int = 5, 
        filter: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        if self.vector_store is None:
            return []
            
        # 使用 LangChain 的 similarity_search_by_vector
        # 它支持 filter 参数进行元数据过滤
        docs_with_score = self.vector_store.similarity_search_by_vector(
            embedding=query_vector,
            k=top_k,
            filter=filter
        )
        
        results = []
        for doc in docs_with_score:
            results.append({
                "text": doc.page_content,
                "score": 0.0,  # LangChain 的这个接口某些版本不直接返回分数，如果需要分数可用 similarity_search_with_score_by_vector
                "metadata": doc.metadata
            })
        return results

    def save(self, path: str = "./vector_store"):
        if self.vector_store:
            self.vector_store.save_local(path)

    def load(self, path: str):
        self.vector_store = FAISS.load_local(
            path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
