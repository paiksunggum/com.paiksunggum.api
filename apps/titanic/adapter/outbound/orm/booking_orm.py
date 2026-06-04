from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from apps.titanic.app.dtos.james_command_dto import BookingCommand
from core.matrix.oracle_database import Base


class BookingORM(Base):
    __tablename__ = "titanic_bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("titanic_persons.passenger_id", ondelete="CASCADE"),
        index=True,
    )
    pclass: Mapped[str] = mapped_column(String(8), default="")
    ticket: Mapped[str] = mapped_column(String(64), default="")
    fare: Mapped[str] = mapped_column(String(32), default="")
    cabin: Mapped[str] = mapped_column(String(64), default="")
    embarked: Mapped[str] = mapped_column(String(8), default="")

    @classmethod
    def from_command(cls, passenger_id: str, command: BookingCommand) -> "BookingORM":
        return cls(
            passenger_id=passenger_id,
            pclass=command.pclass,
            ticket=command.ticket,
            fare=command.fare,
            cabin=command.cabin,
            embarked=command.embarked,
        )
