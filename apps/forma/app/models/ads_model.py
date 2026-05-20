from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Ad(SQLModel, table=True):
    __tablename__ = "ads"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    owner_user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    product_url: str = Field(max_length=1000)
    image_url: str | None = Field(default=None, max_length=1000)
    status: str = Field(default="active", max_length=20)
    created_at: datetime = Field(default_factory=now_utc)
