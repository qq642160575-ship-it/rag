# prompts

本目录负责：管理各种 LLM 任务节点的提示词模板。

## 职责
- 分离系统（System）与用户（User）提示词。
- 使用 YAML 格式定义模板，支持变量注入（`format`）。
- 提供统一的消息封装接口（`get_langchain_messages`）。

## 结构
- `manager.py`: `PromptManager` 核心逻辑。
- `intent.yaml`: 意图识别节点。
- `expand.yaml`: 查询扩展节点。
- `rerank.yaml`: 相关性打分节点。
- `judge.yaml`: 召回质量评估节点。
- `rewrite.yaml`: 查询重写节点。
- `answer.yaml`: 最终问答节点。

## 使用

YAML 示例 (`intent.yaml`):
```yaml
system: |
  你是一个意图识别专家。
user: |
  问题: {original_question}
```

代码示例:
```python
pm = PromptManager("./llm/prompts")
messages = pm.get_langchain_messages("intent", original_question="...")
```
