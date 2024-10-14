from pydantic import BaseModel


class UnifiedInput(BaseModel):
    user_id: str
    text: str
    # 其他通用屬性


class UnifiedOutput(BaseModel):
    response_text: str
    # 其他通用屬性
