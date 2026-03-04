# api

本目录负责：REST API 接口
不负责：业务逻辑、数据存储

## 文件说明

- main.py
  地位：API 入口
  职责：FastAPI 实例、路由挂载

- routes/
  地位：路由层
  职责：请求参数校验、响应封装

- models/
  地位：数据模型
  职责：Pydantic Request/Response 定义

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
