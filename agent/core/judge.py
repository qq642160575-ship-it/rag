"""
输入:
- pydantic.BaseModel

输出:
- RecallJudgeOutput: 召回判定输出模型

位置:
- 位于 agent/core 层
- 负责定义召回质量判定的输出格式

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from pydantic import BaseModel, Field

class RecallJudgeOutput(BaseModel):
    score: float = Field(
        default=0.0, 
        description='召回内容与问题的相关性评分 (0.0-1.0)'
    )
    sufficient: bool = Field(
        default=False, 
        description='当前召回的内容是否足以回答用户问题'
    )
