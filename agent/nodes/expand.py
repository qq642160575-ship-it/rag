"""
输入:
- state: RAGState (状态对象)
- llm_handler: BaseLLMHandler (LLM 处理器)
- prompt_manager: PromptManager (提示词管理器)

输出:
- dict: {"expanded_queries": List[str]} (扩展后的查询列表)

位置:
- 位于 agent/nodes 层
- 负责基于问题和实体进行多维度查询扩展

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from agent.core.rag_state import RAGState
from agent.core.expand import ExpandOutput

def expand_node(state: RAGState, llm_handler, prompt_manager):
    expand_llm = llm_handler.model.with_structured_output(ExpandOutput)
    
    messages = prompt_manager.get_langchain_messages(
        "expand",
        original_question=state["original_question"],
        entities=", ".join(state["entities"])
    )
    result = expand_llm.invoke(messages)
    return {"expanded_queries": result.queries}
