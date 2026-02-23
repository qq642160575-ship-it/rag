"""
input:
- texts: 文本或文本列表
- provider: 嵌入器类型
- model: 模型名称

output:
- List[List[float]]: 向量列表

pos:
- 位于 embedding 层对外唯一入口
- 负责文本向量化

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from typing import List, Union, Optional
from embedding.factory import EmbedderFactory


def embed(
    texts: Union[str, List[str]],
    provider: str = "openai",
    model: Optional[str] = None,
    **kwargs
) -> Union[List[float], List[List[float]]]:
    """
    统一嵌入入口：文本 → 向量
    
    Args:
        texts: 单个文本或文本列表
        provider: 嵌入器类型
        model: 模型名称
        **kwargs: 传递给嵌入器的额外参数
    
    Returns:
        单向量或向量列表
    """
    embedder = EmbedderFactory.get_embedder(provider=provider, model=model, **kwargs)
    
    is_single = isinstance(texts, str)
    text_list = [texts] if is_single else texts
    
    embeddings = embedder.embed(text_list)
    
    return embeddings[0] if is_single else embeddings


def embed_query(
    text: str,
    provider: str = "openai",
    model: Optional[str] = None,
    **kwargs
) -> List[float]:
    """
    查询文本嵌入（单文本）
    """
    embedder = EmbedderFactory.get_embedder(provider=provider, model=model, **kwargs)
    return embedder.embed_query(text)
