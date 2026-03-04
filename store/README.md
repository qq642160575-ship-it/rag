# store

本目录负责：向量存储与检索
不负责：文档摄入、向量化、LLM 调用

## 文件说明

- base.py
  地位：抽象基类
  职责：定义 BaseVectorStore 接口

- factory.py
  地位：存储工厂
  职责：分发 Faiss/Milvus 等存储引擎

- vector_store.py
  地位：对外唯一入口
  职责：统一 add/search/save/load 接口

- providers/
  地位：具体存储实现
  职责：Faiss 引擎实现

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
