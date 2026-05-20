from pydantic import BaseModel, Field


class AdLinkCreateRequest(BaseModel):
    video_id: int
    ad_id: int
    placement_type: str = Field(default="description", max_length=30)
    start_sec: int | None = Field(default=None, ge=0)
    end_sec: int | None = Field(default=None, ge=0)


class AdLinkResponse(BaseModel):
    id: int
    video_id: int
    ad_id: int
    placement_type: str
    start_sec: int | None
    end_sec: int | None

    model_config = {"from_attributes": True}
