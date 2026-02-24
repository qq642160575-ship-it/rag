"""
input:
- file_path: 文档路径
- store_path: 向量存储持久化路径
- embed_provider: 嵌入服务商
- store_provider: 向量存储引擎

output:
- List[str]: 添加成功的块 ID 列表

pos:
- 位于 pipeline 层
- 负责协调 ingestion -> embedding -> store 的完整摄入流水线

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
import os
from typing import List, Dict, Any, Optional
from ingestion.chunker import chunk
from embedding.embedder import embed
from store import vector_store


def ingest_file(
    file_path: str,
    store_path: str = "./vector_store",
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    embed_provider: str = "openai",
    embed_model: Optional[str] = None,
    store_provider: str = "faiss",
    **kwargs
) -> List[str]:
    """
    全流程摄入：文件 -> 解析切片 -> 向量化 -> 关键存 -> 持久化
    
    Args:
        file_path: 文档路径
        store_path: 向量存储路径
        chunk_size: 分块大小
        chunk_overlap: 分块重叠
        embed_provider: 嵌入服务商
        embed_model: 嵌入模型
        store_provider: 存储引擎
        **kwargs: 其他透传参数
        
    Returns:
        成功保存的块 ID 列表
    """
    # 1. 解析与切片
    print(f"正在转换文档: {file_path} ...")
    docs = chunk(
        file_path=file_path,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    if not docs:
        print("未提取到有效内容")
        return []
    
    texts = [doc.content for doc in docs]
    metadatas = [doc.metadata for doc in docs]
    
    # 2. 向量化
    print(f"正在为 {len(texts)} 个数据块生成向量 (Provider: {embed_provider}) ...")
    vectors = embed(
        texts=texts,
        provider=embed_provider,
        model=embed_model,
        **kwargs
    )
    
    # 3. 存储
    print(f"正在存入向量数据库 (Provider: {store_provider}) ...")
    ids = vector_store.add(
        texts=texts,
        vectors=vectors,
        metadatas=metadatas,
        provider=store_provider,
        **kwargs
    )
    
    # 4. 持久化
    print(f"正在持久化到: {store_path} ...")
    vector_store.save(path=store_path, provider=store_provider, **kwargs)
    
    return ids
