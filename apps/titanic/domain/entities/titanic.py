from dataclasses import dataclass


@dataclass(frozen=True)
class TitanicPassenger:
    passenger_id: str
    survived: str
    pclass: str
    name: str
    gender: str
    age: str
    sibsp: str
    parch: str
    ticket: str
    fare: str
    cabin: str
    embarked: str
