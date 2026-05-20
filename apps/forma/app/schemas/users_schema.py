from datetime import datetime

from pydantic import BaseModel, Field


class FormaUserCreateRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(default="user", min_length=1, max_length=30)


class FormaUserResponse(BaseModel):
    id: int
    user_id: str
    email: str
    name: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
