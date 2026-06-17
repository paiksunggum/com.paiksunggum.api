from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Any

from apps.titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelORM
from apps.titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerORM
from apps.titanic.app.dtos.crew_andrew_blueprint_dto import AndrewBlueprintQuery, AndrewBlueprintResponse
from apps.titanic.app.ports.output.crew_andrew_blueprint_port import AndrewBlueprintPort
import logging
logger = logging.getLogger("apps")

def _row_to_dict(person: JackTrainerORM, booking: RoseModelORM | None) -> dict[str, Any]:
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


class AndrewBlueprintRepository(AndrewBlueprintPort):
    '''PostgreSQL을 이용한 앤드류의 승객 명단 관리 저장소'''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_train_set(self) -> list[dict[str, Any]]:
        '''Survived 컬럼이 있는 데이터 전체를 데이터 프레임으로 반환하는 메소드'''
        stmt = (
            select(JackTrainerORM, RoseModelORM)
            .outerjoin(RoseModelORM, JackTrainerORM.passenger_id == RoseModelORM.passenger_id)
            .where(JackTrainerORM.survived.isnot(None))
            .where(JackTrainerORM.survived != "")
        )
        result = await self.session.execute(stmt)
        rows = result.all()
        logger.info("[AndrewBlueprintRepository] get_train_set | 행 수=%d", len(rows))
        return [_row_to_dict(person, booking) for person, booking in rows]

    async def get_test_set(self) -> list[dict[str, Any]]:
        '''Survived 컬럼이 없는 데이터 전체를 데이터 프레임으로 반환하는 메소드'''
        stmt = (
            select(JackTrainerORM, RoseModelORM)
            .outerjoin(RoseModelORM, JackTrainerORM.passenger_id == RoseModelORM.passenger_id)
            .where(
                (JackTrainerORM.survived.is_(None)) | (JackTrainerORM.survived == "")
            )
        )
        result = await self.session.execute(stmt)
        rows = result.all()
        logger.info("[AndrewBlueprintRepository] get_test_set | 행 수=%d", len(rows))
        return [_row_to_dict(person, booking) for person, booking in rows]

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