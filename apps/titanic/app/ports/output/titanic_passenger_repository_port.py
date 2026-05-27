from typing import Protocol

from ....domain.entities.titanic import TitanicPassenger


class TitanicPassengerRepositoryPort(Protocol):
    def save(self, passenger: TitanicPassenger) -> TitanicPassenger:
        ...
