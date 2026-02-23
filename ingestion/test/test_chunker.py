"""
input:
- 文本内容、分块参数

output:
- 测试结果

pos:
- 位于 ingestion/test 层
- 负责测试 chunker.py 分块功能

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
"""
import unittest
from core.schema import RawDocument
from ingestion.chunker import (
    clean_text_for_chunking,
    chunk_text,
    chunk_documents,
    semantic_chunk_text
)


class TestCleanTextForChunking(unittest.TestCase):
    
    def test_remove_empty_lines(self):
        text = "Line 1\n\n\n\nLine 2\n\n\nLine 3"
        result = clean_text_for_chunking(text)
        self.assertNotIn("\n\n\n", result)
    
    def test_remove_special_characters(self):
        text = "Normal text\x00\x01\x02 with special chars"
        result = clean_text_for_chunking(text)
        self.assertNotIn("\x00", result)
        self.assertNotIn("\x01", result)
    
    def test_normalize_spaces(self):
        text = "Text    with     multiple    spaces"
        result = clean_text_for_chunking(text)
        self.assertNotIn("    ", result)
        self.assertIn("Text with multiple spaces", result)
    
    def test_strip_lines(self):
        text = "  Line 1  \n  Line 2  \n  Line 3  "
        result = clean_text_for_chunking(text)
        lines = result.split('\n')
        for line in lines:
            self.assertEqual(line, line.strip())
    
    def test_empty_text(self):
        result = clean_text_for_chunking("")
        self.assertEqual(result, "")
    
    def test_whitespace_only(self):
        result = clean_text_for_chunking("   \n\n   \t\t   ")
        self.assertEqual(result, "")


class TestChunkText(unittest.TestCase):
    
    def test_basic_chunking(self):
        text = "This is a test. " * 100
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
        
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertIsInstance(chunk, RawDocument)
            # 字符数可能略大于 chunk_size 因为 separators
            self.assertLessEqual(len(chunk.content), 150)
    
    def test_chunk_metadata(self):
        text = "Test content"
        metadata = {"author": "Test Author", "date": "2024-01-01"}
        source = "/path/to/test.pdf"
        parent_id = "parent123"
        
        chunks = chunk_text(text, metadata=metadata, source=source, parent_id=parent_id)
        
        self.assertEqual(len(chunks), 1)
        chunk = chunks[0]
        self.assertEqual(chunk.metadata["author"], "Test Author")
        self.assertEqual(chunk.metadata["date"], "2024-01-01")
        self.assertEqual(chunk.metadata["source"], source)
        self.assertEqual(chunk.metadata["parent_id"], parent_id)
        self.assertEqual(chunk.metadata["chunk_index"], 0)
        self.assertEqual(chunk.metadata["total_chunks"], 1)
    
    def test_chunk_overlap(self):
        text = "A" * 200 + "B" * 200
        chunks = chunk_text(text, chunk_size=150, chunk_overlap=50)
        
        self.assertGreater(len(chunks), 1)
    
    def test_empty_text(self):
        chunks = chunk_text("")
        self.assertEqual(len(chunks), 0)
    
    def test_small_text(self):
        text = "Short text"
        chunks = chunk_text(text, chunk_size=512)
        
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].content, "Short text")
    
    def test_chunk_indices(self):
        text = "Content. " * 200
        chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
        
        for i, chunk in enumerate(chunks):
            self.assertEqual(chunk.metadata["chunk_index"], i)
            self.assertEqual(chunk.metadata["total_chunks"], len(chunks))


class TestChunkDocuments(unittest.TestCase):
    
    def test_chunk_multiple_documents(self):
        docs = [
            RawDocument(content="Document 1 content. " * 50, metadata={"source": "doc1.pdf"}),
            RawDocument(content="Document 2 content. " * 50, metadata={"source": "doc2.pdf"}),
        ]
        
        chunks = chunk_documents(docs, chunk_size=100, chunk_overlap=20)
        
        self.assertGreater(len(chunks), 2)
        
        doc1_chunks = [c for c in chunks if c.metadata.get("source") == "doc1.pdf"]
        doc2_chunks = [c for c in chunks if c.metadata.get("source") == "doc2.pdf"]
        
        self.assertGreater(len(doc1_chunks), 0)
        self.assertGreater(len(doc2_chunks), 0)
        # 检查父子关联
        for c in doc1_chunks:
            self.assertEqual(c.metadata["parent_id"], docs[0].id)
        for c in doc2_chunks:
            self.assertEqual(c.metadata["parent_id"], docs[1].id)
    
    def test_empty_documents_list(self):
        chunks = chunk_documents([])
        self.assertEqual(len(chunks), 0)
    
    def test_preserve_metadata(self):
        docs = [
            RawDocument(
                content="Test content. " * 50,
                metadata={"author": "Author1", "category": "Science"}
            )
        ]
        
        chunks = chunk_documents(docs, chunk_size=100)
        
        for chunk in chunks:
            self.assertEqual(chunk.metadata["author"], "Author1")
            self.assertEqual(chunk.metadata["category"], "Science")


class TestSemanticChunkText(unittest.TestCase):
    
    def test_paragraph_based_chunking(self):
        text = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
        chunks = semantic_chunk_text(text, max_chunk_size=50)
        
        self.assertGreater(len(chunks), 0)
        for chunk in chunks:
            self.assertIsInstance(chunk, RawDocument)
            self.assertEqual(chunk.metadata["chunking_strategy"], "semantic")
    
    def test_long_paragraph_splitting(self):
        long_para = "Sentence one. Sentence two. Sentence three. " * 20
        chunks = semantic_chunk_text(long_para, max_chunk_size=100)
        
        self.assertGreater(len(chunks), 1)
    
    def test_chinese_text_chunking(self):
        text = "这是第一段。这是第一段的第二句。\n\n这是第二段。这是第二段的第二句。"
        chunks = semantic_chunk_text(text, max_chunk_size=50)
        
        self.assertGreater(len(chunks), 0)
        for chunk in chunks:
            self.assertGreater(len(chunk.content), 0)
    
    def test_metadata_preservation(self):
        text = "Test paragraph.\n\nAnother paragraph."
        metadata = {"title": "Test Document"}
        source = "/path/to/doc.txt"
        
        chunks = semantic_chunk_text(text, metadata=metadata, source=source)
        
        for chunk in chunks:
            self.assertEqual(chunk.metadata["title"], "Test Document")
            self.assertEqual(chunk.metadata["source"], source)
            self.assertEqual(chunk.metadata["chunking_strategy"], "semantic")
    
    def test_empty_text(self):
        chunks = semantic_chunk_text("")
        self.assertEqual(len(chunks), 0)
    
    def test_chunk_indices(self):
        text = "Para 1.\n\nPara 2.\n\nPara 3.\n\nPara 4."
        chunks = semantic_chunk_text(text, max_chunk_size=20)
        
        for i, chunk in enumerate(chunks):
            self.assertEqual(chunk.metadata["chunk_index"], i)
            self.assertEqual(chunk.metadata["total_chunks"], len(chunks))
    
    def test_mixed_punctuation(self):
        text = "English sentence. 中文句子。Another sentence! 另一个句子？"
        chunks = semantic_chunk_text(text, max_chunk_size=100)
        
        self.assertGreater(len(chunks), 0)


class TestIntegration(unittest.TestCase):
    
    def test_full_pipeline(self):
        raw_text = """
        第一章 引言
        
        这是第一段内容。这段内容包含多个句子。每个句子都有意义。
        
        第二章 主体
        
        这是第二段内容。这段内容也包含多个句子。内容更加丰富。
        
        第三章 结论
        
        这是结论部分。总结了前面的内容。
        """
        
        metadata = {
            "source": "/path/to/document.pdf",
            "author": "Test Author",
            "title": "Test Document"
        }
        
        chunks = semantic_chunk_text(raw_text, max_chunk_size=100, metadata=metadata)
        
        self.assertGreater(len(chunks), 0)
        
        for chunk in chunks:
            self.assertIn("source", chunk.metadata)
            self.assertIn("author", chunk.metadata)
            self.assertIn("chunk_index", chunk.metadata)
            self.assertIn("total_chunks", chunk.metadata)
            self.assertIn("chunk_size", chunk.metadata)
            self.assertGreater(len(chunk.content), 0)


if __name__ == '__main__':
    unittest.main()
