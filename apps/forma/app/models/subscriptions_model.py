from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    subscriber_user_id: int = Field(foreign_key="users.id", index=True)
    creator_user_id: int = Field(foreign_key="users.id", index=True)
    status: str = Field(default="active", max_length=20)
    started_at: datetime = Field(default_factory=now_utc)
    ended_at: datetime | None = Field(default=None)