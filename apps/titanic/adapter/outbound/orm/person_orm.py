from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from apps.titanic.app.dtos.crew_james_command_dto import PersonCommand
from core.matrix.oracle_database import Base


class PersonORM(Base):
    __tablename__ = "titanic_persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    gender: Mapped[str] = mapped_column(String(16), default="")
    age: Mapped[str] = mapped_column(String(16), default="")
    sib_sp: Mapped[str] = mapped_column(String(8), default="0")
    parch: Mapped[str] = mapped_column(String(8), default="0")
    survived: Mapped[str] = mapped_column(String(8), default="")

    @classmethod
    def from_command(cls, command: PersonCommand) -> "PersonORM":
        return cls(
            passenger_id=command.passenger_id,
            name=command.name,
            gender=command.gender,
            age=command.age,
            sib_sp=command.sib_sp,
            parch=command.parch,
            survived=command.survived,
        )
