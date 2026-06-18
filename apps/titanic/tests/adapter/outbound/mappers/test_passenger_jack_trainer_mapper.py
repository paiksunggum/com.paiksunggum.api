import pytest
from types import SimpleNamespace

from apps.titanic.adapter.outbound.mappers.passenger_jack_trainer_mapper import JackTrainerMapper
from apps.titanic.domain.value_objects.social_profile_vo import GenderType
from apps.titanic.domain.value_objects.travel_class_vo import PClassType
from apps.titanic.domain.value_objects.boarding_info_vo import EmbarkedPortType
from apps.titanic.domain.value_objects.survived_vo import SurvivedStatus, SurvivedType
from apps.titanic.domain.entities.passenger_jack_trainer_entity import PassengerId


def _make_orm(**overrides):
    defaults = dict(
        passenger_id="P001",
        name="Braund, Mr. Owen Harris",
        gender="male",
        pclass="3",
        cabin="",
        fare="7.25",
        embarked="S",
        ticket="A/5 21171",
        survived="0",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


class TestToEntity:
    def test_maps_passenger_id(self):
        e = JackTrainerMapper.to_entity(_make_orm(passenger_id="P099"))
        assert str(e.passenger_id) == "P099"

    def test_maps_name(self):
        e = JackTrainerMapper.to_entity(_make_orm(name="Smith, Mr. John"))
        assert e.name == "Smith, Mr. John"

    def test_none_name_maps_to_none(self):
        e = JackTrainerMapper.to_entity(_make_orm(name=None))
        assert e.name is None

    def test_maps_gender_male(self):
        e = JackTrainerMapper.to_entity(_make_orm(gender="male"))
        assert e.social_profile.gender.value == GenderType.MALE

    def test_maps_gender_female(self):
        e = JackTrainerMapper.to_entity(_make_orm(gender="female"))
        assert e.social_profile.gender.value == GenderType.FEMALE

    def test_maps_pclass_first(self):
        e = JackTrainerMapper.to_entity(_make_orm(pclass="1"))
        assert e.travel_class.pclass.value == PClassType.FIRST

    def test_maps_embarked_southampton(self):
        e = JackTrainerMapper.to_entity(_make_orm(embarked="S"))
        assert e.boarding_info.embarked.value == EmbarkedPortType.SOUTHAMPTON

    def test_maps_embarked_cherbourg(self):
        e = JackTrainerMapper.to_entity(_make_orm(embarked="C"))
        assert e.boarding_info.embarked.value == EmbarkedPortType.CHERBOURG

    def test_survived_1_maps_to_survived(self):
        e = JackTrainerMapper.to_entity(_make_orm(survived="1"))
        assert e.survived == SurvivedStatus(value=SurvivedType.SURVIVED)

    def test_survived_0_maps_to_perished(self):
        e = JackTrainerMapper.to_entity(_make_orm(survived="0"))
        assert e.survived == SurvivedStatus(value=SurvivedType.PERISHED)

    def test_none_passenger_id_raises(self):
        with pytest.raises(ValueError):
            JackTrainerMapper.to_entity(_make_orm(passenger_id=None))
