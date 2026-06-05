from datetime import date, datetime

from pydantic import BaseModel, Field


class AdStatsDailyNestedCreateRequest(BaseModel):
    stat_date: date
    impressions: int = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)


class AdStatsDailyCreateRequest(BaseModel):
    ad_id: int
    stat_date: date
    impressions: int = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)


class AdStatsDailyResponse(BaseModel):
    id: int
    ad_id: int
    stat_date: date
    impressions: int
    clicks: int
    created_at: datetime

    model_config = {"from_attributes": True}
