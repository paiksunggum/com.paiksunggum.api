from __future__ import annotations

from apps.titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerORM
from apps.titanic.domain.entities.passenger_jack_trainer_entity import JackTrainerEntity, PassengerId
from apps.titanic.domain.value_objects.social_profile_vo import SocialProfile
from apps.titanic.domain.value_objects.travel_class_vo import TravelClass
from apps.titanic.domain.value_objects.boarding_info_vo import BoardingInfo
from apps.titanic.domain.value_objects.survived_vo import SurvivedStatus


class JackTrainerMapper:
    """JackTrainerORM ↔ JackTrainerEntity 변환."""

    @staticmethod
    def to_entity(orm: JackTrainerORM) -> JackTrainerEntity:
        return JackTrainerEntity(
            passenger_id=PassengerId(orm.passenger_id or ""),
            name=orm.name,
            social_profile=SocialProfile.from_raw(
                name_raw=orm.name,
                gender_raw=orm.gender,
            ),
            travel_class=TravelClass.from_raw(
                pclass_raw=orm.pclass,
                cabin_raw=orm.cabin,
                fare_raw=orm.fare,
            ),
            boarding_info=BoardingInfo.from_raw(
                embarked_raw=orm.embarked,
                ticket_raw=orm.ticket,
            ),
            survived=SurvivedStatus.from_raw(orm.survived),
        )

    @staticmethod
    def to_orm(entity: JackTrainerEntity) -> JackTrainerORM:
        return JackTrainerORM(
            passenger_id=str(entity.passenger_id),
            name=entity.name,
            gender=str(entity.social_profile.gender),
            pclass=str(entity.travel_class.pclass),
            cabin=str(entity.travel_class.cabin_zone),
            fare=str(entity.travel_class.fare.value),
            embarked=str(entity.boarding_info.embarked),
            ticket=str(entity.boarding_info.ticket),
            survived=entity.survived.value,
        )
