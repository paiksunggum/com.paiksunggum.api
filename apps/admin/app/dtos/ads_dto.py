from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class AdsQuery:

    title: str
    image_url: str | None
    target_url: str
    budget: Decimal
    status: str


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class AdsResponse:

    id: int
    title: str
    image_url: str | None
    target_url: str
    budget: Decimal
    status: str
    created_at: datetime | None
