from datetime import datetime
from typing import Any

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Practice(SQLModel, table=True):
    __tablename__ = "practices"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    sports_id: int = Field(
        foreign_key="sports.id",
        index=True,
        sa_column_kwargs={"name": "sport_id"},
    )
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    guide_json: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True),
    )
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=now_utc)
