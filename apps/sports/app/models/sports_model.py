from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Sports(SQLModel, table=True):
    __tablename__ = "sports"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: str | None = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=now_utc)
