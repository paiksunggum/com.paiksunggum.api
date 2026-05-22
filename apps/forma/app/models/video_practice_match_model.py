from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class VideoPracticeMatch(SQLModel, table=True):
    __tablename__ = "video_practice_match"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    video_id: int = Field(foreign_key="videos.id", index=True)
    practice_id: int = Field(foreign_key="practices.id", index=True)
    match_score: float | None = Field(default=None, ge=0, le=100)
    created_at: datetime = Field(default_factory=now_utc)
