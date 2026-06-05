from datetime import datetime

from sqlalchemy import CheckConstraint
from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Feedback(SQLModel, table=True):
    __tablename__ = "feedbacks"
    __table_args__ = (
        CheckConstraint(
            "(video_id IS NULL) <> (frame_id IS NULL)",
            name="ck_feedbacks_video_xor_frame",
        ),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    video_id: int | None = Field(default=None, foreign_key="videos.id", index=True)
    frame_id: int | None = Field(default=None, foreign_key="frames.id", index=True)
    source_type: str = Field(default="system", max_length=20)
    comment: str = Field(max_length=2000)
    score: float | None = Field(default=None, ge=0, le=100)
    created_at: datetime = Field(default_factory=now_utc)
