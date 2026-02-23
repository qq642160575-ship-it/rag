"""
input:
- provider: 嵌入器类型

output:
- BaseEmbedder: 对应类型的嵌入器实例

pos:
- 位于 embedding 层
- 负责嵌入器分发，不负责具体嵌入逻辑

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from typing import Optional
from embedding.base import BaseEmbedder
from embedding.providers.openai_handler import OpenAIEmbedder
from embedding.providers.local_handler import LocalEmbedder


class EmbedderFactory:
    _providers = {
        "openai": OpenAIEmbedder,
        "local": LocalEmbedder,
    }
    
    _default_provider = "openai"
    _default_model = {
        "openai": "text-embedding-3-small",
        "local": "sentence-transformers/all-MiniLM-L6-v2"
    }
    
    @classmethod
    def get_embedder(
        cls,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> BaseEmbedder:
        provider = provider or cls._default_provider
        if provider not in cls._providers:
            raise ValueError(f"Unsupported provider: {provider}")
        
        model = model or cls._default_model.get(provider)
        embedder_class = cls._providers[provider]
        
        if provider == "openai":
            return embedder_class(model=model, **kwargs)
        else:
            return embedder_class(model_name=model, **kwargs)
    
    @classmethod
    def register_provider(cls, name: str, embedder_class: type) -> None:
        cls._providers[name] = embedder_class
