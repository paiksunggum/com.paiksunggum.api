from datetime import datetime

from pydantic import BaseModel, Field


class SubscriptionCreateRequest(BaseModel):
    subscriber_user_id: int
    creator_user_id: int
    status: str = Field(default="active", max_length=20)
    ended_at: datetime | None = None


class SubscriptionResponse(BaseModel):
    id: int
    subscriber_user_id: int
    creator_user_id: int
    status: str
    started_at: datetime
    ended_at: datetime | None

    model_config = {"from_attributes": True}
