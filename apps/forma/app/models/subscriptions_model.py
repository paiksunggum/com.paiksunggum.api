from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    user_id: int = Field(foreign_key="users.id", index=True)
    plan_code: str = Field(max_length=50)
    status: str = Field(default="active", max_length=20)
    started_at: datetime = Field(default_factory=now_utc)
    ended_at: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=now_utc)
