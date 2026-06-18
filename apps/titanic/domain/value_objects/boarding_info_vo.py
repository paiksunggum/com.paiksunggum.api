from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ── EmbarkedPort ──────────────────────────────────────────────────────────────

class EmbarkedPortType(str, Enum):
    CHERBOURG   = "C"
    QUEENSTOWN  = "Q"
    SOUTHAMPTON = "S"
    UNKNOWN     = "U"


@dataclass(frozen=True)
class EmbarkedPort:
    """탑승 항구 VO (embarked 컬럼 — C/Q/S)"""
    value: EmbarkedPortType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "EmbarkedPort":
        mapping = {
            "C": EmbarkedPortType.CHERBOURG,
            "Q": EmbarkedPortType.QUEENSTOWN,
            "S": EmbarkedPortType.SOUTHAMPTON,
        }
        return cls(value=mapping.get((raw or "").strip().upper(), EmbarkedPortType.UNKNOWN))

    @property
    def city(self) -> str:
        return {
            EmbarkedPortType.CHERBOURG:   "쉐르부르 (프랑스)",
            EmbarkedPortType.QUEENSTOWN:  "퀸스타운 (아일랜드)",
            EmbarkedPortType.SOUTHAMPTON: "사우샘프턴 (영국)",
            EmbarkedPortType.UNKNOWN:     "미기재",
        }[self.value]

    def __str__(self) -> str:
        return self.value.value


# ── Ticket ────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Ticket:
    """티켓 번호 VO (ticket 컬럼)"""
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("티켓 번호는 비어 있을 수 없습니다.")
        object.__setattr__(self, "value", self.value.strip().upper())

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Ticket":
        if not raw or not raw.strip():
            raise ValueError("티켓 번호는 비어 있을 수 없습니다.")
        return cls(value=raw)

    def __str__(self) -> str:
        return self.value


# ── BoardingInfo (임베디드 값 타입) ───────────────────────────────────────────

@dataclass(frozen=True)
class BoardingInfo:
    """탑승 정보 임베디드 값 타입 (EmbarkedPort + Ticket).

    둘 다 "어디서, 어떤 티켓으로 탑승했는가"를 표현한다.
    생존 예측 6~7위 피처(Ticket +0.18, Embarked −0.18)를 하나의 단위로 묶는다.
    """
    embarked: EmbarkedPort
    ticket:   Ticket

    @classmethod
    def from_raw(cls, embarked_raw: Optional[str], ticket_raw: Optional[str]) -> "BoardingInfo":
        return cls(
            embarked=EmbarkedPort.from_raw(embarked_raw),
            ticket=Ticket.from_raw(ticket_raw or "UNKNOWN"),
        )

    @property
    def is_southampton(self) -> bool:
        return self.embarked.value == EmbarkedPortType.SOUTHAMPTON

    def __str__(self) -> str:
        return f"{self.embarked.city} / {self.ticket}"
