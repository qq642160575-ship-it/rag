import os
import sys

# 将项目根目录添加到 python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.ingest_flow import ingest_file
from dotenv import load_dotenv

# 加载 .env 变量
load_dotenv()

def run_ingestion():
    file_path = "data/rag_paper.pdf"
    store_path = "data/vector_store_rag"
    
    print(f"开始摄入文件: {file_path}")
    
    try:
        # 尝试使用 local 嵌入（如果环境支持），否则默认 openai
        # 注意：如果使用 openai，请确保已设置 OPENAI_API_KEY
        ids = ingest_file(
            file_path=file_path,
            store_path=store_path,
            chunk_size=500,
            chunk_overlap=50,
            embed_provider="local", 
            store_provider="faiss"
        )
        print(f"摄入成功！共添加了 {len(ids)} 个数据块。")
        print(f"向量库已持久化到: {store_path}")
    except Exception as e:
        print(f"摄入失败: {e}")
        print("\n提示: 如果报错 'pypdf' missing，请运行 'pip install pypdf'")
        print("提示: 如果报错 API Key 问题，请检查 .env 文件或环境变量")

if __name__ == "__main__":
    run_ingestion()
