# pipeline

本目录负责：业务流程编排
不负责：具体解析、向量化、存储实现

## 文件说明

- ingest_flow.py
  地位：摄入流水线入口
  职责：协调 ingestion→embedding→store 完整流程

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
