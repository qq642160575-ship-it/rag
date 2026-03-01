# core

本目录负责：Agent 核心状态定义与结构化输出格式
不负责：业务逻辑处理、动作执行

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件

## 文件说明

- rag_state.py
  地位：全局状态定义
  职责：定义 LangGraph 的核心 RAGState 字典格式

- intent.py
  地位：意图分析模型
  职责：定义用户意图识别的 Pydantic 输出格式

- expand.py
  地位：查询扩展模型
  职责：定义查询扩展生成的 Pydantic 输出格式

- judge.py
  地位：召回评估模型
  职责：定义检索质量评估的 Pydantic 输出格式

- rerank.py
  地位：重排评分模型
  职责：定义片段重排打分的 Pydantic 输出格式
