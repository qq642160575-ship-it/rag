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

from pydantic import BaseModel

class RecallJudgeOutput(BaseModel):
    score: float
    sufficient: bool
