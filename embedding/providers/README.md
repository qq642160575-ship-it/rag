# embedding/providers

本目录负责：具体文本嵌入模型/服务的驱动实现。
不负责：工厂分发、上层调用逻辑。

## 文件说明

- openai_handler.py
  地位：OpenAI 嵌入驱动
  职责：调用 OpenAI Embedding API 将文本转换为向量

- local_handler.py
  地位：本地嵌入驱动
  职责：使用本地模型（如 HuggingFace/Sentence-Transformers）执行嵌入任务

> 声明：
> 一旦本目录结构或职责发生变化，请同步更新本文件
