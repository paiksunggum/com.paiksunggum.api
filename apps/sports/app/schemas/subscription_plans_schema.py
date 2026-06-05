from datetime import datetime

from pydantic import BaseModel, Field


class SubscriptionPlanCreateRequest(BaseModel):
    plan_code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price_cents: int = Field(..., ge=0)
    currency: str = Field(default="KRW", max_length=3)
    billing_interval: str = Field(default="monthly", max_length=20)
    is_active: bool = True


class SubscriptionPlanResponse(BaseModel):
    id: int
    plan_code: str
    name: str
    description: str | None
    price_cents: int
    currency: str
    billing_interval: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
