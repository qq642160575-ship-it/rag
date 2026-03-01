from agent.core.rag_state import RAGState
from agent.nodes.intent import intent_node
from llm.factory import get_llm

state = RAGState
state.original_question = 'hello, i want to ask what is rag?'
llm = get_llm('anthropic', 'claude-sonnet-4.5')
intent_node(state, llm, 'intent')