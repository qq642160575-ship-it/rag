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
        vector_store._instances.clear()
        vector_store._loaded_paths.clear()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        vector_store._instances.clear()
        vector_store._loaded_paths.clear()

    def test_add_and_search(self):
        texts = ["apple", "banana", "orange"]
        vectors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        metadatas = [{"type": "fruit"}, {"type": "fruit"}, {"type": "fruit"}]
        
        ids = vector_store.add(texts, vectors, metadatas, path=self.test_dir)
        self.assertEqual(len(ids), 3)
        
        query = [0.9, 0.1, 0.0]
        results = vector_store.search(query, top_k=1, path=self.test_dir)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "apple")
        self.assertEqual(results[0]["metadata"]["type"], "fruit")

    def test_save_and_load(self):
        texts = ["hello", "world"]
        vectors = [[0.5, 0.5], [1.0, 1.0]]
        
        vector_store.add(texts, vectors, path=self.test_dir)
        vector_store.save(path=self.test_dir)
        
        vector_store._loaded_paths.clear()
        vector_store._instances.clear()
        
        results = vector_store.search([0.4, 0.4], top_k=1, path=self.test_dir)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "hello")

    def test_default_save_path(self):
        """测试默认保存路径 ./save"""
        texts = ["test1", "test2"]
        vectors = [[1.0, 2.0], [3.0, 4.0]]
        
        vector_store.add(texts, vectors, path="./save")
        vector_store.save(path="./save")
        
        self.assertTrue(os.path.exists("./save"))
        
        vector_store._loaded_paths.clear()
        vector_store._instances.clear()
        
        results = vector_store.search([1.0, 2.0], top_k=1, path="./save")
        self.assertEqual(len(results), 1)
        
        shutil.rmtree("./save", ignore_errors=True)

    def test_auto_load_on_search(self):
        """测试 search 时自动加载已存储数据"""
        texts = ["auto", "load", "test"]
        vectors = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
        
        vector_store.add(texts, vectors, path=self.test_dir)
        vector_store.save(path=self.test_dir)
        
        vector_store._loaded_paths.clear()
        vector_store._instances.clear()
        
        results = vector_store.search([0.9, 0.1], top_k=1, path=self.test_dir)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "auto")

    def test_add_after_load(self):
        """测试加载后追加数据"""
        texts1 = ["first", "second"]
        vectors1 = [[1.0, 0.0], [0.0, 1.0]]
        
        vector_store.add(texts1, vectors1, path=self.test_dir)
        vector_store.save(path=self.test_dir)
        
        vector_store._loaded_paths.clear()
        vector_store._instances.clear()
        
        texts2 = ["third"]
        vectors2 = [[1.0, 1.0]]
        
        vector_store.add(texts2, vectors2, path=self.test_dir)
        
        results = vector_store.search([1.0, 1.0], top_k=3, path=self.test_dir)
        
        self.assertEqual(len(results), 3)


if __name__ == "__main__":
    unittest.main()
