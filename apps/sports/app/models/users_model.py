"""공유 `users` 테이블 — Neon 기존 컬럼명(`user_id` 등)에 맞춘 모델."""

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    login_id: str = Field(
        max_length=255,
        unique=True,
        index=True,
        sa_column_kwargs={"name": "user_id"},
    )
    password_hash: str = Field(max_length=255)
    email: str = Field(max_length=255, index=True)
    name: str = Field(max_length=255)
    birthdate: str = Field(max_length=8)
    gender: str = Field(max_length=16)
    role: str = Field(max_length=32)

    @property
    def user_id(self) -> str:
        return self.login_id


__all__ = ["User"]
