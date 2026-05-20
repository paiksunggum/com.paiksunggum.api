from pydantic import BaseModel, Field


class SeedDemoCsvResponse(BaseModel):
    status: str = Field(
        ...,
        description="ok | already_seeded",
    )
    source: str = Field(
        ...,
        description="remote_csv | local_fallback | n/a",
    )
    csv_url: str | None = Field(
        default=None,
        description="사용한(또는 시도한) 원격 CSV 주소",
    )
    rows_used: int
    users_created: int = 0
    sports_created: int = 0
    videos_created: int = 0
    ads_created: int = 0
    ad_links_created: int = 0
    message: str | None = None
