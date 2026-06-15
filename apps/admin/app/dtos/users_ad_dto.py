from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class UsersAdQuery:

    user_id: int
    ad_id: int
    contract_status: str
    allocated_budget: Decimal
    started_at: datetime | None
    ended_at: datetime | None


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class UsersAdResponse:

    id: int
    user_id: int
    ad_id: int
    contract_status: str
    allocated_budget: Decimal
    started_at: datetime | None
    ended_at: datetime | None
    created_at: datetime | None
