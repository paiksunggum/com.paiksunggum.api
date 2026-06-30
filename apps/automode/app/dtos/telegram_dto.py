from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TelegramIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class TelegramIntroduceResult:
    id: int
    name: str


@dataclass(frozen=True)
class TelegramSendCommand:
    text: str


@dataclass(frozen=True)
class TelegramSendResult:
    ok: bool
    message_id: int
