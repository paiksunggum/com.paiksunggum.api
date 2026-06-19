from dataclasses import dataclass


@dataclass(frozen=True)
class PiperCeoQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperCeoResponse:
    id: int
    name: str
