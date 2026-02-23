# ingestion/test

本目录负责：ingestion 模块的单元测试
不负责：集成测试、端到端测试

## 文件说明

- test_pdf_handler.py
  地位：PDFHandler 单元测试
  职责：测试 PDF 解析功能，使用 Mock 模拟 PyPDFLoader

- test_word_handler.py
  地位：WordHandler 单元测试
  职责：测试 Word 解析功能，使用 Mock 模拟 Docx2txtLoader

- test_text_handler.py
  地位：TextHandler 单元测试
  职责：测试文本解析功能，使用 Mock 模拟 TextLoader

- test_factory.py
  地位：ParserFactory 单元测试
  职责：测试工厂分发逻辑、后缀名识别、自定义处理器注册

- test_parser.py
  地位：parser.py 入口单元测试
  职责：测试对外入口的完整流程（工厂分发 + 文本清洗）

- test_utils.py
  地位：utils.py 工具单元测试
  职责：测试文本清洗函数（HTML 标签移除、空白处理）

- test_chunker.py
  地位：chunker.py 分块单元测试
  职责：测试文本分块、元信息保留、语义切分功能

## 运行测试

```bash
# 运行所有测试
python -m unittest discover -s ingestion/test -p "test_*.py"

# 运行单个测试文件
python -m unittest ingestion.test.test_pdf_handler

# 运行特定测试用例
python -m unittest ingestion.test.test_factory.TestParserFactory.test_get_parser_pdf
```

## 测试覆盖

- ✅ PDF 解析器（单页、多页、空文档）
- ✅ Word 解析器（.docx、.doc、空文档）
- ✅ 文本解析器（UTF-8 编码、多行文本、空文档）
- ✅ 工厂分发（后缀名识别、大小写不敏感、不支持格式）
- ✅ 自定义处理器注册
- ✅ 文本清洗（HTML 标签、多余空白、换行符）
- ✅ 完整解析流程（入口 -> 工厂 -> 解析器 -> 清洗）
- ✅ 文本分块（token 分块、语义分块、批量分块）
- ✅ 元信息保留（来源路径、块索引、分块策略）
- ✅ 分块清洗（空行移除、特殊字符处理）

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
