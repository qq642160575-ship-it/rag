"""
input:
- 测试文本文件路径

output:
- 测试结果

pos:
- 位于 ingestion/test 层
- 负责测试 TextHandler 解析功能

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
"""
import unittest
from unittest.mock import patch, MagicMock
from ingestion.providers.text_handler import TextHandler


class TestTextHandler(unittest.TestCase):
    
    @patch('ingestion.providers.text_handler.TextLoader')
    def test_parse_text_success(self, mock_loader):
        mock_doc = MagicMock()
        mock_doc.page_content = "Text file content"
        
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = [mock_doc]
        mock_loader.return_value = mock_loader_instance
        
        handler = TextHandler()
        result = handler.parse("test.txt")
        
        self.assertEqual(result, "Text file content")
        mock_loader.assert_called_once_with("test.txt", encoding="utf-8")
        mock_loader_instance.load.assert_called_once()
    
    @patch('ingestion.providers.text_handler.TextLoader')
    def test_parse_text_empty(self, mock_loader):
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = []
        mock_loader.return_value = mock_loader_instance
        
        handler = TextHandler()
        result = handler.parse("empty.txt")
        
        self.assertEqual(result, "")
    
    @patch('ingestion.providers.text_handler.TextLoader')
    def test_parse_text_multiline(self, mock_loader):
        mock_doc = MagicMock()
        mock_doc.page_content = "Line 1\nLine 2\nLine 3"
        
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = [mock_doc]
        mock_loader.return_value = mock_loader_instance
        
        handler = TextHandler()
        result = handler.parse("multiline.txt")
        
        self.assertEqual(result, "Line 1\nLine 2\nLine 3")


if __name__ == '__main__':
    unittest.main()
