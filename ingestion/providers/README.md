# providers

本目录负责：具体文档解析器实现
不负责：工厂分发、文本清洗

## 文件说明

- pdf_handler.py
  地位：PDF 解析器
  职责：包装 PyPDFLoader，返回文本

- word_handler.py
  地位：Word 解析器
  职责：包装 Docx2txtLoader，返回文本

- text_handler.py
  地位：文本解析器
  职责：包装 TextLoader，返回文本

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
