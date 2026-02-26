import os
from typing import TypedDict, List, Literal, Dict, Any
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_core.documents import Document
from llm.base import BaseLLMHandler
from llm.prompts.manager import PromptManager
from store.base import BaseVectorStore


# =========================
# 强类型输出定义 (Pydantic Models)
# =========================

class IntentOutput(BaseModel):
    task_type: str
    entities: List[str]


class ExpandOutput(BaseModel):
    queries: List[str]


class RecallJudgeOutput(BaseModel):
    score: float
    sufficient: bool


class RerankScoreOutput(BaseModel):
    score: float


# =========================
# Graph State
# =========================

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


class StructuredRAGAgent:
    def __init__(self, llm_handler: BaseLLMHandler, vector_store: BaseVectorStore, prompt_dir: str, embed_func: Any = None):
        self.llm_handler = llm_handler
        self.vector_store = vector_store
        self.prompt_manager = PromptManager(prompt_dir)
        self.embed_func = embed_func
        
        # Initialize structured LLM outputs
        self.intent_llm = self.llm_handler.model.with_structured_output(IntentOutput)
        self.expand_llm = self.llm_handler.model.with_structured_output(ExpandOutput)
        self.rerank_llm = self.llm_handler.model.with_structured_output(RerankScoreOutput)
        self.judge_llm = self.llm_handler.model.with_structured_output(RecallJudgeOutput)
        
        # Build the graph
        self.app = self._build_graph()

    # =========================
    # Nodes
    # =========================

    def intent_node(self, state: RAGState):
        messages = self.prompt_manager.get_langchain_messages(
            "intent", 
            original_question=state["original_question"]
        )
        result = self.intent_llm.invoke(messages)
        return {
            "task_type": result.task_type,
            "entities": result.entities
        }

    def expand_node(self, state: RAGState):
        messages = self.prompt_manager.get_langchain_messages(
            "expand",
            original_question=state["original_question"],
            entities=", ".join(state["entities"])
        )
        result = self.expand_llm.invoke(messages)
        return {"expanded_queries": result.queries}

    def dense_node(self, state: RAGState):
        results = []
        for q in state["expanded_queries"]:
            # 使用项目定义的 BaseVectorStore 接口进行检索
            # 如果提供了 embed_func，则先将文本转为向量
            if self.embed_func:
                query_vector = self.embed_func(q)
                search_results = self.vector_store.search(query_vector, top_k=3)
                
                # 将项目自定义的搜索结果格式转换为 LangChain Document 格式以便后续处理
                docs = [
                    Document(
                        page_content=r["text"], 
                        metadata=r.get("metadata", {})
                    ) for r in search_results
                ]
            elif hasattr(self.vector_store, "similarity_search"):
                # 兼容旧的 LangChain 风格接口（如果有的话）
                docs = self.vector_store.similarity_search(q, k=3)
            else:
                raise ValueError("Vector store requires an embed_func or similarity_search method.")
            
            results.extend(docs)
        
        return {"dense_results": results}

    def merge_node(self, state: RAGState):
        unique = {}
        for doc in state["dense_results"]:
            unique[doc.page_content] = doc
        return {"merged_docs": list(unique.values())}

    def rerank_node(self, state: RAGState):
        scored = []
        for doc in state["merged_docs"]:
            messages = self.prompt_manager.get_langchain_messages(
                "rerank",
                original_question=state["original_question"],
                doc_content=doc.page_content
            )
            result = self.rerank_llm.invoke(messages)
            scored.append((result.score, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return {"reranked_docs": [d for _, d in scored[:5]]}

    def judge_node(self, state: RAGState):
        docs_text = "\n\n".join([d.page_content for d in state["reranked_docs"]])
        messages = self.prompt_manager.get_langchain_messages(
            "judge",
            original_question=state["original_question"],
            docs_text=docs_text
        )
        result = self.judge_llm.invoke(messages)
        return {
            "recall_score": result.score,
            "need_fallback": not result.sufficient
        }

    def rewrite_node(self, state: RAGState):
        messages = self.prompt_manager.get_langchain_messages(
            "rewrite",
            original_question=state["original_question"]
        )
        rewritten = self.llm_handler.invoke(messages).content.strip()
        return {
            "rewritten_query": rewritten,
            "expanded_queries": [rewritten]
        }

    def answer_node(self, state: RAGState):
        docs_text = "\n\n".join([d.page_content for d in state["reranked_docs"]])
        messages = self.prompt_manager.get_langchain_messages(
            "answer",
            original_question=state["original_question"],
            docs_text=docs_text
        )
        answer = self.llm_handler.invoke(messages).content
        return {
            "final_docs": state["reranked_docs"],
            "answer": answer
        }

    # =========================
    # Graph Construction
    # =========================

    def _build_graph(self):
        workflow = StateGraph(RAGState)
        
        # Add nodes
        workflow.add_node("intent", self.intent_node)
        workflow.add_node("expand", self.expand_node)
        workflow.add_node("dense", self.dense_node)
        workflow.add_node("merge", self.merge_node)
        workflow.add_node("rerank", self.rerank_node)
        workflow.add_node("judge", self.judge_node)
        workflow.add_node("rewrite", self.rewrite_node)
        workflow.add_node("answer", self.answer_node)
        
        # Build edges
        workflow.set_entry_point("intent")
        workflow.add_edge("intent", "expand")
        workflow.add_edge("expand", "dense")
        workflow.add_edge("dense", "merge")
        workflow.add_edge("merge", "rerank")
        workflow.add_edge("rerank", "judge")
        
        def route(state: RAGState) -> Literal["answer", "rewrite"]:
            return "rewrite" if state["need_fallback"] else "answer"
            
        workflow.add_conditional_edges("judge", route)
        workflow.add_edge("rewrite", "dense")
        workflow.add_edge("answer", END)
        
        return workflow.compile()

    def invoke(self, question: str):
        return self.app.invoke({"original_question": question})
