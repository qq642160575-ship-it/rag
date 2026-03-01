# agent

本目录负责：高层业务逻辑的编排与 Agent 工作流（基于 LangGraph）。
不负责：原子工具实现、基础 LLM 调用。

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件

## 文件说明

- main.py
  地位：Agent 入口
  职责：组装 LangGraph，定义状态流转

- output_class/
  地位：数据模型层
  职责：定义 TypedDict 和 Pydantic 输出格式

- nodes/
  地位：动作执行层
  职责：实现具体的图节点逻辑

- COMPREHENSIVE_GUIDE.md
  地位：设计说明书
  职责：详细记录 RAG 流程设计细节

