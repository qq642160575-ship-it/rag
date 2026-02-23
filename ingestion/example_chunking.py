"""
示例：完整的文档摄入与分块流程

演示如何：
1. 解析文档（PDF/Word/TXT）
2. 清洗文本
3. 分块处理
4. 保留元信息

面试要点：
- 语义切分：优先按段落和句子边界切分，保持语义完整性
- 元信息保留：追踪文档来源、块索引，便于后续检索溯源
- 灵活分块：支持 token 分块和语义分块两种策略
"""
from ingestion.parser import parse
from ingestion.chunker import chunk_text, semantic_chunk_text, chunk_documents
from langchain_core.documents import Document


def example_basic_chunking():
    """示例 1：基本的文档解析和分块"""
    print("=" * 50)
    print("示例 1：基本文档解析和分块")
    print("=" * 50)
    
    file_path = "data/sample.pdf"
    
    raw_text = parse(file_path)
    print(f"解析后文本长度: {len(raw_text)} 字符")
    
    chunks = chunk_text(
        text=raw_text,
        chunk_size=512,
        chunk_overlap=50,
        source=file_path,
        metadata={"author": "张三", "category": "技术文档"}
    )
    
    print(f"分块数量: {len(chunks)}")
    print(f"\n第一个块:")
    print(f"  内容: {chunks[0].page_content[:100]}...")
    print(f"  元信息: {chunks[0].metadata}")


def example_semantic_chunking():
    """示例 2：语义分块"""
    print("\n" + "=" * 50)
    print("示例 2：语义分块（按段落和句子）")
    print("=" * 50)
    
    text = """
    第一章 人工智能概述
    
    人工智能（AI）是计算机科学的一个分支。它致力于开发能够模拟人类智能的系统。
    这些系统可以执行学习、推理和自我修正等任务。
    
    第二章 机器学习基础
    
    机器学习是人工智能的核心技术之一。它使计算机能够从数据中学习。
    通过训练模型，系统可以识别模式并做出预测。
    
    第三章 深度学习
    
    深度学习是机器学习的一个子集。它使用多层神经网络来处理复杂数据。
    深度学习在图像识别、自然语言处理等领域取得了突破性进展。
    """
    
    chunks = semantic_chunk_text(
        text=text,
        max_chunk_size=200,
        metadata={"title": "AI 教程", "version": "1.0"},
        source="ai_tutorial.txt"
    )
    
    print(f"语义分块数量: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        print(f"\n块 {i + 1}:")
        print(f"  长度: {chunk.metadata['chunk_size']} 字符")
        print(f"  策略: {chunk.metadata['chunking_strategy']}")
        print(f"  内容预览: {chunk.page_content[:80]}...")


def example_batch_chunking():
    """示例 3：批量文档分块"""
    print("\n" + "=" * 50)
    print("示例 3：批量文档分块")
    print("=" * 50)
    
    documents = [
        Document(
            page_content="文档1的内容。" * 100,
            metadata={"source": "doc1.pdf", "author": "作者A"}
        ),
        Document(
            page_content="文档2的内容。" * 100,
            metadata={"source": "doc2.pdf", "author": "作者B"}
        ),
        Document(
            page_content="文档3的内容。" * 100,
            metadata={"source": "doc3.pdf", "author": "作者C"}
        ),
    ]
    
    all_chunks = chunk_documents(
        documents=documents,
        chunk_size=256,
        chunk_overlap=30
    )
    
    print(f"总文档数: {len(documents)}")
    print(f"总分块数: {len(all_chunks)}")
    
    for source in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
        source_chunks = [c for c in all_chunks if c.metadata.get("source") == source]
        print(f"\n{source}: {len(source_chunks)} 个块")


def example_metadata_tracking():
    """示例 4：元信息追踪（面试重点）"""
    print("\n" + "=" * 50)
    print("示例 4：元信息追踪（检索溯源）")
    print("=" * 50)
    
    text = "这是一个测试文档。" * 50
    
    chunks = chunk_text(
        text=text,
        chunk_size=100,
        chunk_overlap=20,
        source="/data/reports/2024_Q1_report.pdf",
        metadata={
            "author": "李四",
            "department": "研发部",
            "date": "2024-01-15",
            "classification": "内部"
        }
    )
    
    print(f"分块数量: {len(chunks)}")
    print("\n每个块的完整元信息:")
    for chunk in chunks[:2]:
        print(f"\n块 {chunk.metadata['chunk_index'] + 1}:")
        for key, value in chunk.metadata.items():
            print(f"  {key}: {value}")
    
    print("\n面试要点：")
    print("1. source 字段：记录文档来源，便于检索后溯源")
    print("2. chunk_index：标记块在原文档中的位置")
    print("3. total_chunks：了解文档被分成多少块")
    print("4. 自定义元信息：可添加作者、部门、日期等业务字段")


def example_interview_points():
    """面试要点总结"""
    print("\n" + "=" * 50)
    print("面试要点总结")
    print("=" * 50)
    
    print("""
    1. 语义切分的优势：
       - 保持段落和句子的完整性
       - 避免在句子中间切断，提高语义连贯性
       - 优先按段落分块，超长段落再按句子切分
    
    2. 元信息保留的重要性：
       - source: 记录文档来源，检索后可以溯源到原文件
       - chunk_index: 标记块的位置，可以定位到原文档的具体部分
       - 自定义字段: 可添加作者、日期、分类等业务元信息
       - 便于后续的权限控制、结果过滤、来源展示
    
    3. 分块策略选择：
       - token 分块: 适合长文本，保证每块大小均匀
       - 语义分块: 适合结构化文档，保持语义完整性
       - 可根据文档类型和业务需求灵活选择
    
    4. 文本清洗的必要性：
       - 去除空行和多余空白，减少噪声
       - 移除特殊控制字符，避免编码问题
       - 规范化文本格式，提高向量化质量
    
    5. 生产级考虑：
       - chunk_overlap: 块之间有重叠，避免语义在边界处丢失
       - 可配置的分块大小，适应不同的模型和场景
       - 批量处理能力，提高大规模文档处理效率
    """)


if __name__ == "__main__":
    example_basic_chunking()
    example_semantic_chunking()
    example_batch_chunking()
    example_metadata_tracking()
    example_interview_points()
