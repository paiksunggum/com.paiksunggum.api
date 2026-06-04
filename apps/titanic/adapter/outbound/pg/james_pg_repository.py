import logging
from typing import Any

from sqlalchemy import delete

from core.matrix.oracle_database import AsyncSessionLocal, engine

from ....app.dtos.james_command_dto import BookingCommand, PersonCommand
from ....app.ports.output.james_repository import JamesRepository
from ..orm.booking_orm import BookingORM
from ..orm.person_orm import PersonORM

logger = logging.getLogger("apps")


def _get_cell(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        if key in row and row[key] is not None:
            value = str(row[key]).strip()
            if value:
                return value
    return ""


def _row_to_person_command(row: dict[str, str]) -> PersonCommand:
    return PersonCommand(
        passenger_id=_get_cell(row, "PassengerId", "passenger_id"),
        name=_get_cell(row, "Name", "name"),
        gender=_get_cell(row, "gender", "Sex", "sex"),
        age=_get_cell(row, "Age", "age"),
        sib_sp=_get_cell(row, "SibSp", "sib_sp", "sibsp"),
        parch=_get_cell(row, "Parch", "parch"),
        survived=_get_cell(row, "Survived", "survived"),
    )


def _row_to_booking_command(row: dict[str, str]) -> BookingCommand:
    return BookingCommand(
        pclass=_get_cell(row, "Pclass", "pclass"),
        ticket=_get_cell(row, "Ticket", "ticket"),
        fare=_get_cell(row, "Fare", "fare"),
        cabin=_get_cell(row, "Cabin", "cabin"),
        embarked=_get_cell(row, "Embarked", "embarked"),
    )


class JamesPgRepository(JamesRepository):
    """James 출력 포트 → Neon(PostgreSQL) person/booking 테이블."""

    async def upload_passengers(
        self,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        if engine is None or AsyncSessionLocal is None:
            raise RuntimeError("DATABASE_URL is not set")

        saved_rows: list[dict[str, Any]] = []
        pending: list[tuple[PersonCommand, BookingCommand, dict[str, Any]]] = []

        for source_row in records:
            row = {
                str(k): str(v) if v is not None else ""
                for k, v in source_row.items()
            }
            person_cmd = _row_to_person_command(row)
            if not person_cmd.passenger_id:
                continue
            pending.append(
                (person_cmd, _row_to_booking_command(row), source_row),
            )

        async with AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(delete(BookingORM))
                await session.execute(delete(PersonORM))

                for person_cmd, _, _ in pending:
                    session.add(PersonORM.from_command(person_cmd))
                await session.flush()

                for person_cmd, booking_cmd, source_row in pending:
                    session.add(
                        BookingORM.from_command(person_cmd.passenger_id, booking_cmd),
                    )
                    saved_rows.append(source_row)

        logger.info(
            "[제임스 pg 레포지터리] Neon 저장 완료 | persons/bookings 각 %d행",
            len(saved_rows),
        )

        return {
            "ok": True,
            "inserted": len(saved_rows),
            "rowCount": len(saved_rows),
            "data": saved_rows,
            "storedIn": "neon",
        }
