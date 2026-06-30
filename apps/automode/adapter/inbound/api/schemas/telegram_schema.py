from __future__ import annotations

from pydantic import BaseModel


class TelegramIntroduceResponseSchema(BaseModel):
    id: int
    name: str


class TelegramSendRequest(BaseModel):
    text: str


class TelegramSendResponse(BaseModel):
    ok: bool
    message_id: int
