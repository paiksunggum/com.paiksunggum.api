from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class UsersAdSchema(BaseModel):
    
    id: int = Field(0, description="계약 ID")
    user_id: int = Field(0, description="유저 ID")
    ad_id: int = Field(1, description="광고 ID")
    contract_status: str = Field("active", description="계약 상태")
    allocated_budget: Decimal = Field(Decimal("0"), description="배정 예산")
    started_at: datetime | None = Field(None, description="계약 시작 시각")
    ended_at: datetime | None = Field(None, description="계약 종료 시각")
    created_at: datetime | None = Field(None, description="생성 시각")
    # 모건 어카운트 매니저 — 유저별 광고 계약·집행

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 42,
                "ad_id": 1,
                "contract_status": "active",
                "allocated_budget": "100000.00",
                "started_at": "2026-01-01T00:00:00Z",
                "ended_at": "2026-12-31T23:59:59Z",
                "created_at": "2026-01-01T00:00:00Z",
            }
        }
    }
