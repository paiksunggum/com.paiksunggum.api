from dataclasses import dataclass


@dataclass(frozen=True)
class PiperCooQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperCooResponse:
    id: int
    name: str
