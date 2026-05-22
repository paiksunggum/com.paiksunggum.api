from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Video(SQLModel, table=True):
    __tablename__ = "videos"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    user_id: int = Field(foreign_key="users.id", index=True)
    sports_id: int = Field(
        foreign_key="sports.id",
        index=True,
        sa_column_kwargs={"name": "sport_id"},
    )
    title: str = Field(max_length=200)
    storage_url: str = Field(
        max_length=1000,
        sa_column_kwargs={"name": "video_url"},
    )
    duration_sec: int | None = Field(default=None)
    visibility: str = Field(default="public", max_length=20)
    created_at: datetime = Field(default_factory=now_utc)
