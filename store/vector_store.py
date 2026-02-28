"""
input:
- texts: 文本列表
- vectors: 向量列表
- query_vector: 查询向量
- path: 持久化路径

output:
- search_results: 检索出的文档列表

pos:
- 位于 store 层对外唯一入口
- 负责屏蔽底层存储细节

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from typing import List, Dict, Any, Optional, Union
from store.factory import VectorStoreFactory


# 全局单例缓存（可选，通常建议由上层业务控制生命周期）
_instances = {}


def get_store(provider: str = "faiss", **kwargs):
    """
    获取或创建一个存储实例。
    注意：这里的 kwargs 应该是初始化参数（如 dimension）。
    """
    # 过滤掉非初始化参数（可选，但目前为了兼容性，我们通过 key 来区分）
    instance_key = f"{provider}_{str(kwargs)}"
    if instance_key not in _instances:
        _instances[instance_key] = VectorStoreFactory.get_vector_store(provider, **kwargs)
    return _instances[instance_key]


def add(
    texts: List[str], 
    vectors: List[List[float]], 
    metadatas: Optional[List[Dict[str, Any]]] = None,
    provider: str = "faiss",
    **kwargs
) -> List[str]:
    """快捷添加接口"""
    # 实例化时不带 runtime 参数
    store = get_store(provider)
    return store.add(texts, vectors, metadatas, **kwargs)


def search(
    query_vector: List[float], 
    top_k: int = 5, 
    provider: str = "faiss",
    **kwargs
) -> List[Dict[str, Any]]:
    """快捷检索接口"""
    # 核心修正：get_store 不要拿走包含 filter 的 kwargs
    store = get_store(provider)
    return store.search(query_vector, top_k, **kwargs)


def save(path: str, provider: str = "faiss", **kwargs):
    """持久化存储"""
    store = get_store(provider, **kwargs)
    store.save(path)


def load(path: str, provider: str = "faiss", **kwargs):
    """从本地加载"""
    store = get_store(provider, **kwargs)
    store.load(path)
