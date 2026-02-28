from pydantic import BaseModel
# =========================
# 强类型输出定义 (Pydantic Models)
# =========================

class IntentOutput(BaseModel):
    task_type: enumerate['search', 'chat', 'write']
