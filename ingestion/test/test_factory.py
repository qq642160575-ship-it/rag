"""
input:
- 文件路径及后缀名

output:
- 测试结果

pos:
- 位于 ingestion/test 层
- 负责测试 ParserFactory 工厂分发功能

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
"""
import unittest
from ingestion.factory import ParserFactory
from ingestion.providers.pdf_handler import PDFHandler
from ingestion.providers.word_handler import WordHandler
from ingestion.providers.text_handler import TextHandler
from ingestion.base import BaseParser


class TestParserFactory(unittest.TestCase):
    
    def test_get_parser_pdf(self):
        parser = ParserFactory.get_parser("document.pdf")
        self.assertIsInstance(parser, PDFHandler)
        self.assertIsInstance(parser, BaseParser)
    
    def test_get_parser_docx(self):
        parser = ParserFactory.get_parser("document.docx")
        self.assertIsInstance(parser, WordHandler)
        self.assertIsInstance(parser, BaseParser)
    
    def test_get_parser_doc(self):
        parser = ParserFactory.get_parser("document.doc")
        self.assertIsInstance(parser, WordHandler)
        self.assertIsInstance(parser, BaseParser)
    
    def test_get_parser_txt(self):
        parser = ParserFactory.get_parser("document.txt")
        self.assertIsInstance(parser, TextHandler)
        self.assertIsInstance(parser, BaseParser)
    
    def test_get_parser_case_insensitive(self):
        parser_upper = ParserFactory.get_parser("document.PDF")
        parser_mixed = ParserFactory.get_parser("document.PdF")
        self.assertIsInstance(parser_upper, PDFHandler)
        self.assertIsInstance(parser_mixed, PDFHandler)
    
    def test_get_parser_with_path(self):
        parser = ParserFactory.get_parser("/path/to/document.pdf")
        self.assertIsInstance(parser, PDFHandler)
    
    def test_get_parser_unsupported_format(self):
        with self.assertRaises(ValueError) as context:
            ParserFactory.get_parser("document.xlsx")
        self.assertIn("Unsupported file format", str(context.exception))
    
    def test_get_parser_no_extension(self):
        with self.assertRaises(ValueError):
            ParserFactory.get_parser("document")
    
    def test_register_handler(self):
        class CustomHandler(BaseParser):
            def parse(self, file_path: str) -> str:
                return "custom"
        
        ParserFactory.register_handler(".custom", CustomHandler)
        parser = ParserFactory.get_parser("file.custom")
        self.assertIsInstance(parser, CustomHandler)
    
    def test_register_handler_case_insensitive(self):
        class AnotherHandler(BaseParser):
            def parse(self, file_path: str) -> str:
                return "another"
        
        ParserFactory.register_handler(".XYZ", AnotherHandler)
        parser = ParserFactory.get_parser("file.xyz")
        self.assertIsInstance(parser, AnotherHandler)


if __name__ == '__main__':
    unittest.main()
