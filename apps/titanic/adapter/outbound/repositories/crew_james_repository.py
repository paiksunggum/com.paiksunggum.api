import logging

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from ....app.dtos.crew_james_command_dto import BookingCommand, JamesCommandQuery, JamesCommandResponse, PersonCommand
from ....app.ports.output.crew_james_port import JamesPort
from ..orm.passenger_rose_model_orm import RoseModelORM
from ..orm.passenger_jack_trainer_orm import JackTrainerORM

logger = logging.getLogger("apps")


class JamesRepository(JamesPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JamesCommandQuery) -> JamesCommandResponse:

        '''제임스 감독의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[JamesRepository] introduce_myself 진입 | request_data={query}")

        response: JamesCommandResponse = JamesCommandResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response


    async def upload_passengers(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        passenger_ids = [c.passenger_id for c in person_commands]

        # 이미 존재하는 passenger_id 조회
        from sqlalchemy import select
        result = await self.session.execute(
            select(JackTrainerORM.passenger_id).where(JackTrainerORM.passenger_id.in_(passenger_ids))
        )
        existing_ids = {row[0] for row in result}

        # 신규만 필터링
        new_pairs = [
            (cp, cb)
            for cp, cb in zip(person_commands, booking_commands)
            if cp.passenger_id not in existing_ids
        ]

        if not new_pairs:
            logger.info("[JamesRepository] 신규 승객 없음 | 저장=0행")
            return 0

        new_persons, new_bookings = zip(*new_pairs)

        # persons 신규 삽입
        stmt = pg_insert(JackTrainerORM).values([
            {
                "passenger_id": c.passenger_id,
                "name": c.name,
                "gender": c.gender,
                "age": c.age,
                "sib_sp": c.sib_sp,
                "parch": c.parch,
                "survived": c.survived,
            }
            for c in new_persons
        ])
        stmt = stmt.on_conflict_do_nothing()
        await self.session.execute(stmt)
        await self.session.flush()

        # bookings 신규 삽입
        self.session.add_all([
            RoseModelORM(
                passenger_id=cp.passenger_id,
                pclass=cb.pclass,
                ticket=cb.ticket,
                fare=cb.fare,
                cabin=cb.cabin,
                embarked=cb.embarked,
            )
            for cp, cb in zip(new_persons, new_bookings)
        ])
        await self.session.commit()

        logger.info("[JamesRepository] upload_passengers 완료 | 저장=%d행", len(new_pairs))
        return len(new_pairs)
