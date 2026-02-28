import os
import sys

# 将项目根目录添加到 python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.ingest_flow import ingest_file
from dotenv import load_dotenv

# 加载 .env 变量
load_dotenv()

from pipeline.ingest_flow import vector_store
from embedding.factory import EmbedderFactory

# 加载本地存储
vector_store.load("data/vector_store_rag", provider="faiss")

# 获取本地嵌入器
embedder = EmbedderFactory.get_embedder(provider="local")
query_vector = embedder.embed_query("What is the core idea of RAG?")

# 1. 正常检索
print("\n>>> 正在执行正常检索...")
results = vector_store.search(query_vector, top_k=3, provider="faiss")
for r in results:
    print(f"[Score: {r.get('score')}] Source: {r['metadata'].get('source')}")
    print(f"Content: {r['text'][:100]}...\n")

# 2. 带过滤条件的检索 (正确路径)
print("\n>>> 正在执行带过滤条件的检索 (source='data/rag_paper.pdf')...")
filter_query = {"source": "data/rag_paper.pdf"}
results_filtered = vector_store.search(query_vector, top_k=3, provider="faiss", filter=filter_query)
print(f"命中数量: {len(results_filtered)}")
for r in results_filtered:
    print(f"Source: {r['metadata'].get('source')} | Text: {r['text'][:100]}...")

# 3. 带过滤条件的检索 (不存在的路径 - 验证硬过滤)
print("\n>>> 正在执行过滤检索 (source='wrong_path.pdf')...")
wrong_filter = {"source": "wrong_path.pdf"}
results_empty = vector_store.search(query_vector, top_k=3, provider="faiss", filter=wrong_filter)
print(f"命中数量 (预期为0): {len(results_empty)}")
