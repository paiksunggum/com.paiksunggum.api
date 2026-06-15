from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class AdsSchema(BaseModel):

    id: int = Field(0, description="광고 ID")
    title: str = Field("나이키 에어맥스 캠페인", description="광고 제목")
    image_url: str | None = Field(None, description="배너 이미지 URL")
    target_url: str = Field("https://example.com", description="랜딩 URL")
    budget: Decimal = Field(Decimal("0"), description="총 광고 예산")
    status: str = Field("active", description="광고 상태")
    created_at: datetime | None = Field(None, description="생성 시각")
    # 스털링 광고 국장 — 광고·상품 메타데이터

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "나이키 에어맥스 캠페인",
                "image_url": "https://cdn.nike.com/banner.png",
                "target_url": "https://nike.com/airmax",
                "budget": "500000.00",
                "status": "active",
                "created_at": "2026-01-01T00:00:00Z",
            }
        }
    }