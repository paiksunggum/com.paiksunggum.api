from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Ad(SQLModel, table=True):
    __tablename__ = "ads"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    title: str = Field(max_length=200)
    image_url: str | None = Field(default=None, max_length=1000)
    target_url: str = Field(max_length=1000)
    budget: Decimal = Field(default=Decimal("0"))
    status: str = Field(default="active", max_length=20)
    created_at: datetime = Field(default_factory=now_utc)
