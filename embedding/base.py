"""
input:
- texts: 文本或文本列表

output:
- List[List[float]]: 向量列表

pos:
- 位于 embedding 层基类定义
- 负责定义嵌入器接口契约

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from abc import ABC, abstractmethod
from typing import List


class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        pass
    
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        pass
