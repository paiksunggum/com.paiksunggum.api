from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class Ads(SQLModel, table=True):
    __tablename__ = "ads"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    image_url: str | None = Field(default=None, max_length=500)
    target_url: str = Field(max_length=500)
    budget: Decimal = Field(default=Decimal("0"), decimal_places=2, max_digits=14)
    status: str = Field(default="active", max_length=30)
    created_at: datetime = Field(default_factory=now_utc)
