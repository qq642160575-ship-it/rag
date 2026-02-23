"""
input:
- raw_text: 原始文本

output:
- str: 清洗后的文本

pos:
- 位于 ingestion 层
- 负责文本清洗，不负责解析

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
import re


def clean_text(raw_text: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw_text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_empty_lines(text: str) -> str:
    return "\n".join(line for line in text.split("\n") if line.strip())
