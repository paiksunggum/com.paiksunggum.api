from __future__ import annotations

from pydantic import BaseModel


class EmailSendSchema(BaseModel):
    to: str
    prompt: str
    to_name: str = ""


class EmailSendResponseSchema(BaseModel):
    to: str
    subject: str
    success: bool


class EmailClassifySchema(BaseModel):
    subject: str
    body: str


class EmailClassifyResponseSchema(BaseModel):
    category: str
    matched_keywords: list[str]
    is_spam: bool


class EmailIntroduceResponseSchema(BaseModel):
    id: int
    name: str
