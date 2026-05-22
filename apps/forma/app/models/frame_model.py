from datetime import datetime
from typing import Any

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Frame(SQLModel, table=True):
    __tablename__ = "frames"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    analysis_history_id: int = Field(foreign_key="analysis_history.id", index=True)
    video_id: int = Field(foreign_key="videos.id", index=True)
    frame_index: int = Field(index=True)
    timestamp_sec: float = Field(ge=0)
    keypoints: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(JSONB, nullable=True),
    )
    created_at: datetime = Field(default_factory=now_utc)
