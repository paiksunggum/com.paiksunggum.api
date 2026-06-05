from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class SubscriptionPlan(SQLModel, table=True):
    __tablename__ = "subscription_plans"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    plan_code: str = Field(max_length=50, unique=True, index=True)
    name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price_cents: int = Field(ge=0)
    currency: str = Field(default="KRW", max_length=3)
    billing_interval: str = Field(default="monthly", max_length=20)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=now_utc)
