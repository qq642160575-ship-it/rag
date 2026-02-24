import os
import shutil
import unittest
import numpy as np
from store import vector_store


class TestVectorStore(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_faiss_store"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        # 清除全局实例以保证测试隔离
        vector_store._instances.clear()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_and_search(self):
        texts = ["apple", "banana", "orange"]
        vectors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        metadatas = [{"type": "fruit"}, {"type": "fruit"}, {"type": "fruit"}]
        
        ids = vector_store.add(texts, vectors, metadatas)
        self.assertEqual(len(ids), 3)
        
        # 搜索 apple 相似的向量
        query = [0.9, 0.1, 0.0]
        results = vector_store.search(query, top_k=1)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "apple")
        self.assertEqual(results[0]["metadata"]["type"], "fruit")

    def test_save_and_load(self):
        texts = ["hello", "world"]
        vectors = [[0.5, 0.5], [1.0, 1.0]]
        
        vector_store.add(texts, vectors, provider="faiss")
        vector_store.save(self.test_dir)
        
        # 清除全局实例或使用新的 provider 参数强制新建
        # 这里简单起见，我们重新初始化并加载
        from store.providers.faiss import FAISSVectorStore
        new_store = FAISSVectorStore()
        new_store.load(self.test_dir)
        
        query = [0.4, 0.4]
        results = new_store.search(query, top_k=1)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "hello")


if __name__ == "__main__":
    unittest.main()
