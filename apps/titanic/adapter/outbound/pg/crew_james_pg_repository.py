import logging
from typing import Any

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import engine

from ....app.dtos.crew_james_command_dto import BookingCommand, JamesCommandQuery, JamesCommandResponse, PersonCommand
from ....app.ports.output.crew_james_repository import JamesRepository
from ..orm.passenger_rose_model_orm import RoseModelORM
from ..orm.passenger_jack_trainer_orm import JackTrainerORM

logger = logging.getLogger("apps")


class JamesPgRepository(JamesRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JamesCommandQuery) -> JamesCommandResponse:

        '''제임스 감독의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[JamesPgRepository] introduce_myself 진입 | request_data={query}")

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
        person_orms = [
            JackTrainerORM(
                passenger_id=command.passenger_id,
                name=command.name,
                gender=command.gender,
                age=command.age,
                sib_sp=command.sib_sp,
                parch=command.parch,
                survived=command.survived,
            )
            for command in person_commands
        ]
        self.session.add_all(person_orms)
        await self.session.flush()

        booking_orms = [
            RoseModelORM(
                passenger_id=person_orm.passenger_id,
                pclass=command.pclass,
                ticket=command.ticket,
                fare=command.fare,
                cabin=command.cabin,
                embarked=command.embarked,
            )
            for person_orm, command in zip(person_orms, booking_commands)
        ]
        self.session.add_all(booking_orms)
        await self.session.commit()

        return len(person_orms)

        