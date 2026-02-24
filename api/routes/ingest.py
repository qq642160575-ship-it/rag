"""
input:
- form-data: 上传的文件
- query-params: 参数配置 (如 provider, chunk_size)

output:
- IngestResponse: 包含生成的 ID 列表

pos:
- 位于 api/routes 层
- 负责摄入业务路由分发

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
import os
import shutil
from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from typing import Optional
from pipeline.ingest_flow import ingest_file
from api.models.schemas import IngestResponse


router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/file", response_model=IngestResponse)
async def upload_and_ingest(
    file: UploadFile = File(...),
    chunk_size: int = Query(512, ge=100, le=2048),
    chunk_overlap: int = Query(50, ge=0),
    embed_provider: str = Query("openai"),
    store_provider: str = Query("faiss"),
    store_path: str = Query("./vector_store")
):
    """
    上传并直接摄入文件：文件 -> 向量库
    """
    # 1. 临时保存文件
    temp_dir = "temp_uploads"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    file_path = os.path.join(temp_dir, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. 调用 pipeline 执行摄入
        ids = ingest_file(
            file_path=file_path,
            store_path=store_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embed_provider=embed_provider,
            store_provider=store_provider
        )
        
        return IngestResponse(
            success=True,
            message=f"文件 {file.filename} 摄入完成",
            ids=ids,
            count=len(ids)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 清理临时文件
        if os.path.exists(file_path):
            os.remove(file_path)
