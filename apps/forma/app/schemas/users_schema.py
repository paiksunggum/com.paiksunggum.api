from datetime import datetime

from pydantic import BaseModel, Field


class FormaUserCreateRequest(BaseModel):
    login_id: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    role: str = Field(default="user", min_length=1, max_length=32)


class FormaUserResponse(BaseModel):
    id: int
    login_id: str
    email: str
    name: str
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
