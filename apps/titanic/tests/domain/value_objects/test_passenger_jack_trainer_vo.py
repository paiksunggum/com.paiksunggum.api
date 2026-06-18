import pytest

from apps.titanic.domain.value_objects.social_profile_vo import (
    Gender, GenderType, Title, TitleType, SocialProfile,
)
from apps.titanic.domain.value_objects.travel_class_vo import (
    PClass, PClassType, CabinZone, CabinZoneType, Fare, TravelClass,
)
from apps.titanic.domain.value_objects.boarding_info_vo import (
    EmbarkedPort, EmbarkedPortType, Ticket, BoardingInfo,
)
from apps.titanic.domain.value_objects.survived_vo import SurvivedStatus, SurvivedType
from apps.titanic.domain.entities.passenger_jack_trainer_entity import PassengerId


class TestPassengerId:
    def test_valid_id_creates_successfully(self):
        assert PassengerId("P001").value == "P001"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            PassengerId("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError):
            PassengerId("   ")

    def test_strips_surrounding_whitespace(self):
        assert PassengerId("  P001  ").value == "P001"

    def test_str_returns_value(self):
        assert str(PassengerId("42")) == "42"


class TestGender:
    def test_from_raw_male(self):
        assert Gender.from_raw("male") == Gender(value=GenderType.MALE)

    def test_from_raw_female(self):
        assert Gender.from_raw("female") == Gender(value=GenderType.FEMALE)

    def test_from_raw_none_is_unknown(self):
        assert Gender.from_raw(None) == Gender(value=GenderType.UNKNOWN)

    def test_from_raw_uppercase_normalized(self):
        assert Gender.from_raw("MALE") == Gender(value=GenderType.MALE)

    def test_from_raw_unrecognized_is_unknown(self):
        assert Gender.from_raw("other") == Gender(value=GenderType.UNKNOWN)


class TestTitle:
    def test_mr_from_name(self):
        assert Title.from_name("Braund, Mr. Owen Harris").value == TitleType.MR

    def test_mrs_from_name(self):
        assert Title.from_name("Cumings, Mrs. John Bradley").value == TitleType.MRS

    def test_miss_from_name(self):
        assert Title.from_name("Heikkinen, Miss. Laina").value == TitleType.MISS

    def test_master_from_name(self):
        assert Title.from_name("Palsson, Master. Gosta").value == TitleType.MASTER

    def test_rare_title(self):
        assert Title.from_name("Capt. Smith").value == TitleType.RARE

    def test_none_name_is_unknown(self):
        assert Title.from_name(None).value == TitleType.UNKNOWN

    def test_is_minor_true_for_master(self):
        assert Title.from_name("Palsson, Master. Gosta").is_minor is True

    def test_is_female_true_for_mrs(self):
        assert Title.from_name("Cumings, Mrs. John").is_female is True


class TestSocialProfile:
    def test_from_raw_male_mr(self):
        p = SocialProfile.from_raw("Braund, Mr. Owen", "male")
        assert p.gender.value == GenderType.MALE
        assert p.title.value == TitleType.MR
        assert p.survival_priority == 0

    def test_from_raw_female_mrs(self):
        p = SocialProfile.from_raw("Cumings, Mrs. John", "female")
        assert p.is_female is True
        assert p.survival_priority == 2

    def test_master_has_highest_priority(self):
        p = SocialProfile.from_raw("Palsson, Master. Gosta", "male")
        assert p.survival_priority == 3


class TestTravelClass:
    def test_from_raw_first_class(self):
        t = TravelClass.from_raw("1", "C85", "71.28")
        assert t.pclass.value == PClassType.FIRST
        assert t.cabin_zone.value == CabinZoneType.C
        assert t.fare.value == 71.28
        assert t.economic_tier == "premium"
        assert t.is_upper_deck is True

    def test_from_raw_third_class_no_cabin(self):
        t = TravelClass.from_raw("3", "", "7.25")
        assert t.has_cabin is False
        assert t.economic_tier == "economy"

    def test_fare_negative_raises(self):
        with pytest.raises(ValueError):
            Fare(value=-1.0)


class TestBoardingInfo:
    def test_from_raw_southampton(self):
        b = BoardingInfo.from_raw("S", "A/5 21171")
        assert b.embarked.value == EmbarkedPortType.SOUTHAMPTON
        assert b.is_southampton is True

    def test_from_raw_cherbourg(self):
        b = BoardingInfo.from_raw("C", "PC 17599")
        assert b.embarked.value == EmbarkedPortType.CHERBOURG

    def test_unknown_port(self):
        b = BoardingInfo.from_raw(None, "12345")
        assert b.embarked.value == EmbarkedPortType.UNKNOWN


class TestSurvivedStatus:
    def test_from_raw_1_means_survived(self):
        assert SurvivedStatus.from_raw("1") == SurvivedStatus(value=SurvivedType.SURVIVED)

    def test_from_raw_0_means_perished(self):
        assert SurvivedStatus.from_raw("0") == SurvivedStatus(value=SurvivedType.PERISHED)

    def test_from_raw_none_is_unknown(self):
        assert SurvivedStatus.from_raw(None) == SurvivedStatus(value=SurvivedType.UNKNOWN)

    def test_is_survived_true(self):
        assert SurvivedStatus(value=SurvivedType.SURVIVED).is_survived is True

    def test_is_survived_false_for_perished(self):
        assert SurvivedStatus(value=SurvivedType.PERISHED).is_survived is False
