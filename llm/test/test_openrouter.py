import os
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from llm.providers import OpenRouterHandler
from dotenv import load_dotenv

load_dotenv()

def test_openrouter():
    """测试 OpenRouter 处理器"""
    print("--- Testing OpenRouterHandler (Chat) ---")
    
    # 默认使用 gpt-3.5-turbo 或其他低成本模型进行测试
    model = "openai/gpt-3.5-turbo"
    print(f"Using model: {model}")
    
    try:
        handler = OpenRouterHandler(model_name=model)
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, who are you?"}
        ]
        
        # 测试聊天
        print("Sending chat request...")
        response = handler.chat(messages)
        print(f"Response: {response}")
        
        # 测试流式
        print("\n--- Testing OpenRouterHandler (Stream) ---")
        print("Sending stream request...")
        stream_content = ""
        for chunk in handler.stream(messages):
            print(chunk, end="", flush=True)
            stream_content += chunk
        print("\nStream completed.")
        
        if response and stream_content:
            print("\nTest PASSED!")
        else:
            print("\nTest FAILED: Empty response.")
            
    except Exception as e:
        print(f"\nTest FAILED with error: {e}")

if __name__ == "__main__":
    if not os.getenv("OPENROUTER_API_KEY"):
        print("CRITICAL: OPENROUTER_API_KEY not found in .env file.")
        sys.exit(1)
    test_openrouter()
