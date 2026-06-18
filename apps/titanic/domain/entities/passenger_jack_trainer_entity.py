from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from ..value_objects.social_profile_vo import SocialProfile
from ..value_objects.travel_class_vo import TravelClass
from ..value_objects.boarding_info_vo import BoardingInfo
from ..value_objects.survived_vo import SurvivedStatus, SurvivedType


@dataclass(frozen=True)
class PassengerId:
    """승객 도메인 식별자"""
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("PassengerId는 비어 있을 수 없습니다.")
        object.__setattr__(self, "value", self.value.strip())

    def __str__(self) -> str:
        return self.value


@dataclass
class JackTrainerEntity:
    """
    JackTrainer Entity.
    - 동일성: PassengerId로만 판단
    - 상태 변경: 명시적 메서드로만 허용
    - ORM 의존 없음
    """

    def __init__(
        self,
        passenger_id:   PassengerId,
        name:           Optional[str],
        social_profile: SocialProfile,
        travel_class:   TravelClass,
        boarding_info:  BoardingInfo,
        survived:       SurvivedStatus,
    ) -> None:
        self._passenger_id   = passenger_id
        self._name           = name
        self._social_profile = social_profile
        self._travel_class   = travel_class
        self._boarding_info  = boarding_info
        self._survived       = survived

    # ── 식별자 ──────────────────────────────────────────
    @property
    def passenger_id(self) -> PassengerId:
        return self._passenger_id

    # ── 조회 ────────────────────────────────────────────
    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def social_profile(self) -> SocialProfile:
        return self._social_profile

    @property
    def travel_class(self) -> TravelClass:
        return self._travel_class

    @property
    def boarding_info(self) -> BoardingInfo:
        return self._boarding_info

    @property
    def survived(self) -> SurvivedStatus:
        return self._survived

    # ── 도메인 행위 ──────────────────────────────────────
    def record_survival(self, survived: bool) -> None:
        """생존 결과 기록 — UNKNOWN 상태일 때만 허용"""
        if self._survived != SurvivedStatus(value=SurvivedType.UNKNOWN):
            raise ValueError("이미 생존 결과가 기록된 승객입니다.")
        self._survived = (
            SurvivedStatus(value=SurvivedType.SURVIVED)
            if survived
            else SurvivedStatus(value=SurvivedType.PERISHED)
        )

    def correct_name(self, new_name: str) -> None:
        if not new_name.strip():
            raise ValueError("이름은 비어 있을 수 없습니다.")
        self._name = new_name.strip()

    # ── 동일성 ───────────────────────────────────────────
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JackTrainerEntity):
            return NotImplemented
        return self._passenger_id == other._passenger_id

    def __hash__(self) -> int:
        return hash(self._passenger_id)

    def __repr__(self) -> str:
        return (
            f"JackTrainerEntity(id={self._passenger_id}, name={self._name!r}, "
            f"survived={self._survived.value.name})"
        )
