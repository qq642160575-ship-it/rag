import os
from unittest.mock import MagicMock
from langchain_core.documents import Document
from agent.structured_rag import StructuredRAGAgent
from dotenv import load_dotenv

load_dotenv()

# =========================
# Mock Objects for Testing
# =========================

def get_mock_agent():
    # Mock LLM Handler
    llm_handler = MagicMock()
    
    # Mock Structured Outputs
    mock_intent = MagicMock()
    mock_intent.invoke.return_value = MagicMock(task_type="Q&A", entities=["RAG", "LangGraph"])
    
    mock_expand = MagicMock()
    mock_expand.invoke.return_value = MagicMock(queries=["RAG architecture", "LangGraph agents"])
    
    mock_rerank = MagicMock()
    mock_rerank.invoke.return_value = MagicMock(score=0.9)
    
    mock_judge = MagicMock()
    mock_judge.invoke.return_value = MagicMock(score=0.95, sufficient=True)
    
    def side_effect(output_schema):
        name = output_schema.__name__
        if "Intent" in name: return mock_intent
        if "Expand" in name: return mock_expand
        if "Rerank" in name: return mock_rerank
        if "Judge" in name: return mock_judge
        return MagicMock()

    llm_handler.model.with_structured_output.side_effect = side_effect
    llm_handler.invoke.return_value = MagicMock(content="RAG is Retrieval-Augmented Generation. LangGraph is for workflows.")

    # Mock VectorStore (Project's BaseVectorStore interface)
    vector_store = MagicMock()
    # The search method should return a list of dicts
    vector_store.search.return_value = [
        {"text": "RAG (Retrieval-Augmented Generation) 是一种结合检索和生成的架构。", "metadata": {"source": "test1"}, "score": 0.1},
        {"text": "LangGraph 可以用于构建复杂的有状态 Agent 工作流。", "metadata": {"source": "test2"}, "score": 0.2}
    ]

    # Mock Embed function
    mock_embed_func = MagicMock(return_value=[0.1, 0.2, 0.3])

    prompt_dir = os.path.join(os.getcwd(), "llm", "prompts")
    return StructuredRAGAgent(llm_handler, vector_store, prompt_dir, embed_func=mock_embed_func)

def test_structured_rag_flow():
    print("--- Initializing Mock Agent (Internal Store Interface) ---")
    agent = get_mock_agent()

    print("\n--- Running Agent Workflow ---")
    question = "什么是 RAG 和 LangGraph？"
    
    try:
        result = agent.invoke(question)
        print("\n--- Final Answer ---")
        print(result["answer"])
        print("\n--- State Variables ---")
        print(f"Task Type: {result.get('task_type')}")
        print(f"Entities: {result.get('entities')}")
        print(f"Recall Score: {result.get('recall_score')}")
        print(f"Reranked Docs Count: {len(result.get('reranked_docs', []))}")
        
        # Verify internal store search was called
        print(f"\n--- Verification ---")
        print(f"Vector store search called: {agent.vector_store.search.called}")
        print(f"Embed func called: {agent.embed_func.called}")
        
    except Exception as e:
        print(f"Error during agent execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_structured_rag_flow()
