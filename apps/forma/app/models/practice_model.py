from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Practice(SQLModel, table=True):
    __tablename__ = "practices"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    user_id: int = Field(foreign_key="user.id", index=True)
    sport_id: int = Field(foreign_key="sports.id", index=True)
    video_id: int | None = Field(default=None, foreign_key="videos.id", index=True)
    note: str | None = Field(default=None, max_length=1000)
    practiced_at: datetime = Field(default_factory=now_utc)
