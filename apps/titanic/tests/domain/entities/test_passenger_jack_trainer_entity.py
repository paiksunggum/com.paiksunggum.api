import pytest

from apps.titanic.domain.entities.passenger_jack_trainer_entity import JackTrainerEntity
from apps.titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    SurvivedStatus,
)


def _make_entity(
    passenger_id: str = "P001",
    name: str | None = "Dawson, Mr. Jack",
    gender_raw: str | None = "male",
    age_value: float | None = 30.0,
    sib_sp: int = 0,
    parch: int = 0,
    survived: SurvivedStatus = SurvivedStatus.PERISHED,
) -> JackTrainerEntity:
    return JackTrainerEntity(
        passenger_id=PassengerId(passenger_id),
        name=name,
        gender=Gender.from_raw(gender_raw),
        age=Age(age_value),
        family_relation=FamilyRelation(sib_sp=sib_sp, parch=parch),
        survived=survived,
    )


class TestFamilyRelation:
    def test_traveled_alone_when_no_family(self):
        assert _make_entity(sib_sp=0, parch=0).family_relation.traveled_alone is True

    def test_not_alone_when_has_siblings(self):
        assert _make_entity(sib_sp=1, parch=0).family_relation.traveled_alone is False

    def test_not_alone_when_has_children(self):
        assert _make_entity(sib_sp=0, parch=1).family_relation.traveled_alone is False

    def test_total_is_sum_of_sib_sp_and_parch(self):
        assert _make_entity(sib_sp=2, parch=3).family_relation.total == 5


class TestAge:
    def test_is_minor_under_18(self):
        assert _make_entity(age_value=15.0).age.is_minor is True

    def test_is_not_minor_at_18(self):
        assert _make_entity(age_value=18.0).age.is_minor is False

    def test_is_not_minor_above_18(self):
        assert _make_entity(age_value=30.0).age.is_minor is False

    def test_none_age_is_not_minor(self):
        assert _make_entity(age_value=None).age.is_minor is False

    def test_negative_age_raises(self):
        with pytest.raises(ValueError):
            _make_entity(age_value=-1.0)


class TestRecordSurvival:
    def test_record_true_sets_survived(self):
        entity = _make_entity(survived=SurvivedStatus.UNKNOWN)
        entity.record_survival(True)
        assert entity.survived == SurvivedStatus.SURVIVED

    def test_record_false_sets_perished(self):
        entity = _make_entity(survived=SurvivedStatus.UNKNOWN)
        entity.record_survival(False)
        assert entity.survived == SurvivedStatus.PERISHED

    def test_record_raises_when_already_set(self):
        # UNKNOWN 상태가 아닐 때 중복 기록 불가
        entity = _make_entity(survived=SurvivedStatus.SURVIVED)
        with pytest.raises(ValueError):
            entity.record_survival(False)


class TestCorrectName:
    def test_updates_name(self):
        entity = _make_entity(name="Old Name")
        entity.correct_name("New Name")
        assert entity.name == "New Name"

    def test_strips_whitespace(self):
        entity = _make_entity()
        entity.correct_name("  Jack Dawson  ")
        assert entity.name == "Jack Dawson"

    def test_blank_name_raises(self):
        entity = _make_entity()
        with pytest.raises(ValueError):
            entity.correct_name("   ")


class TestEquality:
    # __eq__ 버그: isinstance(other, Passenger) → Passenger 미정의 → NameError 발생
    # 아래 테스트는 이 버그를 문서화한다 (Red → 수정 대상: JackTrainerEntity로 교체)
    def test_eq_raises_due_to_undefined_passenger(self):
        with pytest.raises(NameError):
            _make_entity(passenger_id="P001") == _make_entity(passenger_id="P001")

    def test_hash_is_based_on_passenger_id(self):
        # __hash__는 PassengerId 기반 — __eq__ 버그와 무관하게 동작
        assert hash(_make_entity(passenger_id="P001")) == hash(_make_entity(passenger_id="P001"))

    def test_different_passenger_id_has_different_hash(self):
        assert hash(_make_entity(passenger_id="P001")) != hash(_make_entity(passenger_id="P002"))
