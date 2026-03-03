import os

from agent.core.rag_state import RAGState
from agent.nodes.intent import intent_node
from llm.factory import get_llm
from llm.prompts.manager import PromptManager

import langchain
langchain.debug = True
state = RAGState()
state['original_question'] = 'hello, i want to ask what is rag?'
llm = get_llm('anthropic', 'claude-sonnet-4.5')
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
prompt_path = BASE_DIR / 'llm' / 'prompts'
# print(prompt_path)

prompt_manager = PromptManager(prompt_path)
intent_node(state, llm, prompt_manager)