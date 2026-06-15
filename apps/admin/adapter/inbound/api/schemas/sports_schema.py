from datetime import datetime

from pydantic import BaseModel, Field


class SportsSchema(BaseModel):
    
    id: int = Field(0, description="종목 ID")
    name: str = Field("야구", description="종목명")
    description: str | None = Field(None, description="종목 설명")
    is_active: bool = Field(True, description="활성화 여부")
    created_at: datetime | None = Field(None, description="생성 시각")
    # 해리스 국장 — 스포츠 종목 마스터

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "야구",
                "description": "9이닝으로 구성된 팀 스포츠",
                "is_active": True,
                "created_at": "2026-01-01T00:00:00Z",
            }
        }
    }
