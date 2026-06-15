from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class PracticeQuery:

    sports_id: int
    title: str
    description: str | None
    guide_json: dict[str, Any] | None
    is_active: bool


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class PracticeResponse:

    id: int
    sports_id: int
    title: str
    description: str | None
    guide_json: dict[str, Any] | None
    is_active: bool
    created_at: datetime | None
