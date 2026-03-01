"""
输入:
- state: RAGState (状态对象)
- llm_handler: BaseLLMHandler (LLM 处理器)
- prompt_manager: PromptManager (提示词管理器)

输出:
- dict: {"recall_score": float, "need_fallback": bool} (质量分数及是否需要回退的标识)

位置:
- 位于 agent/nodes 层
- 负责评估召回文档的质量，决定是否需要回退重写

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from agent.core.rag_state import RAGState
from agent.core.judge import RecallJudgeOutput

def judge_node(state: RAGState, llm_handler, prompt_manager):
    judge_llm = llm_handler.model.with_structured_output(RecallJudgeOutput)
    docs_text = "\n\n".join([d.page_content for d in state["reranked_docs"]])
    
    messages = prompt_manager.get_langchain_messages(
        "judge",
        original_question=state["original_question"],
        docs_text=docs_text
    )
    result = judge_llm.invoke(messages)
    return {
        "recall_score": result.score,
        "need_fallback": not result.sufficient
    }
