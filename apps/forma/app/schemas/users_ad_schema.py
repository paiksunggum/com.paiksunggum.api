from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class UsersAdNestedCreateRequest(BaseModel):
    ad_id: int
    contract_status: str = Field(default="active", max_length=20)
    allocated_budget: Decimal = Field(default=Decimal("0"), ge=0)
    started_at: datetime | None = None
    ended_at: datetime | None = None


class UsersAdResponse(BaseModel):
    id: int
    user_id: int
    ad_id: int
    contract_status: str
    allocated_budget: Decimal
    started_at: datetime
    ended_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
