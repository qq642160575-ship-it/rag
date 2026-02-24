"""
input:
- system-config: 系统配置环境变量

output:
- app: FastAPI 实例

pos:
- 位于 api 层入口
- 负责系统启动、路由挂载与生命周期管理

声明：
- 一旦本文件逻辑更新
- 必须同步更新本文件注释
- 并更新所属目录的 README.md
"""
import uvicorn
from fastapi import FastAPI
from api.routes import ingest


app = FastAPI(
    title="Laper AI RAG API",
    description="生产级 RAG 系统全流水线接口",
    version="0.1.0"
)


# 挂载路由
app.include_router(ingest.router, prefix="/api/v1")


@app.get("/")
async def root():
    """健康检查"""
    return {"status": "ok", "message": "Welcome to Laper AI RAG API"}


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
