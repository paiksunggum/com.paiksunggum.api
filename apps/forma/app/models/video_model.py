from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Video(SQLModel, table=True):
    __tablename__ = "videos"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    user_id: int = Field(foreign_key="users.id", index=True)
    sport_id: int = Field(foreign_key="sports.id", index=True)
    title: str = Field(max_length=200)
    video_url: str = Field(max_length=1000)
    duration_sec: int | None = Field(default=None)
    visibility: str = Field(default="public", max_length=20)
    created_at: datetime = Field(default_factory=now_utc)
