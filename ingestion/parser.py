"""
input:
- file_path: 文档路径（支持 PDF/Word/TXT）

output:
- RawDocument: 解析后的文档对象

pos:
- 位于 ingestion 层对外入口
- 负责统一调用入口，不负责具体解析逻辑

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from core.schema import RawDocument
from ingestion.factory import ParserFactory
from ingestion.utils import clean_text


def parse(file_path: str) -> RawDocument:
    parser = ParserFactory.get_parser(file_path)
    # 返回 RawDocument 对象
    doc = parser.parse(file_path)
    # 对内容进行清洗并更新
    doc.content = clean_text(doc.content)
    return doc
