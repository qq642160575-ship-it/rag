import unittest
from unittest.mock import patch, MagicMock
from core.schema import RawDocument
from pipeline.ingest_flow import ingest_file


class TestIngestFlow(unittest.TestCase):
    
    @patch('pipeline.ingest_flow.chunk')
    @patch('pipeline.ingest_flow.embed')
    @patch('pipeline.ingest_flow.vector_store')
    def test_ingest_file_success(self, mock_store, mock_embed, mock_chunk):
        # 准备 Mock 数据
        mock_doc1 = RawDocument(content="chunk 1", metadata={"source": "test.txt"})
        mock_doc2 = RawDocument(content="chunk 2", metadata={"source": "test.txt"})
        mock_chunk.return_value = [mock_doc1, mock_doc2]
        
        mock_embed.return_value = [[0.1, 0.2], [0.3, 0.4]]
        mock_store.add.return_value = ["id1", "id2"]
        
        # 执行摄入
        ids = ingest_file(
            file_path="test.txt",
            store_path="test_store",
            embed_provider="mock_embedder",
            store_provider="mock_store"
        )
        
        # 验证结果
        self.assertEqual(ids, ["id1", "id2"])
        
        # 验证解析调用
        mock_chunk.assert_called_once_with(
            file_path="test.txt",
            chunk_size=512,
            chunk_overlap=50
        )
        
        # 验证向量化调用
        mock_embed.assert_called_once_with(
            texts=["chunk 1", "chunk 2"],
            provider="mock_embedder",
            model=None
        )
        
        # 验证存储调用
        mock_store.add.assert_called_once_with(
            texts=["chunk 1", "chunk 2"],
            vectors=[[0.1, 0.2], [0.3, 0.4]],
            metadatas=[mock_doc1.metadata, mock_doc2.metadata],
            provider="mock_store"
        )
        
        # 验证持久化调用
        mock_store.save.assert_called_once_with(
            path="test_store",
            provider="mock_store"
        )

    @patch('pipeline.ingest_flow.chunk')
    def test_ingest_file_empty(self, mock_chunk):
        mock_chunk.return_value = []
        
        ids = ingest_file("empty.txt")
        self.assertEqual(ids, [])


if __name__ == '__main__':
    unittest.main()
