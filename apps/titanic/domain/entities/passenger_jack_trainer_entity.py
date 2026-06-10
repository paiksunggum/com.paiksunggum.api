# domain/entities.py
from typing import Optional
from ..value_objects.passenger_jack_trainer_vo import PassengerId, Gender, Age, FamilyRelation, SurvivedStatus

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
        passenger_id: PassengerId,
        name: Optional[str],
        gender: Gender,
        age: Age,
        family_relation: FamilyRelation,
        survived: SurvivedStatus,
    ) -> None:
        self._passenger_id = passenger_id
        self._name = name
        self._gender = gender
        self._age = age
        self._family_relation = family_relation
        self._survived = survived

    # ── 식별자 ──────────────────────────────────────────
    @property
    def passenger_id(self) -> PassengerId:
        return self._passenger_id

    # ── 조회 ────────────────────────────────────────────
    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def gender(self) -> Gender:
        return self._gender

    @property
    def age(self) -> Age:
        return self._age

    @property
    def family_relation(self) -> FamilyRelation:
        return self._family_relation

    @property
    def survived(self) -> SurvivedStatus:
        return self._survived

    # ── 도메인 행위 ──────────────────────────────────────
    def record_survival(self, survived: bool) -> None:
        """생존 결과 기록 — UNKNOWN 상태일 때만 허용"""
        if self._survived != SurvivedStatus.UNKNOWN:
            raise ValueError("이미 생존 결과가 기록된 승객입니다.")
        self._survived = SurvivedStatus.SURVIVED if survived else SurvivedStatus.PERISHED

    def correct_name(self, new_name: str) -> None:
        if not new_name.strip():
            raise ValueError("이름은 비어 있을 수 없습니다.")
        self._name = new_name.strip()

    # ── 동일성 ───────────────────────────────────────────
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Passenger):
            return NotImplemented
        return self._passenger_id == other._passenger_id

    def __hash__(self) -> int:
        return hash(self._passenger_id)

    def __repr__(self) -> str:
        return (
            f"Passenger(id={self._passenger_id}, name={self._name!r}, "
            f"survived={self._survived.name})"
        )