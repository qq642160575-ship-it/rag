"""
input:
- file_path: Word 文件路径（.docx/.doc）

output:
- RawDocument: 统一文档数据模型

pos:
- 位于 ingestion/providers 层
- 负责 Word 解析，包装 LangChain Docx2txtLoader

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from ingestion.base import BaseParser
from core.schema import RawDocument
from langchain_community.document_loaders import Docx2txtLoader


class WordHandler(BaseParser):
    def parse(self, file_path: str) -> RawDocument:
        loader = Docx2txtLoader(file_path)
        documents = loader.load()
        content = "\n".join([doc.page_content for doc in documents])
        metadata = documents[0].metadata if documents else {}
        metadata["source"] = file_path
        return RawDocument(content=content, metadata=metadata)
