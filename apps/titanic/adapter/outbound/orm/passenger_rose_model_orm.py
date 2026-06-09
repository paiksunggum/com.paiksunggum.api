from __future__ import annotations

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.theone_base import TheOneBase



class RoseModelORM(TheOneBase):
    # 🍟 클래스명은 RoseModel이지만, 실제 DB 테이블은 표준 명칭으로 바인딩!
    __tablename__ = "titanic_bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    passenger_id: Mapped[str | None] = mapped_column(String, ForeignKey("titanic_persons.passenger_id"), nullable=True)
    pclass: Mapped[str | None] = mapped_column(String, nullable=True)
    ticket: Mapped[str | None] = mapped_column(String, nullable=True)
    fare: Mapped[str | None] = mapped_column(String, nullable=True)
    cabin: Mapped[str | None] = mapped_column(String, nullable=True)
    embarked: Mapped[str | None] = mapped_column(String, nullable=True)

