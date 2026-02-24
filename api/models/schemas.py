"""
input:
- 基础请求数据

output:
- Pydantic 模型类

pos:
- 位于 api/models 层
- 负责定义 API 输入输出的数据规范

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class BaseBatchResponse(BaseModel):
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="结果消息")


class IngestResponse(BaseBatchResponse):
    ids: List[str] = Field(default_factory=list, description="生成的数据块 ID 列表")
    count: int = Field(0, description="处理的块数量")


class ErrorResponse(BaseModel):
    error_code: str = Field(..., description="错误码")
    error_message: str = Field(..., description="错误详细信息")
