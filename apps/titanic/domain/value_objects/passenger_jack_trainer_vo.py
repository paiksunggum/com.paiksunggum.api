# domain/value_objects.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass(frozen=True)
class PassengerId:
    """승객 식별자 VO — 빈 문자열 불가, 공백 정규화"""
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("PassengerId는 비어 있을 수 없습니다.")
        object.__setattr__(self, "value", self.value.strip())

    def __str__(self) -> str:
        return self.value


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Gender":
        mapping = {"male": cls.MALE, "female": cls.FEMALE}
        return mapping.get((raw or "").lower(), cls.UNKNOWN)


@dataclass(frozen=True)
class Age:
    """나이 VO — None 허용(미기재), 음수 불가"""
    value: Optional[float]

    def __post_init__(self):
        if self.value is not None and self.value < 0:
            raise ValueError(f"나이는 0 이상이어야 합니다: {self.value}")

    @property
    def is_minor(self) -> bool:
        return self.value is not None and self.value < 18

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else "미기재"


@dataclass(frozen=True)
class FamilyRelation:
    """형제/배우자 수 + 부모/자녀 수 묶음 VO"""
    sib_sp: int  # 형제·배우자
    parch: int   # 부모·자녀

    def __post_init__(self):
        if self.sib_sp < 0 or self.parch < 0:
            raise ValueError("가족 수는 음수가 될 수 없습니다.")

    @property
    def total(self) -> int:
        return self.sib_sp + self.parch

    @property
    def traveled_alone(self) -> bool:
        return self.total == 0


class SurvivedStatus(str, Enum):
    SURVIVED = "1"
    PERISHED = "0"
    UNKNOWN = "unknown"

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "SurvivedStatus":
        mapping = {"1": cls.SURVIVED, "0": cls.PERISHED}
        return mapping.get(raw or "", cls.UNKNOWN)

    @property
    def is_survived(self) -> bool:
        return self == self.SURVIVED