"""
输入:
- state: RAGState (状态对象)
- llm_handler: BaseLLMHandler (LLM 处理器)
- prompt_manager: PromptManager (提示词管理器)

输出:
- dict: {"rewritten_query": str, "expanded_queries": List[str]} (重写后的查询)

位置:
- 位于 agent/nodes 层
- 负责在初始检索质量不佳时，对原始问题进行多角度重写

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from agent.core.rag_state import RAGState

def rewrite_node(state: RAGState, llm_handler, prompt_manager):
    messages = prompt_manager.get_langchain_messages(
        "rewrite",
        original_question=state["original_question"]
    )
    rewritten = llm_handler.invoke(messages).content.strip()
    return {
        "rewritten_query": rewritten,
        "expanded_queries": [rewritten]
    }
