from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class PaymentLog(SQLModel, table=True):
    __tablename__ = "payment_logs"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    subscription_id: int = Field(foreign_key="subscriptions.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    amount_cents: int = Field(ge=0)
    currency: str = Field(default="KRW", max_length=3)
    pg_transaction_id: str = Field(max_length=100)
    status: str = Field(default="pending", max_length=20)
    paid_at: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=now_utc)
