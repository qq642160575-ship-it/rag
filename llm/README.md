# llm

本目录负责：LLM 调用与提示词管理
不负责：文档摄入、向量存储、检索

## 文件说明

- base.py
  地位：抽象基类
  职责：定义 BaseLLMHandler 接口

- factory.py
  地位：LLM 工厂
  职责：分发 OpenAI/Claude/Gemini

- prompts/
  地位：提示词管理
  职责：加载 YAML 模板

- providers/
  地位：具体 LLM 实现
  职责：OpenAI/Claude/Gemini API 封装

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
