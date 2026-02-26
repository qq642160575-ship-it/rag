# 供应商映射
_PROVIDER_CLASSES: Dict[str, str] = {
    "openai": "llm.providers.OpenAIHandler",
    "anthropic": "llm.providers.AnthropicHandler",
    "gemini": "llm.providers.GeminiHandler",
}

def _get_class(path: str):
    import importlib
    module_path, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

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
    provider_path = _PROVIDER_CLASSES.get(provider.lower())
    if not provider_path:
        raise ValueError(f"不支持的 LLM 供应商: {provider}. 可选: {list(_PROVIDER_CLASSES.keys())}")
    
    handler_class = _get_class(provider_path)
    return handler_class(model_name=model_name, **kwargs)
