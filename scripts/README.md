# scripts

本目录负责：存放各种辅助脚本、测试脚本和离线处理工具。

## 脚本说明

- **ingest_data.py**
  - **用途**：离线执行数据摄入。
  - **功能**：自动下载指定 PDF（如果不存在），调用 `pipeline.ingest_flow` 将文档切片并进行本地向量化（使用 local embedder），最后持久化到 `data/` 目录。
  
- **test_search.py**
  - **用途**：验证向量库检索效果。
  - **功能**：加载 `data/vector_store_rag` 索引，使用 `local` 嵌入器转换查询，并打印最相关的文档片段。

---
> 声明：
> 任何新增脚本或脚本逻辑重大变更，必须同步更新此 README 文档。
