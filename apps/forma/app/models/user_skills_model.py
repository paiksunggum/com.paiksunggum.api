from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class UserSkill(SQLModel, table=True):
    __tablename__ = "user_skills"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    user_id: int = Field(foreign_key="users.id", index=True)
    practice_id: int = Field(foreign_key="practices.id", index=True)
    ai_level: int = Field(default=0, ge=0, le=100)
    coach_level: int = Field(default=0, ge=0, le=100)
    assessed_at: datetime = Field(default_factory=now_utc)
    created_at: datetime = Field(default_factory=now_utc)
