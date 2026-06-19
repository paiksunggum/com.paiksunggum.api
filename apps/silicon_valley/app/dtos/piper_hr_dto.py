from dataclasses import dataclass


@dataclass(frozen=True)
class PiperHrQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperHrResponse:
    id: int
    name: str
