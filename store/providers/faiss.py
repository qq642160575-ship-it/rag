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
import numpy as np
import faiss
import pickle
from typing import List, Dict, Any, Optional
from store.base import BaseVectorStore


class FAISSVectorStore(BaseVectorStore):
    def __init__(self, dimension: Optional[int] = None):
        self.dimension = dimension
        self.index = None
        self.documents = []
        self.metadatas = []
        
        if dimension:
            self.index = faiss.IndexFlatL2(dimension)

    def _init_index(self, dimension: int):
        if self.index is None:
            self.dimension = dimension
            self.index = faiss.IndexFlatL2(dimension)

    def add(
        self, 
        texts: List[str], 
        vectors: List[List[float]], 
        metadatas: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> List[str]:
        if not texts or not vectors:
            return []
            
        vectors_np = np.array(vectors).astype('float32')
        self._init_index(vectors_np.shape[1])
        
        self.index.add(vectors_np)
        self.documents.extend(texts)
        if metadatas:
            self.metadatas.extend(metadatas)
        else:
            self.metadatas.extend([{} for _ in texts])
            
        # 返回索引范围作为简单 ID
        start_idx = len(self.documents) - len(texts)
        return [str(i) for i in range(start_idx, len(self.documents))]

    def search(
        self, 
        query_vector: List[float], 
        top_k: int = 5, 
        **kwargs
    ) -> List[Dict[str, Any]]:
        if self.index is None:
            return []
            
        query_np = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_np, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1 or idx >= len(self.documents):
                continue
            results.append({
                "text": self.documents[idx],
                "score": float(distances[0][i]),
                "metadata": self.metadatas[idx] if idx < len(self.metadatas) else {}
            })
        return results

    def save(self, path: str = "./vector_store"):
        if not os.path.exists(path):
            os.makedirs(path)
            
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))
        with open(os.path.join(path, "data.pkl"), "wb") as f:
            pickle.dump({
                "documents": self.documents,
                "metadatas": self.metadatas,
                "dimension": self.dimension
            }, f)

    def load(self, path: str):
        self.index = faiss.read_index(os.path.join(path, "index.faiss"))
        with open(os.path.join(path, "data.pkl"), "rb") as f:
            data = pickle.load(f)
            self.documents = data["documents"]
            self.metadatas = data["metadatas"]
            self.dimension = data["dimension"]
