from __future__ import annotations
import logging
from typing import Any

import pandas as pd
from kiwipiepy import Kiwi
from sklearn.model_selection import StratifiedKFold, cross_val_score

from apps.titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from apps.titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort
from apps.titanic.app.use_cases.passenger_rose_model_interactor import (
    LogisticRegressionStrategy,
    RandomForestStrategy,
    XGBoostStrategy,
    LightGBMStrategy,
    DecisionTreeStrategy,
    SVMStrategy,
    KNNStrategy,
    NaiveBayesStrategy,
    VotingEnsembleStrategy,
)

logger = logging.getLogger("apps")


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerPort):
        self.repository = repository
        self.kiwi = Kiwi()

    def train_model(self, X, y: list) -> JackTrainerResponse:
        '''Lowe 피처(X)와 레이블(y)로 로즈 전략들을 훈련 + Stratified 5-Fold 교차검증'''
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

        strategies = [
            LogisticRegressionStrategy(),
            RandomForestStrategy(),
            XGBoostStrategy(),
            LightGBMStrategy(),
            DecisionTreeStrategy(),
            SVMStrategy(),
            KNNStrategy(),
            NaiveBayesStrategy(),
            VotingEnsembleStrategy(),
        ]

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        results: dict[str, Any] = {}

        for strategy in strategies:
            # 전체 데이터로 fit (최종 모델)
            strategy.fit(X, y)

            # 5-Fold 교차검증으로 정확도 측정
            sklearn_model = strategy._model
            scores = cross_val_score(sklearn_model, X, y, cv=cv, scoring="accuracy", n_jobs=-1)
            accuracy = float(scores.mean())
            std      = float(scores.std())

            results[strategy.name] = {
                "accuracy": round(accuracy, 4),
                "std":      round(std, 4),
                "cv_scores": [round(s, 4) for s in scores.tolist()],
            }
            logger.info(
                "JackTrainerInteractor: %s  CV accuracy=%.4f (±%.4f)",
                strategy.name, accuracy, std,
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
