# agent

本目录负责：高层业务逻辑的编排与 Agent 工作流（基于 LangGraph）。

## 职责
- 定义状态机（StateGraph）与节点逻辑。
- 编排 LLM 调用、向量检索、重排序等原子操作。
- 实现复杂的多步推理与自我修正逻辑（如重写查询）。

## 结构
- `structured_rag.py`: 生产级结构化 RAG Agent 实现。
    - 使用 `PromptManager` 管理分层提示词。
    - 集成 `with_structured_output` 进行强类型输出控制。
    - 包含：意图分析、查询扩展、召回质量评估、查询重写、最终回答。

## 使用

```python
from llm.factory import get_llm
from store.factory import get_vector_store # 假设已有
from agent.structured_rag import StructuredRAGAgent

# 初始化依赖
llm_handler = get_llm("openai", "gpt-4o-mini")
vector_store = ... # 初始化你的向量数据库

# 创建 Agent
agent = StructuredRAGAgent(
    llm_handler=llm_handler,
    vector_store=vector_store,
    prompt_dir="./llm/prompts"
)

# 执行
result = agent.invoke("为什么 ingestion 后检索不到内容？")
print(result["answer"])
```

> 声明：
> 任何 agent 逻辑的更新必须同步更新本文件。
