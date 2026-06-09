from __future__ import annotations

from apps.titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelORM


class RoseModelMapper:
    """RoseModelORM ↔ dict 변환. (엔티티 미정의 — 추후 BookingEntity 작성 후 교체)"""

    @staticmethod
    def to_dict(orm: RoseModelORM) -> dict:
        return {
            "id": orm.id,
            "person_id": orm.person_id,
            "pclass": orm.pclass,
            "ticket": orm.ticket,
            "fare": orm.fare,
            "cabin": orm.cabin,
            "embarked": orm.embarked,
        }

    @staticmethod
    def to_orm(data: dict) -> RoseModelORM:
        return RoseModelORM(
            person_id=data.get("person_id"),
            pclass=data.get("pclass"),
            ticket=data.get("ticket"),
            fare=data.get("fare"),
            cabin=data.get("cabin"),
            embarked=data.get("embarked"),
        )
