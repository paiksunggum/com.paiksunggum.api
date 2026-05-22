from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class UsersAd(SQLModel, table=True):
    __tablename__ = "users_ad"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    user_id: int = Field(foreign_key="users.id", index=True)
    ad_id: int = Field(foreign_key="ads.id", index=True)
    contract_status: str = Field(default="active", max_length=20)
    allocated_budget: Decimal = Field(default=Decimal("0"))
    started_at: datetime = Field(default_factory=now_utc)
    ended_at: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=now_utc)
