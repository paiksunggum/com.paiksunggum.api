from __future__ import annotations

from apps.titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerORM
from apps.titanic.domain.entities.passenger_jack_trainer_entity import JackTrainerEntity
from apps.titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    SurvivedStatus,
)


class JackTrainerMapper:
    """JackTrainerORM ↔ JackTrainerEntity 변환."""

    @staticmethod
    def to_entity(orm: JackTrainerORM) -> JackTrainerEntity:
        return JackTrainerEntity(
            passenger_id=PassengerId(orm.passenger_id or ""),
            name=orm.name,
            gender=Gender.from_raw(orm.gender),
            age=Age(float(orm.age) if orm.age else None),
            family_relation=FamilyRelation(
                sib_sp=int(orm.sib_sp or 0),
                parch=int(orm.parch or 0),
            ),
            survived=SurvivedStatus.from_raw(orm.survived),
        )

    @staticmethod
    def to_orm(entity: JackTrainerEntity) -> JackTrainerORM:
        return JackTrainerORM(
            passenger_id=str(entity.passenger_id),
            name=entity.name,
            gender=entity.gender.value,
            age=str(entity.age.value) if entity.age.value is not None else "",
            sib_sp=str(entity.family_relation.sib_sp),
            parch=str(entity.family_relation.parch),
            survived=entity.survived.value,
        )
