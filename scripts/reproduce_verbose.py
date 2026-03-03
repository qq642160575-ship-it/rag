import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.callbacks import StdOutCallbackHandler
import langchain
from pydantic import BaseModel, Field
from typing import List

# Load .env
load_dotenv()

class IntentOutput(BaseModel):
    task_type: str = Field(description="任务类型")
    entities: List[str] = Field(description="提取的实体")

def test_verbose():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    base_url = os.getenv("ANTHROPIC_BASE_URL")
    
    print(f"IS_PRO: {os.getenv('IS_PRO')}")
    
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        anthropic_api_key=api_key,
        anthropic_api_url=base_url,
    )

    print("\n--- Testing with StdOutCallbackHandler ---")
    messages = [HumanMessage(content="Hello, what is RAG?")]
    llm.invoke(messages, config={"callbacks": [StdOutCallbackHandler()]})

    print("\n--- Testing with langchain.debug = True ---")
    langchain.debug = True
    llm.invoke(messages)
    langchain.debug = False

    print("\n--- Testing with_structured_output and StdOutCallbackHandler ---")
    structured_llm = llm.with_structured_output(IntentOutput)
    structured_llm.invoke(messages, config={"callbacks": [StdOutCallbackHandler()]})

if __name__ == "__main__":
    test_verbose()
