from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisHistoryStartRequest(BaseModel):
    status: str = Field(default="PENDING", pattern="^(PENDING|SUCCESS|FAILED)$")
    round_number: int = Field(default=1, ge=1)
    started_at: datetime | None = None
    completed_at: datetime | None = None


class AnalysisHistoryUpdateRequest(BaseModel):
    status: str | None = Field(default=None, pattern="^(PENDING|SUCCESS|FAILED)$")
    started_at: datetime | None = None
    completed_at: datetime | None = None


class AnalysisHistoryResponse(BaseModel):
    id: int
    video_id: int
    status: str
    round_number: int
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
