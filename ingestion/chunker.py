"""
input:
- file_path: 文档路径（支持 PDF/Word/TXT）
- chunk_size: 每个块的最大 token 数
- chunk_overlap: 块之间的重叠 token 数
- metadata: 文档元信息（来源、作者等）
- strategy: 切片策略 ("basic" 或 "semantic")

output:
- List[RawDocument]: 分块后的文档列表，包含元信息及父文档关联

pos:
- 位于 ingestion 层对外唯一入口
- 负责文档解析 + 文本分块，保留来源信息

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
from typing import List, Dict, Any, Optional, Literal
from core.schema import RawDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

from ingestion.parser import parse


def chunk(
    file_path: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    metadata: Optional[Dict[str, Any]] = None,
    strategy: Literal["basic", "semantic"] = "basic"
) -> List[RawDocument]:
    """
    统一切片入口：解析文档 + 切片
    
    Args:
        file_path: 文档路径
        chunk_size: 每个块的最大字符数
        chunk_overlap: 块之间的重叠字符数
        metadata: 文档元信息
        strategy: 切片策略 "basic" 或 "semantic"
    
    Returns:
        分块后的 RawDocument 列表
    """
    doc = parse(file_path)
    
    merged_metadata = doc.metadata.copy()
    if metadata:
        merged_metadata.update(metadata)
    
    if strategy == "semantic":
        return semantic_chunk_text(
            text=doc.content,
            max_chunk_size=chunk_size,
            metadata=merged_metadata,
            source=file_path,
            parent_id=doc.id
        )
    else:
        return chunk_text(
            text=doc.content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            metadata=merged_metadata,
            source=file_path,
            parent_id=doc.id
        )


def clean_text_for_chunking(text: str) -> str:
    """
    清洗文本，去除空行和特殊字符
    
    Args:
        text: 原始文本
    
    Returns:
        清洗后的文本
    """
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)


def chunk_text(
    text: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    metadata: Optional[Dict[str, Any]] = None,
    source: Optional[str] = None,
    parent_id: Optional[str] = None
) -> List[RawDocument]:
    """
    将文本按 token 分块，保留来源信息
    
    Args:
        text: 待分块的文本
        chunk_size: 每个块的最大字符数（近似 token 数）
        chunk_overlap: 块之间的重叠字符数
        metadata: 文档元信息
        source: 文档来源路径
        parent_id: 父文档 ID
    
    Returns:
        分块后的 RawDocument 列表，每个块包含元信息
    """
    cleaned_text = clean_text_for_chunking(text)
    
    if not cleaned_text:
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", ". ", "! ", "? ", "；", "; ", "，", ", ", " ", ""],
        is_separator_regex=False
    )
    
    chunks = text_splitter.split_text(cleaned_text)
    
    base_metadata = metadata.copy() if metadata else {}
    if source:
        base_metadata["source"] = source
    if parent_id:
        base_metadata["parent_id"] = parent_id
    
    documents = []
    for i, chunk in enumerate(chunks):
        chunk_metadata = base_metadata.copy()
        chunk_metadata["chunk_index"] = i
        chunk_metadata["total_chunks"] = len(chunks)
        chunk_metadata["chunk_size"] = len(chunk)
        
        doc = RawDocument(
            content=chunk,
            metadata=chunk_metadata
        )
        documents.append(doc)
    
    return documents


def chunk_documents(
    documents: List[RawDocument],
    chunk_size: int = 512,
    chunk_overlap: int = 50
) -> List[RawDocument]:
    """
    对多个文档进行分块处理
    
    Args:
        documents: RawDocument 文档列表
        chunk_size: 每个块的最大字符数
        chunk_overlap: 块之间的重叠字符数
    
    Returns:
        分块后的 RawDocument 列表
    """
    all_chunks = []
    
    for doc in documents:
        chunks = chunk_text(
            text=doc.content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            metadata=doc.metadata,
            source=doc.metadata.get("source"),
            parent_id=doc.id
        )
        all_chunks.extend(chunks)
    
    return all_chunks


def semantic_chunk_text(
    text: str,
    max_chunk_size: int = 512,
    metadata: Optional[Dict[str, Any]] = None,
    source: Optional[str] = None,
    parent_id: Optional[str] = None
) -> List[RawDocument]:
    """
    语义分块：优先按段落和句子边界切分
    
    Args:
        text: 待分块的文本
        max_chunk_size: 每个块的最大字符数
        metadata: 文档元信息
        source: 文档来源路径
        parent_id: 父文档 ID
    
    Returns:
        语义分块后的 RawDocument 列表
    """
    cleaned_text = clean_text_for_chunking(text)
    
    if not cleaned_text:
        return []
    
    paragraphs = cleaned_text.split('\n\n')
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        para_size = len(para)
        
        if current_size + para_size <= max_chunk_size:
            current_chunk.append(para)
            current_size += para_size + 2
        else:
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
            
            if para_size > max_chunk_size:
                sentences = re.split(r'([。！？.!?])', para)
                sentence_pairs = [''.join(sentences[i:i+2]) for i in range(0, len(sentences)-1, 2)]
                if len(sentences) % 2 == 1:
                    sentence_pairs.append(sentences[-1])
                
                temp_chunk = []
                temp_size = 0
                for sent in sentence_pairs:
                    sent = sent.strip()
                    if not sent:
                        continue
                    sent_size = len(sent)
                    if temp_size + sent_size <= max_chunk_size:
                        temp_chunk.append(sent)
                        temp_size += sent_size
                    else:
                        if temp_chunk:
                            chunks.append(''.join(temp_chunk))
                        temp_chunk = [sent]
                        temp_size = sent_size
                
                if temp_chunk:
                    chunks.append(''.join(temp_chunk))
                
                current_chunk = []
                current_size = 0
            else:
                current_chunk = [para]
                current_size = para_size + 2
    
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    base_metadata = metadata.copy() if metadata else {}
    if source:
        base_metadata["source"] = source
    if parent_id:
        base_metadata["parent_id"] = parent_id
    base_metadata["chunking_strategy"] = "semantic"
    
    documents = []
    for i, chunk in enumerate(chunks):
        chunk_metadata = base_metadata.copy()
        chunk_metadata["chunk_index"] = i
        chunk_metadata["total_chunks"] = len(chunks)
        chunk_metadata["chunk_size"] = len(chunk)
        
        doc = RawDocument(
            content=chunk,
            metadata=chunk_metadata
        )
        documents.append(doc)
    
    return documents
