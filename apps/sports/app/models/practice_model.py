from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Practice(SQLModel, table=True):
    __tablename__ = "practices"

    id: int | None = Field(default=None, primary_key=True)
    sports_id: int = Field(foreign_key="sports.id", index=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None)
    guide_json: dict | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=now_utc)
