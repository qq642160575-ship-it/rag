"""
input:
- file_path: 文档路径

output:
- RawDocument: 统一文档数据模型

pos:
- 位于 ingestion 层基类定义
- 负责定义解析器接口契约

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from abc import ABC, abstractmethod
from core.schema import RawDocument


class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> RawDocument:
        pass
