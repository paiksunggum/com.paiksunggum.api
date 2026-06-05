from datetime import datetime

from pydantic import BaseModel, Field


class PaymentLogNestedCreateRequest(BaseModel):
    user_id: int
    amount_cents: int = Field(..., ge=0)
    currency: str = Field(default="KRW", max_length=3)
    pg_transaction_id: str = Field(..., min_length=1, max_length=100)
    status: str = Field(default="pending", max_length=20)
    paid_at: datetime | None = None


class PaymentLogCreateRequest(BaseModel):
    subscription_id: int
    user_id: int
    amount_cents: int = Field(..., ge=0)
    currency: str = Field(default="KRW", max_length=3)
    pg_transaction_id: str = Field(..., min_length=1, max_length=100)
    status: str = Field(default="pending", max_length=20)
    paid_at: datetime | None = None


class PaymentLogResponse(BaseModel):
    id: int
    subscription_id: int
    user_id: int
    amount_cents: int
    currency: str
    pg_transaction_id: str
    status: str
    paid_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
