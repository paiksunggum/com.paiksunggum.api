from __future__ import annotations
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ── Gender ────────────────────────────────────────────────────────────────────

class GenderType(str, Enum):
    MALE    = "male"
    FEMALE  = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Gender:
    """성별 VO (gender 컬럼)"""
    value: GenderType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Gender":
        mapping = {"male": GenderType.MALE, "female": GenderType.FEMALE}
        return cls(value=mapping.get((raw or "").lower(), GenderType.UNKNOWN))

    @property
    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    def __str__(self) -> str:
        return self.value.value


# ── Title ─────────────────────────────────────────────────────────────────────

class TitleType(str, Enum):
    MR      = "Mr"
    MISS    = "Miss"
    MRS     = "Mrs"
    MASTER  = "Master"
    ROYAL   = "Royal"
    RARE    = "Rare"
    UNKNOWN = "Unknown"


_RARE   = {"Capt", "Col", "Don", "Dr", "Major", "Rev", "Jonkheer", "Dona", "Mme"}
_ROYAL  = {"Countess", "Lady", "Sir"}
_RENAME = {"Mlle": "Miss", "Ms": "Miss"}
_ORDINAL: dict[TitleType, int] = {
    TitleType.MR: 1, TitleType.MISS: 2, TitleType.MRS: 3,
    TitleType.MASTER: 4, TitleType.ROYAL: 5, TitleType.RARE: 6, TitleType.UNKNOWN: 0,
}


@dataclass(frozen=True)
class Title:
    """호칭 VO (name 컬럼 파생 — 피처 엔지니어링)"""
    value: TitleType

    @classmethod
    def from_name(cls, name: Optional[str]) -> "Title":
        if not name:
            return cls(value=TitleType.UNKNOWN)
        match = re.search(r"([A-Za-z]+)\.", name)
        if not match:
            return cls(value=TitleType.UNKNOWN)
        raw = _RENAME.get(match.group(1), match.group(1))
        if raw in _RARE:
            return cls(value=TitleType.RARE)
        if raw in _ROYAL:
            return cls(value=TitleType.ROYAL)
        try:
            return cls(value=TitleType(raw))
        except ValueError:
            return cls(value=TitleType.UNKNOWN)

    @property
    def ordinal(self) -> int:
        return _ORDINAL[self.value]

    @property
    def is_female(self) -> bool:
        return self.value in (TitleType.MRS, TitleType.MISS)

    @property
    def is_minor(self) -> bool:
        return self.value == TitleType.MASTER

    def __str__(self) -> str:
        return self.value.value


# ── SocialProfile (임베디드 값 타입) ──────────────────────────────────────────

@dataclass(frozen=True)
class SocialProfile:
    """사회적 정체성 임베디드 값 타입 (Gender + Title).

    Gender와 Title은 함께 "이 사람이 누구인가"를 표현한다.
    생존 예측에서 가장 강력한 두 피처(0.54, 0.37)를 하나의 단위로 묶는다.
    """
    gender: Gender
    title: Title

    @classmethod
    def from_raw(cls, name_raw: Optional[str], gender_raw: Optional[str]) -> "SocialProfile":
        return cls(gender=Gender.from_raw(gender_raw), title=Title.from_name(name_raw))

    @property
    def is_female(self) -> bool:
        return self.gender.is_female

    @property
    def is_privileged(self) -> bool:
        return self.title.value in (TitleType.ROYAL, TitleType.RARE)

    @property
    def survival_priority(self) -> int:
        """'Women and children first' 원칙 기반 우선도 (높을수록 우선)"""
        if self.title.is_minor:
            return 3
        if self.is_female:
            return 2
        if self.is_privileged:
            return 1
        return 0

    def __str__(self) -> str:
        return f"{self.title} ({self.gender})"
