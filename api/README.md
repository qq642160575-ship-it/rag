# api

本目录负责：对外 HTTP 接口编排。
不负责：核心业务核辑、解析、向量计算、存储。

## 职责
- 定义 FastAPI/Flask 路由
- 处理请求校验与响应封装
- 编排 Ingestion、Embedding、Retrieval 与 LLM 的整体流水线

> 声明：
> 一旦本目录结构或职责发生变化，请同步更新本文件
