# store

本目录负责：文本向量的存储、检索与持久化编排。
不负责：文本向量化（由 embedding 层负责）、数据清洗、业务逻辑分发。

## 文件说明

- base.py
  地位：存储层抽象基座
  职责：定义 `BaseVectorStore` 接口契约，确保不同引擎的兼容性

- factory.py
  地位：实例选择器
  职责：根据配置动态生产具体的存储引擎实例（如 FAISS）

- vector_store.py
  地位：存储层唯一对外出口
  职责：屏蔽底层引擎差异，提供极致简化的单例/快捷操作接口

- providers/faiss.py
  地位：FAISS 引擎驱动实现
  职责：执行基于 L2 距离的向量检索与本地磁盘持久化

> 声明：
> 一旦本目录结构或职责发生变化，请同步更新本文件

## 快速使用
```python
from store import vector_store

vector_store.add(texts=["Hello"], vectors=[[0.1, 0.2]])
results = vector_store.search([0.1, 0.21], top_k=1)
```
