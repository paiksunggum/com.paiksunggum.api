from __future__ import annotations

from pydantic import BaseModel


class EmailSendSchema(BaseModel):
    to: str
    prompt: str


class EmailSendResponseSchema(BaseModel):
    to: str
    subject: str
    success: bool
