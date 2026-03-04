# agent

本目录负责：RAG Agent 工作流编排
不负责：原子工具、基础 LLM 调用

## 文件说明

- structured_rag.py
  地位：Agent 核心
  职责：LangGraph RAG 流程（意图→扩展→检索→重排→判断→回答）

- nodes/
  地位：图节点实现
  职责：各阶段具体逻辑

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
