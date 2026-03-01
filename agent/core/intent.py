"""
输入:
- pydantic.BaseModel
- typing_extensions.Literal

输出:
- IntentOutput: 意图分析输出模型

位置:
- 位于 agent/core 层
- 负责定义意图分析的强类型输出格式

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from typing_extensions import Literal

class IntentOutput(BaseModel):
    """
    固定意图输出格式
    """
    task_type: Literal['search', 'summary', 'compare', 'chitchat']
    entities: List[str]
    filters: Optional[Dict[str, Any]] = None
    reason: str
