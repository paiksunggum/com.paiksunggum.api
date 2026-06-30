from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JusoIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class JusoIntroduceResult:
    id: int
    name: str


@dataclass(frozen=True)
class JusoContactCommand:
    first_name: str
    middle_name: str
    last_name: str
    nickname: str
    organization_name: str
    organization_title: str
    birthday: str
    labels: str
    email: str
    phone: str


@dataclass(frozen=True)
class JusoContactUploadResult:
    inserted: int


@dataclass(frozen=True)
class JusoContactItem:
    name: str
    email: str
