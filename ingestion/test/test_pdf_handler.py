"""
input:
- 测试 PDF 文件路径

output:
- 测试结果

pos:
- 位于 ingestion/test 层
- 负责测试 PDFHandler 解析功能

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
"""
import unittest
from unittest.mock import patch, MagicMock
from ingestion.providers.pdf_handler import PDFHandler


class TestPDFHandler(unittest.TestCase):
    
    @patch('ingestion.providers.pdf_handler.PyPDFLoader')
    def test_parse_pdf_success(self, mock_loader):
        mock_doc1 = MagicMock()
        mock_doc1.page_content = "Page 1 content"
        mock_doc2 = MagicMock()
        mock_doc2.page_content = "Page 2 content"
        
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = [mock_doc1, mock_doc2]
        mock_loader.return_value = mock_loader_instance
        
        handler = PDFHandler()
        result = handler.parse("test.pdf")
        
        self.assertEqual(result, "Page 1 content\nPage 2 content")
        mock_loader.assert_called_once_with("test.pdf")
        mock_loader_instance.load.assert_called_once()
    
    @patch('ingestion.providers.pdf_handler.PyPDFLoader')
    def test_parse_pdf_empty(self, mock_loader):
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = []
        mock_loader.return_value = mock_loader_instance
        
        handler = PDFHandler()
        result = handler.parse("empty.pdf")
        
        self.assertEqual(result, "")
    
    @patch('ingestion.providers.pdf_handler.PyPDFLoader')
    def test_parse_pdf_single_page(self, mock_loader):
        mock_doc = MagicMock()
        mock_doc.page_content = "Single page content"
        
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = [mock_doc]
        mock_loader.return_value = mock_loader_instance
        
        handler = PDFHandler()
        result = handler.parse("single.pdf")
        
        self.assertEqual(result, "Single page content")


if __name__ == '__main__':
    unittest.main()
