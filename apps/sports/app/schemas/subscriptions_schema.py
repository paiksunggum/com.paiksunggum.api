from datetime import datetime

from pydantic import BaseModel, Field


class SubscriptionNestedCreateRequest(BaseModel):
    plan_code: str = Field(..., min_length=1, max_length=50)
    status: str = Field(default="active", max_length=20)
    ended_at: datetime | None = None


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_code: str
    status: str
    started_at: datetime
    ended_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
