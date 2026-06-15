from datetime import datetime

from pydantic import BaseModel, Field


class PracticeSchema(BaseModel):

    id: int = Field(0, description="연습 항목 ID")
    sports_id: int = Field(1, description="대상 종목 ID")
    title: str = Field("직구 투구 자세", description="연습 항목 제목")
    description: str | None = Field(None, description="연습 설명")
    guide_json: dict | None = Field(None, description="자세 가이드 JSON")
    is_active: bool = Field(True, description="활성화 여부")
    created_at: datetime | None = Field(None, description="생성 시각")
    # 천 수석 코치 — 종목별 권장 자세 카탈로그

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "sports_id": 1,
                "title": "직구 투구 자세",
                "description": "팔꿈치 각도와 손목 스냅을 중심으로 한 직구 폼",
                "guide_json": {"phase": "wind-up", "key_points": ["팔꿈치 90도", "릴리즈 포인트"]},
                "is_active": True,
                "created_at": "2026-01-01T00:00:00Z",
            }
        }
    }