# monitoring

本目录负责：调用链追踪与指标收集
不负责：业务逻辑、数据存储

## 文件说明

- tracer.py
  地位：调用链追踪核心
  职责：基于 OpenTelemetry 的分布式追踪

- metrics.py
  地位：指标收集核心
  职责：基于 Prometheus 的延迟/错误率/请求量统计

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件

## 使用示例

### 1. 追踪函数执行
```python
from monitoring import trace_step

@trace_step("ingestion.chunk")
def process_file(path):
    # 你的业务逻辑
    return chunks
```
**输出示例**：
```
Span(ingestion.chunk) started
Span(ingestion.chunk) ended
```

### 2. 追踪代码块
```python
from monitoring import trace_block

def search():
    with trace_block("store.search", provider="faiss"):
        results = vector_store.search(query_vector, top_k=5)
        return results
```
**输出示例**：
```
Span(store.search) started
Span(store.search) provider=faiss
Span(store.search) ended
```

### 3. 自动记录延迟
```python
from monitoring import track_latency

@track_latency("rag.retrieval", provider="faiss")
def retrieve(query_vector):
    return vector_store.search(query_vector)
```
**输出示例**：
```
# Prometheus 指标输出
# HELP rag_retrieval_seconds Latency of retrieval
# TYPE rag_retrieval_seconds histogram
rag_retrieval_seconds_bucket{provider="faiss",le="0.005"} 0.0
rag_retrieval_seconds_bucket{provider="faiss",le="0.01"} 1.0
rag_retrieval_seconds_bucket{provider="faiss",le="0.025"} 5.0
...
rag_retrieval_seconds_sum{provider="faiss"} 0.123
rag_retrieval_seconds_count{provider="faiss"} 10
```

### 4. 手动计时块
```python
from monitoring import Timer

def ingest():
    with Timer("pipeline.ingest", step="embedding"):
        vectors = embed(texts)
    with Timer("pipeline.ingest", step="storage"):
        store.add(vectors)
```
**输出示例**：
```
# 指标输出
pipeline_ingest_seconds_bucket{step="embedding",le="0.1"} 8.0
pipeline_ingest_seconds_bucket{step="storage",le="0.05"} 8.0
```

### 5. 计数请求/错误
```python
from monitoring import Metrics

# 成功计数
Metrics.inc_counter("api.requests", status="success", endpoint="/search")

# 错误计数
Metrics.inc_counter("api.requests", status="error", endpoint="/search")
```
**输出示例**：
```
# HELP api_requests_total Total API requests
# TYPE api_requests_total counter
api_requests_total{endpoint="/search",status="success"} 95.0
api_requests_total{endpoint="/search",status="error"} 5.0
```

### 6. 在 pipeline 中使用
```python
from monitoring import trace_step, track_latency, Timer
from pipeline.ingest_flow import ingest_file

@trace_step("pipeline.ingest")
@track_latency("pipeline.ingest", provider="openai")
def monitored_ingest(path):
    with Timer("pipeline.total", file=path):
        return ingest_file(path)
```
**输出示例**：
```
Span(pipeline.ingest) started
Span(pipeline.ingest) provider=openai
pipeline_ingest_seconds_bucket{le="0.5"} 2.0
pipeline_ingest_seconds_bucket{le="1.0"} 5.0
pipeline_ingest_seconds_sum{provider="openai"} 3.456
pipeline_ingest_seconds_count{provider="openai"} 5
```

### 7. 初始化（可选）
```python
from monitoring import Tracer

# 默认自动初始化，也可手动指定服务名
Tracer.init(service_name="my-rag-service")
```
**输出示例**：
```
Tracer initialized: my-rag-service
```

### 8. 完整使用示例
```python
from monitoring import trace_step, track_latency, Metrics, Timer
from ingestion import chunk
from embedding import embed
from store import vector_store

@trace_step("full.pipeline")
@track_latency("full.pipeline", provider="faiss")
def run_rag_pipeline(file_path: str):
    # 1. 解析切片
    with Timer("step.chunk"):
        docs = chunk(file_path)
    
    # 2. 向量化
    with Timer("step.embed"):
        texts = [d.content for d in docs]
        vectors = embed(texts)
    
    # 3. 存储
    with Timer("step.store"):
        ids = vector_store.add(texts, vectors)
    
    # 4. 计数
    Metrics.inc_counter("pipeline.success", status="ok")
    return ids

# 运行
run_rag_pipeline("doc.pdf")
```
**输出示例**：
```
Span(full.pipeline) started
Span(step.chunk) started
Span(step.chunk) ended
Span(step.embed) started
Span(step.embed) ended
Span(step.store) started
Span(step.store) ended
Span(full.pipeline) ended

# Prometheus 指标
pipeline_success_total{status="ok"} 1.0
step_chunk_seconds_bucket{le="0.1"} 1.0
step_embed_seconds_bucket{le="0.5"} 1.0  
step_store_seconds_bucket{le="0.05"} 1.0
```
