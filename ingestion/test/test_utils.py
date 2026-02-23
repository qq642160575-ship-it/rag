"""
input:
- 原始文本

output:
- 测试结果

pos:
- 位于 ingestion/test 层
- 负责测试 utils.py 文本清洗功能

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
"""
import unittest
from ingestion.utils import clean_text, remove_empty_lines


class TestUtils(unittest.TestCase):
    
    def test_clean_text_remove_html_tags(self):
        raw_text = "This is <b>bold</b> and <i>italic</i> text"
        result = clean_text(raw_text)
        self.assertEqual(result, "This is bold and italic text")
    
    def test_clean_text_remove_multiple_spaces(self):
        raw_text = "Text   with    multiple     spaces"
        result = clean_text(raw_text)
        self.assertEqual(result, "Text with multiple spaces")
    
    def test_clean_text_remove_newlines(self):
        raw_text = "Line 1\n\n\nLine 2"
        result = clean_text(raw_text)
        self.assertEqual(result, "Line 1 Line 2")
    
    def test_clean_text_strip_whitespace(self):
        raw_text = "   Text with leading and trailing spaces   "
        result = clean_text(raw_text)
        self.assertEqual(result, "Text with leading and trailing spaces")
    
    def test_clean_text_combined(self):
        raw_text = "  <p>Paragraph with   multiple spaces</p>\n\n<div>Another section</div>  "
        result = clean_text(raw_text)
        self.assertEqual(result, "Paragraph with multiple spaces Another section")
    
    def test_clean_text_empty_string(self):
        result = clean_text("")
        self.assertEqual(result, "")
    
    def test_clean_text_only_whitespace(self):
        result = clean_text("   \n\n   \t\t   ")
        self.assertEqual(result, "")
    
    def test_remove_empty_lines_basic(self):
        text = "Line 1\n\nLine 2\n\n\nLine 3"
        result = remove_empty_lines(text)
        self.assertEqual(result, "Line 1\nLine 2\nLine 3")
    
    def test_remove_empty_lines_whitespace_only(self):
        text = "Line 1\n   \nLine 2\n\t\nLine 3"
        result = remove_empty_lines(text)
        self.assertEqual(result, "Line 1\nLine 2\nLine 3")
    
    def test_remove_empty_lines_no_empty_lines(self):
        text = "Line 1\nLine 2\nLine 3"
        result = remove_empty_lines(text)
        self.assertEqual(result, "Line 1\nLine 2\nLine 3")
    
    def test_remove_empty_lines_all_empty(self):
        text = "\n\n\n"
        result = remove_empty_lines(text)
        self.assertEqual(result, "")
    
    def test_remove_empty_lines_single_line(self):
        text = "Single line"
        result = remove_empty_lines(text)
        self.assertEqual(result, "Single line")


if __name__ == '__main__':
    unittest.main()
