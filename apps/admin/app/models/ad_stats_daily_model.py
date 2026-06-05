from datetime import date, datetime

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class AdStatsDaily(SQLModel, table=True):
    __tablename__ = "ad_stats_daily"
    __table_args__ = (
        UniqueConstraint("ad_id", "stat_date", name="uq_ad_stats_daily_ad_date"),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    ad_id: int = Field(foreign_key="ads.id", index=True)
    stat_date: date
    impressions: int = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=now_utc)
