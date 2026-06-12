import pytest
from types import SimpleNamespace

from apps.titanic.adapter.outbound.mappers.passenger_jack_trainer_mapper import JackTrainerMapper
from apps.titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    SurvivedStatus,
)
from apps.titanic.domain.entities.passenger_jack_trainer_entity import JackTrainerEntity


def _make_orm(**overrides):
    defaults = dict(
        passenger_id="P001",
        name="Dawson, Mr. Jack",
        gender="male",
        age="30.0",
        sib_sp="0",
        parch="0",
        survived="0",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def _make_entity(
    passenger_id: str = "P001",
    name: str | None = "Dawson, Mr. Jack",
    gender_raw: str = "male",
    age_value: float | None = 30.0,
    sib_sp: int = 0,
    parch: int = 0,
    survived_raw: str = "0",
) -> JackTrainerEntity:
    return JackTrainerEntity(
        passenger_id=PassengerId(passenger_id),
        name=name,
        gender=Gender.from_raw(gender_raw),
        age=Age(age_value),
        family_relation=FamilyRelation(sib_sp=sib_sp, parch=parch),
        survived=SurvivedStatus.from_raw(survived_raw),
    )


class TestToEntity:
    def test_maps_passenger_id(self):
        entity = JackTrainerMapper.to_entity(_make_orm(passenger_id="P099"))
        assert str(entity.passenger_id) == "P099"

    def test_maps_name(self):
        entity = JackTrainerMapper.to_entity(_make_orm(name="Smith, Mr. John"))
        assert entity.name == "Smith, Mr. John"

    def test_none_name_maps_to_none(self):
        entity = JackTrainerMapper.to_entity(_make_orm(name=None))
        assert entity.name is None

    def test_maps_gender_male(self):
        entity = JackTrainerMapper.to_entity(_make_orm(gender="male"))
        assert entity.gender == Gender.MALE

    def test_maps_gender_female(self):
        entity = JackTrainerMapper.to_entity(_make_orm(gender="female"))
        assert entity.gender == Gender.FEMALE

    def test_invalid_gender_maps_to_unknown(self):
        entity = JackTrainerMapper.to_entity(_make_orm(gender=None))
        assert entity.gender == Gender.UNKNOWN

    def test_maps_age(self):
        entity = JackTrainerMapper.to_entity(_make_orm(age="25.0"))
        assert entity.age.value == 25.0

    def test_none_age_maps_to_none(self):
        entity = JackTrainerMapper.to_entity(_make_orm(age=None))
        assert entity.age.value is None

    def test_maps_family_relation(self):
        entity = JackTrainerMapper.to_entity(_make_orm(sib_sp="2", parch="3"))
        assert entity.family_relation.sib_sp == 2
        assert entity.family_relation.parch == 3

    def test_none_sib_sp_parch_defaults_to_zero(self):
        entity = JackTrainerMapper.to_entity(_make_orm(sib_sp=None, parch=None))
        assert entity.family_relation.sib_sp == 0
        assert entity.family_relation.parch == 0

    def test_survived_1_maps_to_survived(self):
        entity = JackTrainerMapper.to_entity(_make_orm(survived="1"))
        assert entity.survived == SurvivedStatus.SURVIVED

    def test_survived_0_maps_to_perished(self):
        entity = JackTrainerMapper.to_entity(_make_orm(survived="0"))
        assert entity.survived == SurvivedStatus.PERISHED

    def test_survived_none_maps_to_unknown(self):
        entity = JackTrainerMapper.to_entity(_make_orm(survived=None))
        assert entity.survived == SurvivedStatus.UNKNOWN

    def test_none_passenger_id_raises(self):
        # passenger_id=None → PassengerId("") → ValueError (빈 ID 불허)
        with pytest.raises(ValueError):
            JackTrainerMapper.to_entity(_make_orm(passenger_id=None))


class TestToOrm:
    def test_maps_passenger_id_to_string(self):
        orm = JackTrainerMapper.to_orm(_make_entity(passenger_id="P001"))
        assert orm.passenger_id == "P001"

    def test_maps_name(self):
        orm = JackTrainerMapper.to_orm(_make_entity(name="Brown, Mrs. Anne"))
        assert orm.name == "Brown, Mrs. Anne"

    def test_maps_gender_male_to_string(self):
        orm = JackTrainerMapper.to_orm(_make_entity(gender_raw="male"))
        assert orm.gender == "male"

    def test_maps_gender_female_to_string(self):
        orm = JackTrainerMapper.to_orm(_make_entity(gender_raw="female"))
        assert orm.gender == "female"

    def test_maps_age_to_string(self):
        orm = JackTrainerMapper.to_orm(_make_entity(age_value=25.0))
        assert orm.age == "25.0"

    def test_none_age_maps_to_empty_string(self):
        orm = JackTrainerMapper.to_orm(_make_entity(age_value=None))
        assert orm.age == ""

    def test_maps_family_relation_to_strings(self):
        orm = JackTrainerMapper.to_orm(_make_entity(sib_sp=2, parch=3))
        assert orm.sib_sp == "2"
        assert orm.parch == "3"

    def test_survived_maps_to_string_1(self):
        orm = JackTrainerMapper.to_orm(_make_entity(survived_raw="1"))
        assert orm.survived == "1"

    def test_perished_maps_to_string_0(self):
        orm = JackTrainerMapper.to_orm(_make_entity(survived_raw="0"))
        assert orm.survived == "0"

    def test_unknown_survived_maps_to_unknown_string(self):
        orm = JackTrainerMapper.to_orm(_make_entity(survived_raw=""))
        assert orm.survived == "unknown"
