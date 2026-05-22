from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PracticeCreateRequest(BaseModel):
    sports_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    guide_json: dict[str, Any] | None = None
    is_active: bool = True


class PracticeResponse(BaseModel):
    id: int
    sports_id: int
    title: str
    description: str | None
    guide_json: dict[str, Any] | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
