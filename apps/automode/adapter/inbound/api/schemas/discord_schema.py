from __future__ import annotations

from pydantic import BaseModel


class DiscordIntroduceResponseSchema(BaseModel):
    id: int
    name: str
