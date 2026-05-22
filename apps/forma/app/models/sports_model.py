from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Sport(SQLModel, table=True):
    __tablename__ = "sports"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    name: str = Field(max_length=100, unique=True, index=True)
    description: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=now_utc)
