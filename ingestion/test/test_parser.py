"""
input:
- 文件路径

output:
- 测试结果

pos:
- 位于 ingestion/test 层
- 负责测试 parser.py 对外入口功能

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
"""
import unittest
from unittest.mock import patch, MagicMock
from core.schema import RawDocument
from ingestion.parser import parse


class TestParser(unittest.TestCase):
    
    @patch('ingestion.parser.ParserFactory.get_parser')
    @patch('ingestion.parser.clean_text')
    def test_parse_success(self, mock_clean_text, mock_get_parser):
        mock_parser_instance = MagicMock()
        mock_raw_doc = RawDocument(content="  Raw text with   spaces  ", metadata={"source": "test.pdf"})
        mock_parser_instance.parse.return_value = mock_raw_doc
        mock_get_parser.return_value = mock_parser_instance
        mock_clean_text.return_value = "Cleaned text"
        
        result = parse("test.pdf")
        
        self.assertIsInstance(result, RawDocument)
        self.assertEqual(result.content, "Cleaned text")
        self.assertEqual(result.metadata["source"], "test.pdf")
        mock_get_parser.assert_called_once_with("test.pdf")
        mock_parser_instance.parse.assert_called_once_with("test.pdf")
        mock_clean_text.assert_called_once_with("  Raw text with   spaces  ")
    
    @patch('ingestion.parser.ParserFactory.get_parser')
    @patch('ingestion.parser.clean_text')
    def test_parse_pdf(self, mock_clean_text, mock_get_parser):
        mock_parser_instance = MagicMock()
        mock_raw_doc = RawDocument(content="PDF content", metadata={"source": "document.pdf"})
        mock_parser_instance.parse.return_value = mock_raw_doc
        mock_get_parser.return_value = mock_parser_instance
        mock_clean_text.return_value = "PDF content"
        
        result = parse("document.pdf")
        
        self.assertIsInstance(result, RawDocument)
        self.assertEqual(result.content, "PDF content")
        mock_get_parser.assert_called_once_with("document.pdf")
    
    @patch('ingestion.parser.ParserFactory.get_parser')
    @patch('ingestion.parser.clean_text')
    def test_parse_word(self, mock_clean_text, mock_get_parser):
        mock_parser_instance = MagicMock()
        mock_raw_doc = RawDocument(content="Word content", metadata={"source": "document.docx"})
        mock_parser_instance.parse.return_value = mock_raw_doc
        mock_get_parser.return_value = mock_parser_instance
        mock_clean_text.return_value = "Word content"
        
        result = parse("document.docx")
        
        self.assertIsInstance(result, RawDocument)
        self.assertEqual(result.content, "Word content")
        mock_get_parser.assert_called_once_with("document.docx")
    
    @patch('ingestion.parser.ParserFactory.get_parser')
    @patch('ingestion.parser.clean_text')
    def test_parse_text(self, mock_clean_text, mock_get_parser):
        mock_parser_instance = MagicMock()
        mock_raw_doc = RawDocument(content="Text content", metadata={"source": "document.txt"})
        mock_parser_instance.parse.return_value = mock_raw_doc
        mock_get_parser.return_value = mock_parser_instance
        mock_clean_text.return_value = "Text content"
        
        result = parse("document.txt")
        
        self.assertIsInstance(result, RawDocument)
        self.assertEqual(result.content, "Text content")
        mock_get_parser.assert_called_once_with("document.txt")
    
    @patch('ingestion.parser.ParserFactory.get_parser')
    def test_parse_unsupported_format(self, mock_get_parser):
        mock_get_parser.side_effect = ValueError("Unsupported file format: .xlsx")
        
        with self.assertRaises(ValueError) as context:
            parse("document.xlsx")
        
        self.assertIn("Unsupported file format", str(context.exception))


if __name__ == '__main__':
    unittest.main()
