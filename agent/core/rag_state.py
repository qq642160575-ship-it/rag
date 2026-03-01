"""
输入:
- typing.TypedDict
- langchain_core.documents.Document

输出:
- RAGState: LangGraph 的核心状态类

位置:
- 位于 agent/core 层
- 统一维护 Agent 的全局状态流转格式

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from typing import TypedDict, List
from langchain_core.documents import Document

class RAGState(TypedDict):
    original_question: str
    
    # Intent analysis
    task_type: str
    entities: List[str]
    
    # Retrieval
    expanded_queries: List[str]
    dense_results: List[Document]
    merged_docs: List[Document]
    reranked_docs: List[Document]
    
    # Quality control
    recall_score: float
    need_fallback: bool
    
    # Fallback/Rewrite
    rewritten_query: str
    
    # Output
    final_docs: List[Document]
    answer: str
