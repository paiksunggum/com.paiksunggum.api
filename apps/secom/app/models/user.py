from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    login_id: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    email: str = Field(max_length=255, index=True)
    name: str = Field(max_length=255)
    birthdate: str = Field(max_length=8)
    gender: str = Field(max_length=16)
    role: str = Field(max_length=32)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    @property
    def user_id(self) -> str:
        """API·스키마 호환용 (DB 컬럼은 login_id)."""
        return self.login_id
