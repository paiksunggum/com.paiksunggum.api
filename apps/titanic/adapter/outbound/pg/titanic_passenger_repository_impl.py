from ....domain.entities.titanic import TitanicPassenger


class InMemoryTitanicPassengerRepository:
    def __init__(self) -> None:
        self._store: dict[str, TitanicPassenger] = {}

    def save(self, passenger: TitanicPassenger) -> TitanicPassenger:
        if passenger.passenger_id in self._store:
            raise ValueError(
                f"PassengerId '{passenger.passenger_id}' already exists."
            )
        self._store[passenger.passenger_id] = passenger
        return passenger
