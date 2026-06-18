from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SurvivedType(str, Enum):
    SURVIVED = "1"
    PERISHED = "0"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SurvivedStatus:
    """생존 여부 VO (survived 컬럼 — 0=사망, 1=생존)"""
    value: SurvivedType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "SurvivedStatus":
        mapping = {"1": SurvivedType.SURVIVED, "0": SurvivedType.PERISHED}
        return cls(value=mapping.get(raw or "", SurvivedType.UNKNOWN))

    @property
    def is_survived(self) -> bool:
        return self.value == SurvivedType.SURVIVED

    def __str__(self) -> str:
        return self.value.value
