from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Feedback(SQLModel, table=True):
    __tablename__ = "feedbacks"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    video_id: int = Field(foreign_key="videos.id", index=True)
    frame_id: int | None = Field(default=None, foreign_key="frames.id", index=True)
    source_type: str = Field(default="system", max_length=20)
    comment: str = Field(max_length=1000)
    score: float | None = Field(default=None, ge=0, le=100)
    created_at: datetime = Field(default_factory=now_utc)
