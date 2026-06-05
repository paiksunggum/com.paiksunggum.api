from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class FrameNestedCreateRequest(BaseModel):
    frame_index: int = Field(..., ge=0)
    timestamp_sec: float = Field(..., ge=0)
    keypoints: dict[str, Any] | None = None


class FrameResponse(BaseModel):
    id: int
    analysis_history_id: int
    video_id: int
    frame_index: int
    timestamp_sec: float
    keypoints: dict[str, Any] | None
    created_at: datetime

    model_config = {"from_attributes": True}
