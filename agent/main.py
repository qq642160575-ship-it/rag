"""
输入:
- llm_handler: BaseLLMHandler (LLM 处理器)
- vector_store: BaseVectorStore (向量数据库对象)
- prompt_dir: str (提示词模板目录)
- embed_func: Optional[Callable] (可选的向量化函数)

输出:
- app: 编译后的 LangGraph 工作流应用

位置:
- 位于 agent 层
- 系统的总指挥部，负责组装所有节点并定义工作流拓扑

声明:
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录下 agent/README.md
"""

from typing import Literal, Any
from langgraph.graph import StateGraph, END

from llm.base import BaseLLMHandler
from llm.prompts.manager import PromptManager
from store.base import BaseVectorStore
from agent.core.rag_state import RAGState

# 导入节点实现
from agent.nodes.intent import intent_node
from agent.nodes.expand import expand_node
from agent.nodes.retrieval import retrieval_node
from agent.nodes.rerank import rerank_node
from agent.nodes.judge import judge_node
from agent.nodes.rewrite import rewrite_node
from agent.nodes.answer import answer_node

class StructuredRAGAgent:
    def __init__(self, llm_handler: BaseLLMHandler, vector_store: BaseVectorStore, prompt_dir: str, embed_func: Any = None):
        self.llm_handler = llm_handler
        self.vector_store = vector_store
        self.prompt_manager = PromptManager(prompt_dir)
        self.embed_func = embed_func
        
        # Build the graph
        self.app = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(RAGState)
        
        # Add nodes (using lambda to inject dependencies)
        workflow.add_node("intent", lambda state: intent_node(state, self.llm_handler, self.prompt_manager))
        workflow.add_node("expand", lambda state: expand_node(state, self.llm_handler, self.prompt_manager))
        workflow.add_node("retrieval", lambda state: retrieval_node(state, self.vector_store, self.embed_func))
        workflow.add_node("rerank", lambda state: rerank_node(state, self.llm_handler, self.prompt_manager))
        workflow.add_node("judge", lambda state: judge_node(state, self.llm_handler, self.prompt_manager))
        workflow.add_node("rewrite", lambda state: rewrite_node(state, self.llm_handler, self.prompt_manager))
        workflow.add_node("answer", lambda state: answer_node(state, self.llm_handler, self.prompt_manager))
        
        # Define edges
        workflow.set_entry_point("intent")
        workflow.add_edge("intent", "expand")
        workflow.add_edge("expand", "retrieval")
        workflow.add_edge("retrieval", "rerank")
        workflow.add_edge("rerank", "judge")
        
        def route(state: RAGState) -> Literal["answer", "rewrite"]:
            return "rewrite" if state["need_fallback"] else "answer"
            
        workflow.add_conditional_edges("judge", route)
        workflow.add_edge("rewrite", "retrieval")
        workflow.add_edge("answer", END)
        
        return workflow.compile()

    def invoke(self, question: str):
        return self.app.invoke({"original_question": question})
