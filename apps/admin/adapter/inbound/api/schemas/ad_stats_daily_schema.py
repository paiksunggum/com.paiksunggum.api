from datetime import date, datetime

from pydantic import BaseModel, Field


class AdStatsDailySchema(BaseModel):
    
    id: int = Field(0, description="레코드 ID")
    ad_id: int = Field(1, description="광고 ID")
    stat_date: date = Field(description="집계 날짜")
    impressions: int = Field(0, description="노출 횟수")
    clicks: int = Field(0, description="클릭 횟수")
    created_at: datetime | None = Field(None, description="생성 시각")
    # 콜 성과 분석관 — 일별 광고 노출·클릭 집계

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "ad_id": 1,
                "stat_date": "2026-06-15",
                "impressions": 12000,
                "clicks": 340,
                "created_at": "2026-06-15T00:00:00Z",
            }
        }
    }
