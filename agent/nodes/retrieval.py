"""
输入:
- state: RAGState (状态对象)
- vector_store: BaseVectorStore (向量数据库对象)
- embed_func: Optional[Callable] (可选的向量化函数)

输出:
- dict: {"merged_docs": List[Document]} (去重后的文档列表)

位置:
- 位于 agent/nodes 层
- 负责向量检索、结果合并与基础去重

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from typing import List
from langchain_core.documents import Document
from agent.core.rag_state import RAGState

def retrieval_node(state: RAGState, vector_store, embed_func=None):
    results = []
    for q in state["expanded_queries"]:
        if embed_func:
            query_vector = embed_func(q)
            search_results = vector_store.search(query_vector, top_k=3)
            docs = [
                Document(
                    page_content=r["text"], 
                    metadata=r.get("metadata", {})
                ) for r in search_results
            ]
        elif hasattr(vector_store, "similarity_search"):
            docs = vector_store.similarity_search(q, k=3)
        else:
            raise ValueError("Vector store requires an embed_func or similarity_search method.")
        
        results.extend(docs)
    
    # Merge and deduplicate
    unique = {}
    for doc in results:
        unique[doc.page_content] = doc
        
    return {"merged_docs": list(unique.values())}
