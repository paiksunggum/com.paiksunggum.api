from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class AdLink(SQLModel, table=True):
    __tablename__ = "ad_links"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    video_id: int = Field(foreign_key="videos.id", index=True)
    ad_id: int = Field(foreign_key="ads.id", index=True)
    placement_type: str = Field(default="overlay", max_length=30)
    exposed_at: datetime = Field(default_factory=now_utc)
    created_at: datetime = Field(default_factory=now_utc)
