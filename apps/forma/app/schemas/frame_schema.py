from pydantic import BaseModel, Field


class FrameCreateRequest(BaseModel):
    video_id: int
    frame_index: int
    timestamp_sec: float = Field(ge=0)
    pose_json: str | None = None


class FrameResponse(BaseModel):
    id: int
    video_id: int
    frame_index: int
    timestamp_sec: float
    pose_json: str | None

    model_config = {"from_attributes": True}
