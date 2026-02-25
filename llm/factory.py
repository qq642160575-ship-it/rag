from typing import Any, Dict, Type
from llm.base import BaseLLMHandler
from llm.providers import AnthropicHandler, OpenAIHandler, GeminiHandler

# 供应商映射
PROVIDER_MAP: Dict[str, Type[BaseLLMHandler]] = {
    "openai": OpenAIHandler,
    "anthropic": AnthropicHandler,
    "gemini": GeminiHandler,
}

def get_llm(provider: str, model_name: str, **kwargs: Any) -> BaseLLMHandler:
    """
    LLM 处理器工厂函数。
    
    Args:
        provider: 供应商名称 ('openai', 'anthropic', 'gemini')
        model_name: 模型名称
        **kwargs: 传给构造函数的参数（如 temperature）
        
    Returns:
        相应的 BaseLLMHandler 子类实例
    """
    handler_class = PROVIDER_MAP.get(provider.lower())
    if not handler_class:
        raise ValueError(f"不支持的 LLM 供应商: {provider}. 可选: {list(PROVIDER_MAP.keys())}")
    
    return handler_class(model_name=model_name, **kwargs)
