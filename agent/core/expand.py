"""
输入:
- pydantic.BaseModel

输出:
- ExpandOutput: 查询扩展输出模型

位置:
- 位于 agent/core 层
- 负责定义查询扩展的输出格式

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from typing import List
from pydantic import BaseModel

class ExpandOutput(BaseModel):
    queries: List[str]
