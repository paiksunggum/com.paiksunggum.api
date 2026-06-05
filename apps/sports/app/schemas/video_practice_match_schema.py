from datetime import datetime

from pydantic import BaseModel, Field


class VideoPracticeMatchNestedCreateRequest(BaseModel):
    practice_id: int
    match_score: float | None = Field(default=None, ge=0, le=100)


class VideoPracticeMatchResponse(BaseModel):
    id: int
    video_id: int
    practice_id: int
    match_score: float | None
    created_at: datetime

    model_config = {"from_attributes": True}
