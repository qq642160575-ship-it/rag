"""
输入:
- state: RAGState (状态对象)
- llm_handler: BaseLLMHandler (LLM 处理器)
- prompt_manager: PromptManager (提示词管理器)

输出:
- dict: {"reranked_docs": List[Document]} (重排后的高质量文档列表)

位置:
- 位于 agent/nodes 层
- 负责对召回文档进行相关性精排

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from agent.core.rag_state import RAGState
from agent.core.rerank import RerankScoreOutput

def rerank_node(state: RAGState, llm_handler, prompt_manager):
    rerank_llm = llm_handler.model.with_structured_output(RerankScoreOutput)
    scored = []
    
    for doc in state["merged_docs"]:
        messages = prompt_manager.get_langchain_messages(
            "rerank",
            original_question=state["original_question"],
            doc_content=doc.page_content
        )
        result = rerank_llm.invoke(messages)
        scored.append((result.score, doc))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    return {"reranked_docs": [d for _, d in scored[:5]]}
