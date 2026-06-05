from datetime import date

from pydantic import BaseModel, Field, field_validator


class FormaUserCreateRequest(BaseModel):
    login_id: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    birthdate: date | str = Field(default=date(1970, 1, 1))
    gender: str = Field(default="none", max_length=16)
    role: str = Field(default="user", min_length=1, max_length=32)

    @field_validator("birthdate", mode="before")
    @classmethod
    def normalize_birthdate(cls, value: date | str) -> str:
        if isinstance(value, date):
            return value.strftime("%Y%m%d")
        raw = str(value).strip()
        if len(raw) == 10 and raw[4] == "-":
            return f"{raw[:4]}{raw[5:7]}{raw[8:10]}"
        return raw


class FormaUserResponse(BaseModel):
    id: int
    login_id: str
    email: str
    name: str
    birthdate: str
    gender: str
    role: str

    model_config = {"from_attributes": True}
