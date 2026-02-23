"""
input:
- 无

output:
- RawDocument: 统一文档数据模型

pos:
- 位于 core 层
- 负责数据结构定义，不负责业务逻辑

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
import datetime
from datetime import datetime as dt, timezone
from typing import Any, Dict
import uuid
from langchain_core.documents import Document
from pydantic import BaseModel, Field


class RawDocument(BaseModel):
    """
    统一的文档中的格式
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="文档唯一标识")
    content: str = Field(..., description="提取出来的文本内容")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="文档的元信息，如来源、作者等")
    created_datetime: dt = Field(default_factory=lambda: dt.now(timezone.utc), description="文档创建时间")


    def to_langchain_document(self) -> Document:
        """
        转换为 langchain 的 Document 对象
        """
        return Document(
            page_content=self.content,
            metadata=self.metadata
        )