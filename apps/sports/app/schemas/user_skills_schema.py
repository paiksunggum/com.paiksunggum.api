from datetime import datetime

from pydantic import BaseModel, Field


class UserSkillNestedCreateRequest(BaseModel):
    practice_id: int
    ai_level: int = Field(default=0, ge=0, le=100)
    coach_level: int = Field(default=0, ge=0, le=100)
    assessed_at: datetime | None = None


class UserSkillResponse(BaseModel):
    id: int
    user_id: int
    practice_id: int
    ai_level: int
    coach_level: int
    assessed_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
