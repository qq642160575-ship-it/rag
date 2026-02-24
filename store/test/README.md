# store/test

本目录负责：store 模块的单元测试与集成测试验证。
不负责：端到端业务测试。

## 文件说明

- test_vector_store.py
  地位：向量存储核心功能测试
  职责：验证 add, search, save, load 等核心接口的正确性与隔离性

> 声明：
> 一旦本目录结构或职责发生变化，请同步更新本文件
