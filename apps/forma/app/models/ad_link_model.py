from sqlmodel import Field, SQLModel


class AdLink(SQLModel, table=True):
    __tablename__ = "ad_links"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    video_id: int = Field(foreign_key="videos.id", index=True)
    ad_id: int = Field(foreign_key="ads.id", index=True)
    placement_type: str = Field(default="description", max_length=30)
    start_sec: int | None = Field(default=None, ge=0)
    end_sec: int | None = Field(default=None, ge=0)
