from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ── PClass ────────────────────────────────────────────────────────────────────

class PClassType(int, Enum):
    FIRST  = 1
    SECOND = 2
    THIRD  = 3


@dataclass(frozen=True)
class PClass:
    """티켓 등급 VO (pclass 컬럼)"""
    value: PClassType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "PClass":
        if raw is None or str(raw).strip() == "":
            raise ValueError("PClass는 필수 값입니다.")
        try:
            return cls(value=PClassType(int(str(raw).strip())))
        except (ValueError, KeyError):
            raise ValueError(f"PClass 유효하지 않은 값: '{raw}'")

    @property
    def is_first_class(self) -> bool:
        return self.value == PClassType.FIRST

    def __str__(self) -> str:
        return str(self.value.value)


# ── CabinZone ─────────────────────────────────────────────────────────────────

class CabinZoneType(str, Enum):
    A = "A"; B = "B"; C = "C"; D = "D"
    E = "E"; F = "F"; G = "G"; T = "T"
    UNKNOWN = "U"


@dataclass(frozen=True)
class CabinZone:
    """객실 구역 VO (cabin 컬럼 첫 글자 — 피처 엔지니어링)"""
    value: CabinZoneType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "CabinZone":
        if not raw or not str(raw).strip():
            return cls(value=CabinZoneType.UNKNOWN)
        first = str(raw).strip()[0].upper()
        zone = CabinZoneType(first) if first in CabinZoneType._value2member_map_ else CabinZoneType.UNKNOWN
        return cls(value=zone)

    @property
    def is_known(self) -> bool:
        return self.value != CabinZoneType.UNKNOWN

    def __str__(self) -> str:
        return self.value.value


# ── Fare ──────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Fare:
    """요금 VO (fare 컬럼)"""
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"요금은 0 이상이어야 합니다: {self.value}")

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Fare":
        if raw is None or str(raw).strip() == "":
            return cls(value=0.0)
        try:
            return cls(value=float(str(raw).strip()))
        except ValueError:
            raise ValueError(f"Fare 유효하지 않은 값: '{raw}'")

    @property
    def tier(self) -> str:
        if self.value == 0:   return "무료"
        if self.value < 10:   return "저가"
        if self.value < 30:   return "중가"
        if self.value < 100:  return "고가"
        return "최고가"

    def __str__(self) -> str:
        return f"£{self.value:.2f}"


# ── TravelClass (임베디드 값 타입) ────────────────────────────────────────────

@dataclass(frozen=True)
class TravelClass:
    """여행 조건 임베디드 값 타입 (PClass + CabinZone + Fare).

    세 값은 모두 승객의 경제적 지위와 탑승 조건을 표현한다.
    생존 예측 3~5위 피처(0.34, 0.29, 0.26)를 하나의 개념 단위로 묶는다.
    """
    pclass:     PClass
    cabin_zone: CabinZone
    fare:       Fare

    @classmethod
    def from_raw(
        cls,
        pclass_raw: Optional[str],
        cabin_raw:  Optional[str],
        fare_raw:   Optional[str],
    ) -> "TravelClass":
        return cls(
            pclass=PClass.from_raw(pclass_raw),
            cabin_zone=CabinZone.from_raw(cabin_raw),
            fare=Fare.from_raw(fare_raw),
        )

    @property
    def is_upper_deck(self) -> bool:
        return self.cabin_zone.value in (CabinZoneType.A, CabinZoneType.B, CabinZoneType.C)

    @property
    def has_cabin(self) -> bool:
        return self.cabin_zone.is_known

    @property
    def economic_tier(self) -> str:
        if self.pclass.value == PClassType.FIRST:   return "premium"
        if self.pclass.value == PClassType.SECOND:  return "middle"
        return "economy"

    def __str__(self) -> str:
        return f"{self.pclass}등석 / {self.cabin_zone}구역 / {self.fare}"
