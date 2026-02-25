import os
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from llm.providers import AnthropicHandler, OpenAIHandler, GeminiHandler
from dotenv import load_dotenv

load_dotenv()

def test_provider(handler_class, name, model_name, api_key_env):
    """通用测试函数"""
    print(f"\n{'='*20} Testing {name} ({model_name}) {'='*20}")
    
    if not os.getenv(api_key_env):
        print(f"SKIP: {api_key_env} not found in .env file.")
        return

    try:
        handler = handler_class(model_name=model_name)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Just say 'OK' if you can hear me."}
        ]
        
        # 测试聊天
        print(f"Testing {name} chat...")
        response = handler.chat(messages)
        print(f"Response: {response}")
        
        # 测试流式
        print(f"Testing {name} stream...")
        stream_content = ""
        for chunk in handler.stream(messages):
            print(chunk, end="", flush=True)
            stream_content += chunk
        print("\nStream completed.")
        
        if response and stream_content:
            print(f"SUCCESS: {name} test PASSED!")
        else:
            print(f"FAILURE: {name} test FAILED (empty response).")
            
    except Exception as e:
        print(f"ERROR: {name} test FAILED with error: {e}")

if __name__ == "__main__":
    # 测试 OpenAI
    test_provider(OpenAIHandler, "OpenAI", "gpt-4o-mini", "OPENAI_API_KEY")
    
    # 测试 Anthropic
    test_provider(AnthropicHandler, "Anthropic", "claude-3-haiku-20240307", "ANTHROPIC_API_KEY")
    
    # 测试 Gemini
    test_provider(GeminiHandler, "Gemini", "gemini-1.5-flash", "GOOGLE_API_KEY")
