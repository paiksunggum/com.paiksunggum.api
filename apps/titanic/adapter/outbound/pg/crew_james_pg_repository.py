import logging
from typing import Any

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import engine

from ....app.dtos.crew_james_command_dto import BookingCommand, PersonCommand
from ....app.ports.output.crew_james_repository import JamesRepository
from ..orm.booking_orm import BookingORM
from ..orm.person_orm import PersonORM

logger = logging.getLogger("apps")


class JamesPgRepository(JamesRepository):
    """James 출력 포트 → Neon(PostgreSQL) person/booking 테이블."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upload_passengers(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> dict[str, Any]:
        if engine is None:
            raise RuntimeError("DATABASE_URL is not set")

        pending: list[tuple[PersonCommand, BookingCommand]] = []
        for person_cmd, booking_cmd in zip(person_commands, booking_commands, strict=True):
            if not person_cmd.passenger_id:
                continue
            pending.append((person_cmd, booking_cmd))

        async with self._session.begin():
            await self._session.execute(delete(BookingORM))
            await self._session.execute(delete(PersonORM))

            for person_cmd, _ in pending:
                self._session.add(PersonORM.from_command(person_cmd))
            await self._session.flush()

            for person_cmd, booking_cmd in pending:
                self._session.add(
                    BookingORM.from_command(person_cmd.passenger_id, booking_cmd),
                )

        inserted = len(pending)
        logger.info(
            "[JamesPgRepository] Neon 저장 완료 | persons/bookings 각 %d행",
            inserted,
        )

        return {
            "ok": True,
            "inserted": inserted,
            "rowCount": inserted,
            "dataRowCount": inserted,
            "storedIn": "neon",
        }
