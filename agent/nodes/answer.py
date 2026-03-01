"""
输入:
- state: RAGState (状态对象)
- llm_handler: BaseLLMHandler (LLM 处理器)
- prompt_manager: PromptManager (提示词管理器)

输出:
- dict: {"final_docs": List[Document], "answer": str} (最终参考文档和生成的回答)

位置:
- 位于 agent/nodes 层
- 终点节点，负责结合上下文生成最终回答

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from agent.core.rag_state import RAGState

def answer_node(state: RAGState, llm_handler, prompt_manager):
    docs_text = "\n\n".join([d.page_content for d in state["reranked_docs"]])
    messages = prompt_manager.get_langchain_messages(
        "answer",
        original_question=state["original_question"],
        docs_text=docs_text
    )
    answer = llm_handler.invoke(messages).content
    return {
        "final_docs": state["reranked_docs"],
        "answer": answer
    }
