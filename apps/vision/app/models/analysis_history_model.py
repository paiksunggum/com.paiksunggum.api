from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class AnalysisHistory(SQLModel, table=True):
    __tablename__ = "analysis_history"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    video_id: int = Field(foreign_key="videos.id", index=True)
    status: str = Field(default="PENDING", max_length=20)
    round_number: int = Field(default=1, ge=1)
    started_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=now_utc)
