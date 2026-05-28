import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ....app.ports.output.walter_repository import WalterPassengerPage
from .james_pg_repository import TitanicPassengerModel

logger = logging.getLogger("apps")


class WalterPgRepository:
    async def read_passengers(
        self,
        *,
        page: int,
        page_size: int,
        db: AsyncSession,
    ) -> WalterPassengerPage:
        logger.info(
            "[WalterPgRepository] query start - table=%s, page=%d, page_size=%d",
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
            "[WalterPgRepository] query done - total=%d, returned=%d",
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
