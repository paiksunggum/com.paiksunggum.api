from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Any

from apps.titanic.adapter.outbound.orm.booking_orm import BookingORM
from apps.titanic.adapter.outbound.orm.person_orm import PersonORM
from apps.titanic.app.dtos.crew_andrew_blueprint_dto import AndrewBlueprintQuery, AndrewBlueprintResponse
from apps.titanic.app.ports.output.crew_andrew_blueprint_repository import AndrewBlueprintRepository
import logging
logger = logging.getLogger("apps")

def _row_to_dict(person: PersonORM, booking: BookingORM | None) -> dict[str, Any]:
    return {
        "id": person.id,
        "passenger_id": person.passenger_id,
        "survived": person.survived,
        "pclass": booking.pclass if booking else None,
        "name": person.name,
        "gender": person.gender,
        "age": person.age,
        "sibsp": person.sib_sp,
        "parch": person.parch,
        "ticket": booking.ticket if booking else None,
        "fare": booking.fare if booking else None,
        "cabin": booking.cabin if booking else None,
        "embarked": booking.embarked if booking else None,
    }


class AndrewBlueprintPgRepository(AndrewBlueprintRepository):
    '''PostgreSQL을 이용한 앤드류의 승객 명단 관리 저장소'''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: AndrewBlueprintQuery) -> AndrewBlueprintResponse:
        '''승객 명단을 가져오는 메소드'''


        logger.info("###############################################")
        logger.info("💊[앤드류 레포지토리] DB 에서 반환하는 승객 명단")
        logger.info(f"👍🏻ID: {query.id}")
        logger.info(f"🐥이름: {query.name}")
        logger.info(f"🦜메모: {query.memo}")
        logger.info("###############################################")


        return AndrewBlueprintResponse(
            id=query.id * 10000,
            name=query.name,
            memo=query.memo,
        )