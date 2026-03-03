import os
from pathlib import Path
from agent.core.rag_state import RAGState
from agent.nodes.intent import intent_node
from llm.factory import get_llm
from llm.prompts.manager import PromptManager
from dotenv import load_dotenv

# Load .env
load_dotenv()

def verify_fix():
    print("Starting verification of LLM debug fix...")
    
    # Initialize state
    state = RAGState()
    state["original_question"] = 'hello, i want to ask what is rag?'
    
    # Initialize LLM (this should trigger langchain.debug = True)
    llm = get_llm('anthropic', 'claude-3-5-sonnet-20240620')
    
    # Initialize PromptManager
    BASE_DIR = Path(__file__).resolve().parent.parent
    prompt_path = BASE_DIR / 'llm' / 'prompts'
    prompt_manager = PromptManager(prompt_path)
    
    print("\n--- Calling intent_node (this should show debug output) ---")
    result = intent_node(state, llm, prompt_manager)
    print("\n--- Result ---")
    print(result)

if __name__ == "__main__":
    verify_fix()
