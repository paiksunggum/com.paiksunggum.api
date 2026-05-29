from typing import Any
import logging

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import AsyncSessionLocal, Base, engine

from ....app.ports.output.james_repository import JamesRepository
from ....domain.entities.titanic import TitanicPassenger

logger = logging.getLogger("apps")


class TitanicPassengerModel(Base):
    __tablename__ = "titanic_passengers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[str] = mapped_column(String(32), index=True)
    survived: Mapped[str] = mapped_column(String(8))
    pclass: Mapped[str] = mapped_column(String(8))
    name: Mapped[str] = mapped_column(String(255))
    gender: Mapped[str] = mapped_column(String(16))
    age: Mapped[str] = mapped_column(String(16), default="")
    sibsp: Mapped[str] = mapped_column(String(8), default="0")
    parch: Mapped[str] = mapped_column(String(8), default="0")
    ticket: Mapped[str] = mapped_column(String(64), default="")
    fare: Mapped[str] = mapped_column(String(32), default="")
    cabin: Mapped[str] = mapped_column(String(64), default="")
    embarked: Mapped[str] = mapped_column(String(8), default="")


def _get_cell(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        if key in row and row[key] is not None:
            value = str(row[key]).strip()
            if value:
                return value
    return ""


def _row_to_domain(row: dict[str, str]) -> TitanicPassenger:
    return TitanicPassenger(
        passenger_id=_get_cell(row, "PassengerId", "passenger_id"),
        survived=_get_cell(row, "Survived", "survived"),
        pclass=_get_cell(row, "Pclass", "pclass"),
        name=_get_cell(row, "Name", "name"),
        gender=_get_cell(row, "gender", "Sex", "sex"),
        age=_get_cell(row, "Age", "age"),
        sibsp=_get_cell(row, "SibSp", "sibsp"),
        parch=_get_cell(row, "Parch", "parch"),
        ticket=_get_cell(row, "Ticket", "ticket"),
        fare=_get_cell(row, "Fare", "fare"),
        cabin=_get_cell(row, "Cabin", "cabin"),
        embarked=_get_cell(row, "Embarked", "embarked"),
    )


def _domain_to_model(passenger: TitanicPassenger) -> TitanicPassengerModel:
    return TitanicPassengerModel(
        passenger_id=passenger.passenger_id,
        survived=passenger.survived,
        pclass=passenger.pclass,
        name=passenger.name,
        gender=passenger.gender,
        age=passenger.age,
        sibsp=passenger.sibsp,
        parch=passenger.parch,
        ticket=passenger.ticket,
        fare=passenger.fare,
        cabin=passenger.cabin,
        embarked=passenger.embarked,
    )


class JamesPgRepository(JamesRepository):
    """James 출력 포트 → Neon(PostgreSQL) 어댑터."""

    async def upload_passengers(
        self,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        if engine is None or AsyncSessionLocal is None:
            raise RuntimeError("DATABASE_URL is not set")

        logger.info(
            "[DB저장소] PostgreSQL 저장 시작 | 승객 %d행",
            len(records),
        )
        saved_rows: list[dict[str, Any]] = []

        async with AsyncSessionLocal() as session:
            async with session.begin():
                for source_row in records:
                    row = {str(k): str(v) if v is not None else "" for k, v in source_row.items()}
                    domain_passenger = _row_to_domain(row)
                    session.add(_domain_to_model(domain_passenger))
                    saved_rows.append(source_row)

        logger.info(
            "[DB저장소] PostgreSQL 저장 완료 | 삽입 %d행, 테이블=%s",
            len(saved_rows),
            TitanicPassengerModel.__tablename__,
        )

        return {
            "ok": True,
            "rowCount": len(saved_rows),
            "data": saved_rows,
            "storedIn": "neon",
        }
