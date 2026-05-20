from datetime import datetime

from pydantic import BaseModel, Field


class VideoCreateRequest(BaseModel):
    user_id: int
    sport_id: int
    title: str = Field(..., min_length=1, max_length=200)
    video_url: str = Field(..., min_length=1, max_length=1000)
    duration_sec: int | None = Field(default=None, ge=0)
    visibility: str = Field(default="public", max_length=20)


class VideoResponse(BaseModel):
    id: int
    user_id: int
    sport_id: int
    title: str
    video_url: str
    duration_sec: int | None
    visibility: str
    created_at: datetime

    model_config = {"from_attributes": True}
