from __future__ import annotations

from pydantic import BaseModel, Field


class JusoIntroduceResponseSchema(BaseModel):
    id: int
    name: str


class JusoContactSchema(BaseModel):
    """Google 주소록 CSV 한 행"""

    first_name: str | None = Field(None)
    middle_name: str | None = Field(None)
    last_name: str | None = Field(None)
    nickname: str | None = Field(None)
    organization_name: str | None = Field(None)
    organization_title: str | None = Field(None)
    birthday: str | None = Field(None)
    labels: str | None = Field(None)
    email_1_value: str | None = Field(None)
    phone_1_value: str | None = Field(None)

    model_config = {"populate_by_name": True}


class JusoContactUploadResponse(BaseModel):
    inserted: int
    file_name: str
    columns: list[str]
    data_row_count: int


class JusoContactItemSchema(BaseModel):
    name: str
    email: str
