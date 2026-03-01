"""
输入:
- state: RAGState (状态对象)
- llm_handler: BaseLLMHandler (LLM 处理器)
- prompt_manager: PromptManager (提示词管理器)

输出:
- dict: {"task_type": ..., "entities": ...} (包含任务类型和实体的字典)

位置:
- 位于 agent/nodes 层
- 负责分析用户意图并提取关键实体

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from agent.core.rag_state import RAGState
from agent.core.intent import IntentOutput

def intent_node(state: RAGState, llm_handler, prompt_manager):
    # 在节点内部初始化结构化输出，或者从外部传入
    intent_llm = llm_handler.model.with_structured_output(IntentOutput)
    
    messages = prompt_manager.get_langchain_messages(
        "intent", 
        original_question=state["original_question"]
    )
    result = intent_llm.invoke(messages)
    return {
        "task_type": result.task_type,
        "entities": result.entities
    }
