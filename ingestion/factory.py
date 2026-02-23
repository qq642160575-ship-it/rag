"""
input:
- file_path: 文档路径
- 后缀名: 自动提取

output:
- BaseParser: 对应格式的解析器实例

pos:
- 位于 ingestion 层
- 负责解析器分发，不负责具体解析逻辑

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from pathlib import Path

from ingestion.base import BaseParser
from ingestion.providers.pdf_handler import PDFHandler
from ingestion.providers.word_handler import WordHandler
from ingestion.providers.text_handler import TextHandler


class ParserFactory:
    _handlers = {
        ".pdf": PDFHandler,
        ".docx": WordHandler,
        ".doc": WordHandler,
        ".txt": TextHandler,
    }

    @classmethod
    def get_parser(cls, file_path: str) -> BaseParser:
        suffix = Path(file_path).suffix.lower()
        if suffix not in cls._handlers:
            raise ValueError(f"Unsupported file format: {suffix}")
        return cls._handlers[suffix]()

    @classmethod
    def register_handler(cls, suffix: str, handler_class: type) -> None:
        cls._handlers[suffix.lower()] = handler_class
