import logging
from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field, SQLModel

from ....app.ports.output.james_repository import JamesRepository
from ....app.ports.output.walter_repository import WalterPassengerPage, WalterRepository

logger = logging.getLogger("apps")


class TitanicPassengerModel(SQLModel, table=True):
    __tablename__ = "titanic_passengers"

    id: int | None = Field(default=None, primary_key=True)
    passenger_id: str = Field(default="", index=True)
    survived: str = ""
    pclass: str = ""
    name: str = ""
    gender: str = ""
    age: str = ""
    sibsp: str = ""
    parch: str = ""
    ticket: str = ""
    fare: str = ""
    cabin: str = ""
    embarked: str = ""


def _cell(row: dict[str, Any], *keys: str) -> str:
    for key in keys:
        if key in row and row[key] is not None:
            return str(row[key])
    return ""


class JamesPgRepository(JamesRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def upload_passengers(
        self,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        logger.info(
            "[DB저장소] PostgreSQL 업로드 시작 | 테이블=%s, %d행",
            TitanicPassengerModel.__tablename__,
            len(records),
        )
        await self._db.execute(delete(TitanicPassengerModel))
        for row in records:
            self._db.add(
                TitanicPassengerModel(
                    passenger_id=_cell(row, "PassengerId", "passenger_id"),
                    survived=_cell(row, "Survived", "survived"),
                    pclass=_cell(row, "Pclass", "pclass"),
                    name=_cell(row, "Name", "name"),
                    gender=_cell(row, "gender", "Sex"),
                    age=_cell(row, "Age", "age"),
                    sibsp=_cell(row, "SibSp", "sibsp"),
                    parch=_cell(row, "Parch", "parch"),
                    ticket=_cell(row, "Ticket", "ticket"),
                    fare=_cell(row, "Fare", "fare"),
                    cabin=_cell(row, "Cabin", "cabin"),
                    embarked=_cell(row, "Embarked", "embarked"),
                )
            )
        await self._db.commit()
        logger.info(
            "[DB저장소] PostgreSQL 업로드 완료 | %d행",
            len(records),
        )
        return {"inserted": len(records)}


class WalterPgRepository(WalterRepository):
    async def get_passengers(
        self,
        *,
        page: int,
        page_size: int,
        db: AsyncSession,
    ) -> WalterPassengerPage:
        logger.info(
            "[DB저장소] PostgreSQL 조회 시작 | 테이블=%s, page=%d, page_size=%d",
            TitanicPassengerModel.__tablename__,
            page,
            page_size,
        )
        offset = (page - 1) * page_size

        total_result = await db.execute(
            select(func.count()).select_from(TitanicPassengerModel)
        )
        total = int(total_result.scalar_one() or 0)
        total_pages = max((total + page_size - 1) // page_size, 1)

        stmt = (
            select(TitanicPassengerModel)
            .order_by(TitanicPassengerModel.id.asc())
            .offset(offset)
            .limit(page_size)
        )
        result = await db.execute(stmt)
        passengers = result.scalars().all()
        logger.info(
            "[DB저장소] PostgreSQL 조회 완료 | 전체 %d건, 반환 %d건",
            total,
            len(passengers),
        )

        return {
            "page": page,
            "pageSize": page_size,
            "total": total,
            "totalPages": total_pages,
            "items": [
                {
                    "id": item.id,
                    "passengerId": item.passenger_id,
                    "name": item.name,
                    "gender": item.gender,
                    "age": item.age,
                    "pclass": item.pclass,
                    "survived": item.survived,
                }
                for item in passengers
            ],
        }
