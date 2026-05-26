from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackNestedCreateRequest(BaseModel):
    frame_id: int | None = None
    source_type: str = Field(default="system", max_length=20)
    comment: str = Field(..., min_length=1, max_length=2000)
    score: float | None = Field(default=None, ge=0, le=100)


class FeedbackResponse(BaseModel):
    id: int
    video_id: int | None
    frame_id: int | None
    source_type: str
    comment: str
    score: float | None
    created_at: datetime

    model_config = {"from_attributes": True}
