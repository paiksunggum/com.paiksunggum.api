from datetime import datetime

from pydantic import BaseModel, Field


class PracticeCreateRequest(BaseModel):
    user_id: int
    sport_id: int
    video_id: int | None = None
    note: str | None = Field(default=None, max_length=1000)


class PracticeResponse(BaseModel):
    id: int
    user_id: int
    sport_id: int
    video_id: int | None
    note: str | None
    practiced_at: datetime

    model_config = {"from_attributes": True}
