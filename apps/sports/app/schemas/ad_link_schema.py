from datetime import datetime

from pydantic import BaseModel, Field


class AdExposureCreateRequest(BaseModel):
    ad_id: int
    placement_type: str = Field(default="overlay", max_length=30)
    exposed_at: datetime | None = None


class AdLinkResponse(BaseModel):
    id: int
    video_id: int
    ad_id: int
    placement_type: str
    exposed_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
