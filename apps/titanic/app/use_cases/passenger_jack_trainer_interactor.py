from __future__ import annotations
import logging
from typing import Any

from kiwipiepy import Kiwi

from apps.titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from apps.titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.app.ports.input.passenger_rose_model_use_case import PredictionFeatures
from apps.titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository
from apps.titanic.app.use_cases.passenger_rose_model_interactor import (
    LogisticRegressionStrategy,
    RandomForestStrategy,
    XGBoostStrategy,
    LightGBMStrategy,
    CatBoostStrategy,
    DecisionTreeStrategy,
    SVMStrategy,
    KNNStrategy,
    NaiveBayesStrategy,
    KMeansPCAStrategy,
)

logger = logging.getLogger("apps")

# 실제 타이타닉 생존/사망 레이블이 있는 샘플 훈련 데이터
_TRAIN_DATA: list[tuple[PredictionFeatures, bool]] = [
    (PredictionFeatures(1, "female", 29.0, 0, 0, 211.30, "C"), True),   # 1등석 여성 — 생존
    (PredictionFeatures(1, "male",    2.0, 1, 2, 151.55, "S"), True),   # 유아 — 생존
    (PredictionFeatures(3, "male",   22.0, 1, 0,   7.25, "S"), False),  # Jack — 사망
    (PredictionFeatures(1, "female", 17.0, 1, 2, 151.55, "S"), True),   # Rose — 생존
    (PredictionFeatures(3, "male",   35.0, 0, 0,   8.05, "S"), False),  # 3등석 남성 — 사망
    (PredictionFeatures(2, "female", 14.0, 1, 0,  30.07, "S"), True),   # 2등석 여성 — 생존
    (PredictionFeatures(3, "female", 26.0, 0, 0,   7.92, "S"), False),  # 3등석 여성 — 사망
    (PredictionFeatures(1, "male",   54.0, 0, 0,  51.86, "S"), False),  # 1등석 중년남 — 사망
    (PredictionFeatures(3, "male",    8.0, 3, 1,  21.07, "S"), False),  # 3등석 아이 — 사망
    (PredictionFeatures(2, "female", 30.0, 0, 0,  13.00, "S"), True),   # 2등석 여성 — 생존
]


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository
        self.kiwi = Kiwi()

    async def train_model(self, train_set) -> JackTrainerResponse:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        strategies = [
            LogisticRegressionStrategy(),
            RandomForestStrategy(),
            XGBoostStrategy(),
            LightGBMStrategy(),
            CatBoostStrategy(),
            DecisionTreeStrategy(),
            SVMStrategy(),
            KNNStrategy(),
            NaiveBayesStrategy(),
            KMeansPCAStrategy(),
        ]

        results: dict[str, Any] = {}
        for strategy in strategies:
            correct = sum(
                1 for features, actual in _TRAIN_DATA
                if strategy.predict(features).survived == actual
            )
            accuracy = correct / len(_TRAIN_DATA)
            results[strategy.name] = {
                "accuracy": round(accuracy, 4),
                "correct": correct,
                "total": len(_TRAIN_DATA),
            }
            logger.info(
                "JackTrainerInteractor: %s accuracy=%.4f (%d/%d)",
                strategy.name, accuracy, correct, len(_TRAIN_DATA),
            )

        return results

    async def analyze_message_intent(self, user_message: str) -> dict:
        tokens = self.kiwi.tokenize(user_message)
        keywords = [token.form for token in tokens if token.tag in ("NNG", "NNP", "VV", "VA")]
        return {
            "keywords": keywords,
            "raw_tokens": [(token.form, token.tag) for token in tokens],
        }

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 도슨의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name,
        ))
