from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiscordIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class DiscordIntroduceResult:
    id: int
    name: str
