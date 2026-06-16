from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from apps.titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from apps.titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse


@dataclass(frozen=True)
class PredictionFeatures:
    pclass: int      # 객실 등급: 1, 2, 3
    sex: str         # "male" / "female"
    age: float
    sibsp: int       # 형제자매·배우자 수
    parch: int       # 부모·자녀 수
    fare: float
    embarked: str    # "C" / "Q" / "S"


@dataclass(frozen=True)
class PredictionResult:
    survived: bool
    probability: float
    algorithm: str


class SurvivalPredictionStrategy(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def predict(self, features: PredictionFeatures) -> PredictionResult:
        pass


class RoseModelUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        pass

    @abstractmethod
    async def predict_survival(self, features: PredictionFeatures) -> PredictionResult:
        pass
