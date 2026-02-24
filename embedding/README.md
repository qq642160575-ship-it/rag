# embedding

本目录负责：文本向量化处理。
不负责：文档摄入、向量存储、检索、LLM 调用。

## 文件说明

- base.py
  地位：嵌入器层抽象基座
  职责：定义 `BaseEmbedder` 接口契约，确保不同服务商的兼容性

- factory.py
  地位：嵌入器工厂
  职责：根据配置动态生产具体的嵌入器实例（如 OpenAI, Local）

- embedder.py
  地位：嵌入层对外唯一入口
  职责：提供统一的文本向量化接口，屏蔽底层引擎差异

- providers/
  地位：具体嵌入器实现
  职责：包装各大厂商的 API 或本地模型（OpenAI, Sentence-Transformers 等）

> 声明：
> 一旦本目录结构或职责发生变化，请同步更新本文件
