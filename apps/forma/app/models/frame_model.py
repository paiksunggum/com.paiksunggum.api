from sqlmodel import Field, SQLModel


class Frame(SQLModel, table=True):
    __tablename__ = "frames"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    video_id: int = Field(foreign_key="videos.id", index=True)
    frame_index: int = Field(index=True)
    timestamp_sec: float = Field(ge=0)
    pose_json: str | None = Field(default=None)
