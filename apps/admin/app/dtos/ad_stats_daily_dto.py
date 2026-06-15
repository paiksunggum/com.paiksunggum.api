from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class AdStatsDailyQuery:

    ad_id: int
    stat_date: date
    impressions: int
    clicks: int


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class AdStatsDailyResponse:

    id: int
    ad_id: int
    stat_date: date
    impressions: int
    clicks: int
    created_at: datetime | None
