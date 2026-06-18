import pytest

from apps.titanic.domain.entities.passenger_jack_trainer_entity import JackTrainerEntity, PassengerId
from apps.titanic.domain.value_objects.social_profile_vo import SocialProfile
from apps.titanic.domain.value_objects.travel_class_vo import TravelClass
from apps.titanic.domain.value_objects.boarding_info_vo import BoardingInfo
from apps.titanic.domain.value_objects.survived_vo import SurvivedStatus, SurvivedType


def _make_entity(
    passenger_id: str = "P001",
    name: str | None = "Dawson, Mr. Jack",
    gender_raw: str | None = "male",
    pclass_raw: str = "3",
    survived: SurvivedStatus = SurvivedStatus(value=SurvivedType.PERISHED),
) -> JackTrainerEntity:
    return JackTrainerEntity(
        passenger_id=PassengerId(passenger_id),
        name=name,
        social_profile=SocialProfile.from_raw(name, gender_raw),
        travel_class=TravelClass.from_raw(pclass_raw, "", "7.25"),
        boarding_info=BoardingInfo.from_raw("S", "A/5 21171"),
        survived=survived,
    )


class TestSocialProfile:
    def test_male_mr_entity(self):
        e = _make_entity(name="Dawson, Mr. Jack", gender_raw="male")
        assert e.social_profile.is_female is False
        assert e.social_profile.survival_priority == 0

    def test_female_mrs_entity(self):
        e = _make_entity(name="Dewitt Bukater, Mrs. John", gender_raw="female")
        assert e.social_profile.is_female is True
        assert e.social_profile.survival_priority == 2


class TestTravelClass:
    def test_third_class_economy(self):
        e = _make_entity(pclass_raw="3")
        assert e.travel_class.economic_tier == "economy"

    def test_first_class_premium(self):
        e = _make_entity(pclass_raw="1")
        assert e.travel_class.economic_tier == "premium"


class TestRecordSurvival:
    def test_record_true_sets_survived(self):
        e = _make_entity(survived=SurvivedStatus(value=SurvivedType.UNKNOWN))
        e.record_survival(True)
        assert e.survived == SurvivedStatus(value=SurvivedType.SURVIVED)

    def test_record_false_sets_perished(self):
        e = _make_entity(survived=SurvivedStatus(value=SurvivedType.UNKNOWN))
        e.record_survival(False)
        assert e.survived == SurvivedStatus(value=SurvivedType.PERISHED)

    def test_record_raises_when_already_set(self):
        e = _make_entity(survived=SurvivedStatus(value=SurvivedType.SURVIVED))
        with pytest.raises(ValueError):
            e.record_survival(False)


class TestCorrectName:
    def test_updates_name(self):
        e = _make_entity(name="Old Name")
        e.correct_name("New Name")
        assert e.name == "New Name"

    def test_strips_whitespace(self):
        e = _make_entity()
        e.correct_name("  Jack Dawson  ")
        assert e.name == "Jack Dawson"

    def test_blank_name_raises(self):
        e = _make_entity()
        with pytest.raises(ValueError):
            e.correct_name("   ")


class TestEquality:
    def test_same_passenger_id_is_equal(self):
        assert _make_entity("P001") == _make_entity("P001")

    def test_different_passenger_id_not_equal(self):
        assert _make_entity("P001") != _make_entity("P002")

    def test_hash_same_for_same_id(self):
        assert hash(_make_entity("P001")) == hash(_make_entity("P001"))

    def test_hash_different_for_different_id(self):
        assert hash(_make_entity("P001")) != hash(_make_entity("P002"))
