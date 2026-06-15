from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class SportsQuery:

    name: str
    description: str | None
    is_active: bool


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class SportsResponse:

    id: int
    name: str
    description: str | None
    is_active: bool
    created_at: datetime | None
