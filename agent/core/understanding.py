"""
input:
- pydantic.BaseModel
- typing.List

output:
- UnderstandingOutput: 语义理解综合输出模型

pos:
- 位于 agent/core 层
- 负责整合意图识别、检索判定与查询扩展的输出格式

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from typing import List
from pydantic import BaseModel, Field

class UnderstandingOutput(BaseModel):
    """
    语义理解综合输出格式
    """
    task_type: str = Field(
        ..., 
        description='任务意图分类 (例如: search, chitchat, compare)'
    )
    need_retrieval: bool = Field(
        ..., 
        description='根据意图判断是否需要执行知识库检索'
    )
    expanded_queries: List[str] = Field(
        default_factory=list, 
        description='生成的多个改写查询列表，用于扩大召回范围'
    )
    risk_level: str = Field(
        default='low', 
        description='安全合规风险等级 (low, medium, high)'
    )
