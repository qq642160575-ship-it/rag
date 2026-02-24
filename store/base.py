"""
input:
- texts: 文本列表
- vectors: 向量列表
- query_vector: 查询向量
- path: 持久化路径

output:
- various: 接口定义

pos:
- 位于 store 层基类定义
- 负责定义向量存储接口契约

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union


class BaseVectorStore(ABC):
    @abstractmethod
    def add(
        self, 
        texts: List[str], 
        vectors: List[List[float]], 
        metadatas: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> List[str]:
        """
        向向量空间添加数据
        
        Args:
            texts: 原始文本内容
            vectors: 对应的向量列表
            metadatas: 对应的元数据
            
        Returns:
            添加成功的 ID 列表
        """
        pass

    @abstractmethod
    def search(
        self, 
        query_vector: List[float], 
        top_k: int = 5, 
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        相似性检索
        
        Args:
            query_vector: 查询向量
            top_k: 返回最相似的前 K 个结果
            
        Returns:
            搜索结果列表，包含文本、得分和元数据
        """
        pass

    @abstractmethod
    def save(self, path: str):
        """持久化存储"""
        pass

    @abstractmethod
    def load(self, path: str):
        """从本地加载"""
        pass
