# llm

本目录负责：大语言模型（LLM）的调用与提示词管理。
不负责：文档摄入、向量检索、前端交互。

## 职责
- 封装不同模型服务商的 API 调用（OpenAI, Anthropic, Gemini 等）
- 管理系统提示词（Prompts）模板
- 实现对话上下文管理与流式输出处理

## 结构
- `base.py`: 定义 `BaseLLMHandler` 接口。
- `providers/`: 各种模型供应商的实现。
    - `openai.py`: OpenAI 客户端实现（基于 LangChain）。
    - `anthropic.py`: Anthropic 客户端实现（基于 LangChain）。
    - `gemini.py`: Google Gemini 客户端实现（基于 LangChain）。

## 使用

### 1. 统一接口调用
```python
from llm.providers import OpenAIHandler

handler = OpenAIHandler(model_name="gpt-4o")

# 统一消息格式调用
response = handler.chat([{"role": "user", "content": "你好"}])
```

### 2. 工厂模式（推荐）
```python
from llm.factory import get_llm

llm = get_llm("openai", model_name="gpt-4o", temperature=0)
# llm = get_llm("anthropic", model_name="claude-3-5-sonnet-20240620")
```

### 3. 在 LangGraph / LangChain 中使用
如果你需要在 LangGraph 节点中使用，或者需要使用 `.with_structured_output()` 等高级功能，请使用 `.model` 属性获取原始 LangChain 对象：

```python
from llm.factory import get_llm

handler = get_llm("openai", model_name="gpt-4o")

# 获取原始 LangChain 聊天模型
llm = handler.model 

# 结构化输出
structured_llm = llm.with_structured_output(MySchema)

# 在 LangGraph 节点中使用
def my_node(state):
    # 可以直接使用 handler.invoke (兼容底层 invoke)
    result = handler.invoke(f"处理问题: {state['query']}")
    return {"response": result.content}
```

> 声明：

> 一旦本目录结构或职责发生变化，请同步更新本文件


