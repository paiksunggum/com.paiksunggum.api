import pytest

from apps.titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    SurvivedStatus,
)


class TestPassengerId:
    def test_valid_id_creates_successfully(self):
        pid = PassengerId("P001")
        assert pid.value == "P001"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            PassengerId("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError):
            PassengerId("   ")

    def test_str_returns_value(self):
        assert str(PassengerId("42")) == "42"

    def test_strips_surrounding_whitespace(self):
        assert PassengerId("  P001  ").value == "P001"


class TestGender:
    def test_from_raw_male(self):
        assert Gender.from_raw("male") == Gender.MALE

    def test_from_raw_female(self):
        assert Gender.from_raw("female") == Gender.FEMALE

    def test_from_raw_none_is_unknown(self):
        assert Gender.from_raw(None) == Gender.UNKNOWN

    def test_from_raw_uppercase_is_normalized(self):
        assert Gender.from_raw("MALE") == Gender.MALE

    def test_from_raw_unrecognized_string_is_unknown(self):
        assert Gender.from_raw("other") == Gender.UNKNOWN


class TestAge:
    def test_valid_age_creates_successfully(self):
        assert Age(value=22.5).value == 22.5

    def test_none_age_is_allowed(self):
        assert Age(value=None).value is None

    def test_negative_age_raises(self):
        with pytest.raises(ValueError):
            Age(value=-1.0)

    def test_boundary_0_is_valid(self):
        Age(value=0.0)

    def test_is_minor_true_under_18(self):
        assert Age(value=17.9).is_minor is True

    def test_is_minor_false_at_18(self):
        assert Age(value=18.0).is_minor is False

    def test_is_minor_false_for_none_age(self):
        assert Age(value=None).is_minor is False


class TestFamilyRelation:
    def test_total_sums_sib_sp_and_parch(self):
        assert FamilyRelation(sib_sp=2, parch=3).total == 5

    def test_traveled_alone_when_both_zero(self):
        assert FamilyRelation(sib_sp=0, parch=0).traveled_alone is True

    def test_not_alone_with_siblings(self):
        assert FamilyRelation(sib_sp=1, parch=0).traveled_alone is False

    def test_not_alone_with_children(self):
        assert FamilyRelation(sib_sp=0, parch=1).traveled_alone is False

    def test_negative_sib_sp_raises(self):
        with pytest.raises(ValueError):
            FamilyRelation(sib_sp=-1, parch=0)

    def test_negative_parch_raises(self):
        with pytest.raises(ValueError):
            FamilyRelation(sib_sp=0, parch=-1)


class TestSurvivedStatus:
    def test_from_raw_1_means_survived(self):
        assert SurvivedStatus.from_raw("1") == SurvivedStatus.SURVIVED

    def test_from_raw_0_means_perished(self):
        assert SurvivedStatus.from_raw("0") == SurvivedStatus.PERISHED

    def test_from_raw_none_is_unknown(self):
        assert SurvivedStatus.from_raw(None) == SurvivedStatus.UNKNOWN

    def test_from_raw_empty_string_is_unknown(self):
        assert SurvivedStatus.from_raw("") == SurvivedStatus.UNKNOWN

    def test_from_raw_unrecognized_value_is_unknown(self):
        # 인식할 수 없는 값은 예외 없이 UNKNOWN으로 처리
        assert SurvivedStatus.from_raw("2") == SurvivedStatus.UNKNOWN

    def test_is_survived_true_for_survived(self):
        assert SurvivedStatus.SURVIVED.is_survived is True

    def test_is_survived_false_for_perished(self):
        assert SurvivedStatus.PERISHED.is_survived is False

    def test_is_survived_false_for_unknown(self):
        assert SurvivedStatus.UNKNOWN.is_survived is False
