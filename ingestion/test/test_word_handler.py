"""
input:
- 测试 Word 文件路径

output:
- 测试结果

pos:
- 位于 ingestion/test 层
- 负责测试 WordHandler 解析功能

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
"""
import unittest
from unittest.mock import patch, MagicMock
from ingestion.providers.word_handler import WordHandler


class TestWordHandler(unittest.TestCase):
    
    @patch('ingestion.providers.word_handler.Docx2txtLoader')
    def test_parse_word_success(self, mock_loader):
        mock_doc = MagicMock()
        mock_doc.page_content = "Word document content"
        
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = [mock_doc]
        mock_loader.return_value = mock_loader_instance
        
        handler = WordHandler()
        result = handler.parse("test.docx")
        
        self.assertEqual(result, "Word document content")
        mock_loader.assert_called_once_with("test.docx")
        mock_loader_instance.load.assert_called_once()
    
    @patch('ingestion.providers.word_handler.Docx2txtLoader')
    def test_parse_word_empty(self, mock_loader):
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = []
        mock_loader.return_value = mock_loader_instance
        
        handler = WordHandler()
        result = handler.parse("empty.docx")
        
        self.assertEqual(result, "")
    
    @patch('ingestion.providers.word_handler.Docx2txtLoader')
    def test_parse_doc_file(self, mock_loader):
        mock_doc = MagicMock()
        mock_doc.page_content = "Old Word format content"
        
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = [mock_doc]
        mock_loader.return_value = mock_loader_instance
        
        handler = WordHandler()
        result = handler.parse("test.doc")
        
        self.assertEqual(result, "Old Word format content")
        mock_loader.assert_called_once_with("test.doc")


if __name__ == '__main__':
    unittest.main()
