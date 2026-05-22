from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class AdCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    target_url: str = Field(..., min_length=1, max_length=1000)
    image_url: str | None = Field(default=None, max_length=1000)
    budget: Decimal = Field(default=Decimal("0"), ge=0)
    status: str = Field(default="active", max_length=20)


class AdResponse(BaseModel):
    id: int
    title: str
    image_url: str | None
    target_url: str
    budget: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
