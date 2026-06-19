from dataclasses import dataclass


@dataclass(frozen=True)
class PiperSysQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperSysResponse:
    id: int
    name: str
