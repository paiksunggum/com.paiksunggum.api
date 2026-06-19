from dataclasses import dataclass


@dataclass(frozen=True)
class PiperDashQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperDashResponse:
    id: int
    name: str
