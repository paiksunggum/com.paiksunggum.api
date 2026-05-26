from datetime import date, datetime

from pydantic import BaseModel, Field


class FormaUserCreateRequest(BaseModel):
    login_id: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    birthdate: date = Field(default=date(1970, 1, 1))
    role: str = Field(default="user", min_length=1, max_length=32)


class FormaUserResponse(BaseModel):
    id: int
    login_id: str
    email: str
    name: str
    birthdate: date
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
