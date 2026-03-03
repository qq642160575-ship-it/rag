"""
输入:
- state: RAGState (状态对象)
- llm_handler: BaseLLMHandler (LLM 处理器)
- prompt_manager: PromptManager (提示词管理器)

输出:
- dict: {"task_type": ..., "need_retrieval": ..., "expanded_queries": ..., "risk_level": ...}

位置:
- 位于 agent/nodes 层
- 整合了之前的意图分析 (intent) 与查询扩展 (expand) 节点，一次性完成语义理解

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""

from agent.core.rag_state import RAGState
from agent.core.understanding import UnderstandingOutput
from llm.base import DebugHandler

def understanding_node(state: RAGState, llm_handler, prompt_manager):
    # 初始化结构化输出 LLM
    understanding_llm = llm_handler.model.with_structured_output(UnderstandingOutput)
    
    # 使用整合的 prompt (假设 prompt 名为 understanding)
    # 如果暂无 understanding prompt，建议合并 intent 和 expand 的 prompt 内容
    messages = prompt_manager.get_langchain_messages(
        "understanding", 
        original_question=state["original_question"]
    )
    
    result = understanding_llm.invoke(messages, config={"callbacks": [DebugHandler()]})
    
    return {
        "task_type": result.task_type,
        "need_retrieval": result.need_retrieval,
        "expanded_queries": result.expanded_queries,
        "risk_level": result.risk_level
    }
