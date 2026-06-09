from __future__ import annotations

from apps.titanic.app.dtos.crew_james_command_dto import (
    BookingCommand,
    JamesCommandResponse,
    PersonCommand,
)
from apps.titanic.app.ports.input.crew_james_command_use_case import JamesCommandUseCase
from apps.titanic.app.ports.output.crew_james_repository import JamesRepository
from ...adapter.inbound.api.schemas.crew_james_command_schema import JamesCommandSchema
from apps.titanic.app.dtos.crew_james_command_dto import JamesCommandQuery

class JamesCommandInteractor(JamesCommandUseCase):
    def __init__(self, repository: JamesRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: JamesCommandSchema) -> JamesCommandResponse:
        return await self.repository.introduce_myself(JamesCommandQuery(
            id = schema.id,
            name = schema.name
        ))

    async def upload_passengers(
        self, passengers: list[JamesCommandSchema]) -> dict:
        person_commands = [
            PersonCommand(
                passenger_id=record.passenger_id or "",
                name=record.name or "",
                gender=record.gender or "",
                age=record.age or "",
                sib_sp=record.sib_sp or "",
                parch=record.parch or "",
                survived=record.survived or "",
            )
            for record in passengers
        ]
        booking_commands = [
            BookingCommand(
                pclass=record.pclass or "",
                ticket=record.ticket or "",
                fare=record.fare or "",
                cabin=record.cabin or "",
                embarked=record.embarked or "",
            )
            for record in passengers
        ]

        saved = await self.repository.upload_passengers(
            person_commands,
            booking_commands,
        )

        return {"inserted": saved}

