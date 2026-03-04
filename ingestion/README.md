# ingestion

本目录负责：文档摄入与解析切片
不负责：向量存储、检索、LLM 调用

## 文件说明

- parser.py
  地位：解析入口
  职责：调用解析器工厂，返回 RawDocument

- factory.py
  地位：解析器工厂
  职责：根据后缀名分发解析器

- base.py
  地位：抽象基类
  职责：定义 BaseParser 接口

- utils.py
  地位：文本清洗
  职责：去空白、去 HTML

- chunker.py
  地位：对外唯一入口
  职责：解析+切片统一入口，支持 basic/semantic 策略

- providers/
  地位：具体解析器
  职责：PDF/Word/Txt 解析实现

> 声明：
> 一旦本目录结构或职责发生变化，请更新本文件
