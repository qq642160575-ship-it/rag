# ingestion

本目录负责：文档摄入与解析
不负责：向量存储、检索、LLM 调用

## 文件说明

- parser.py
  地位：对外唯一入口
  职责：统一调用入口，返回清洗后的文本

- factory.py
  地位：解析器工厂
  职责：根据后缀名分发对应解析器

- base.py
  地位：抽象基类定义
  职责：定义 BaseParser 接口契约

- utils.py
  地位：文本清洗工具
  职责：去空白、去 HTML 标签

- chunker.py
  地位：文本分块处理
  职责：清洗文本、按 token 分块、保留元信息

- providers/
  地位：具体解析器实现
  职责：包装 LangChain Loader

## 支持格式

| 后缀 | 解析器 | LangChain Loader |
|------|--------|------------------|
| .pdf | PDFHandler | PyPDFLoader |
| .docx/.doc | WordHandler | Docx2txtLoader |
| .txt | TextHandler | TextLoader |

## 分块功能

- **文本清洗**
  - 去除空行和多余空白
  - 移除特殊控制字符
  - 规范化空格和换行

- **分块策略**
  - `chunk_text()`: 基于 token 的递归分块
  - `semantic_chunk_text()`: 基于语义的段落/句子分块
  - `chunk_documents()`: 批量文档分块

- **元信息保留**
  - source: 文档来源路径
  - chunk_index: 块在文档中的索引
  - total_chunks: 文档总块数
  - chunk_size: 当前块的字符数
  - chunking_strategy: 分块策略标识

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
