"""
input:
- file_path: PDF 文件路径

output:
- RawDocument: 统一文档数据模型

pos:
- 位于 ingestion/providers 层
- 负责 PDF 解析，包装 LangChain PyPDFLoader

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from ingestion.base import BaseParser
from core.schema import RawDocument
from langchain_community.document_loaders import PyPDFLoader


class PDFHandler(BaseParser):
    def parse(self, file_path: str) -> RawDocument:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        content = "\n".join([doc.page_content for doc in documents])
        # 将 LangChain 文档的第一个元数据作为基础元数据，并添加 source
        metadata = documents[0].metadata if documents else {}
        metadata["source"] = file_path
        return RawDocument(content=content, metadata=metadata)
