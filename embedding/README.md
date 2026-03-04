# embedding

本目录负责：文本向量化
不负责：文档摄入、向量存储、检索、LLM 调用

## 文件说明

- base.py
  地位：抽象基类
  职责：定义 BaseEmbedder 接口

- factory.py
  地位：嵌入器工厂
  职责：分发 OpenAI/Local 嵌入器

- embedder.py
  地位：对外唯一入口
  职责：统一 embed/embed_query 接口

- providers/
  地位：具体嵌入器
  职责：OpenAI/本地模型实现

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
