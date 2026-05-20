from datetime import datetime

from pydantic import BaseModel, Field


class AdCreateRequest(BaseModel):
    owner_user_id: int
    title: str = Field(..., min_length=1, max_length=200)
    product_url: str = Field(..., min_length=1, max_length=1000)
    image_url: str | None = Field(default=None, max_length=1000)
    status: str = Field(default="active", max_length=20)


class AdResponse(BaseModel):
    id: int
    owner_user_id: int
    title: str
    product_url: str
    image_url: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
