from __future__ import annotations
import logging

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from apps.titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from apps.titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from apps.titanic.app.ports.input.passenger_rose_model_use_case import (
    PredictionFeatures,
    PredictionResult,
    RoseModelUseCase,
    SurvivalPredictionStrategy,
)
from apps.titanic.app.ports.output.passenger_rose_model_port import RoseModelPort

logger = logging.getLogger("apps")

# Lowe FareBand 분위 기준 (타이타닉 훈련 데이터 기반 고정값)
_FARE_BINS = [0, 7.91, 14.45, 31.0, float("inf")]


def _features_to_df(features: PredictionFeatures) -> pd.DataFrame:
    """PredictionFeatures → Lowe 피처 엔지니어링과 동일한 포맷의 DataFrame."""
    gender = 1 if features.sex == "female" else 0
    emb    = {"C": 2, "Q": 3, "S": 1}.get(features.embarked, 1)

    age = features.age if features.age > 0 else 30.0
    if age <= 0:    age_group = 0
    elif age <= 5:  age_group = 1
    elif age <= 12: age_group = 2
    elif age <= 18: age_group = 3
    elif age <= 24: age_group = 4
    elif age <= 35: age_group = 5
    elif age <= 60: age_group = 6
    else:           age_group = 7

    fare_band = int(np.searchsorted(_FARE_BINS, features.fare, side="right"))
    fare_band = max(1, min(4, fare_band))

    return pd.DataFrame([{
        "pclass":   features.pclass,
        "gender":   gender,
        "sibsp":    features.sibsp,
        "parch":    features.parch,
        "embarked": emb,
        "Title":    0,       # 개별 예측 시 name 없으므로 Unknown
        "AgeGroup": age_group,
        "FareBand": fare_band,
    }])


class LogisticRegressionStrategy(SurvivalPredictionStrategy):
    """선형 관계 기반 이진 분류. 각 피처가 생존에 미치는 영향을 직관적으로 해석."""

    def __init__(self):
        self._model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(C=0.5, max_iter=1000, random_state=42)),
        ])

    @property
    def name(self) -> str:
        return "LogisticRegression"

    def fit(self, X: pd.DataFrame, y: list) -> None:
        self._model.fit(X, y)

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        df = _features_to_df(features)
        prob = float(self._model.predict_proba(df)[0][1])
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class RandomForestStrategy(SurvivalPredictionStrategy):
    """다수 결정 트리 결합(배깅). 노이즈에 강하고 안정적인 Baseline."""

    def __init__(self):
        self._model = RandomForestClassifier(
            n_estimators=300, max_depth=6, min_samples_split=4,
            min_samples_leaf=2, random_state=42, n_jobs=-1,
        )

    @property
    def name(self) -> str:
        return "RandomForest"

    def fit(self, X: pd.DataFrame, y: list) -> None:
        self._model.fit(X, y)

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        df = _features_to_df(features)
        prob = float(self._model.predict_proba(df)[0][1])
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class XGBoostStrategy(SurvivalPredictionStrategy):
    """그래디언트 부스팅 기반 고성능 모델. 리더보드 최상위권."""

    def __init__(self):
        self._model = XGBClassifier(
            n_estimators=200, max_depth=4, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            eval_metric="logloss", random_state=42, verbosity=0,
        )

    @property
    def name(self) -> str:
        return "XGBoost"

    def fit(self, X: pd.DataFrame, y: list) -> None:
        self._model.fit(X, y)

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        df = _features_to_df(features)
        prob = float(self._model.predict_proba(df)[0][1])
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class LightGBMStrategy(SurvivalPredictionStrategy):
    """리프 중심(Leaf-wise) 트리 분할. 속도와 성능 균형."""

    def __init__(self):
        self._model = LGBMClassifier(
            n_estimators=200, max_depth=5, learning_rate=0.05,
            num_leaves=31, subsample=0.8, random_state=42, verbose=-1,
        )

    @property
    def name(self) -> str:
        return "LightGBM"

    def fit(self, X: pd.DataFrame, y: list) -> None:
        self._model.fit(X, y)

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        df = _features_to_df(features)
        prob = float(self._model.predict_proba(df)[0][1])
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class DecisionTreeStrategy(SurvivalPredictionStrategy):
    """나무 가지치기 형태의 직관적 규칙 기반 모델. 시각화 용이."""

    def __init__(self):
        self._model = DecisionTreeClassifier(max_depth=5, random_state=42)

    @property
    def name(self) -> str:
        return "DecisionTree"

    def fit(self, X: pd.DataFrame, y: list) -> None:
        self._model.fit(X, y)

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        df = _features_to_df(features)
        prob = float(self._model.predict_proba(df)[0][1])
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class SVMStrategy(SurvivalPredictionStrategy):
    """마진 최대화 최적 결정 경계 탐색. 표준화된 데이터에서 비선형 관계 파악."""

    def __init__(self):
        self._model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", SVC(C=1.0, kernel="rbf", probability=True, random_state=42)),
        ])

    @property
    def name(self) -> str:
        return "SVM"

    def fit(self, X: pd.DataFrame, y: list) -> None:
        self._model.fit(X, y)

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        df = _features_to_df(features)
        prob = float(self._model.predict_proba(df)[0][1])
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class KNNStrategy(SurvivalPredictionStrategy):
    """가장 가까운 K개 이웃 기준 분류. 나이·요금·등급 유사도 기반."""

    def __init__(self):
        self._model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", KNeighborsClassifier(n_neighbors=7, weights="distance")),
        ])

    @property
    def name(self) -> str:
        return "KNN"

    def fit(self, X: pd.DataFrame, y: list) -> None:
        self._model.fit(X, y)

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        df = _features_to_df(features)
        prob = float(self._model.predict_proba(df)[0][1])
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class NaiveBayesStrategy(SurvivalPredictionStrategy):
    """베이즈 정리 기반 조건부 확률 분류. 희소 데이터에 강함."""

    def __init__(self):
        self._model = GaussianNB()

    @property
    def name(self) -> str:
        return "NaiveBayes"

    def fit(self, X: pd.DataFrame, y: list) -> None:
        self._model.fit(X, y)

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        df = _features_to_df(features)
        prob = float(self._model.predict_proba(df)[0][1])
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class VotingEnsembleStrategy(SurvivalPredictionStrategy):
    """상위 모델 소프트 보팅 앙상블. 단일 모델보다 안정적인 최고 성능."""

    def __init__(self):
        self._model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", VotingClassifier(
                estimators=[
                    ("xgb", XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.05,
                                          subsample=0.8, eval_metric="logloss",
                                          random_state=42, verbosity=0)),
                    ("lgb", LGBMClassifier(n_estimators=200, max_depth=5, learning_rate=0.05,
                                           num_leaves=31, subsample=0.8,
                                           random_state=42, verbose=-1)),
                    ("rf",  RandomForestClassifier(n_estimators=300, max_depth=6,
                                                   random_state=42, n_jobs=-1)),
                ],
                voting="soft",
            )),
        ])

    @property
    def name(self) -> str:
        return "VotingEnsemble"

    def fit(self, X: pd.DataFrame, y: list) -> None:
        self._model.fit(X, y)

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        df = _features_to_df(features)
        prob = float(self._model.named_steps["clf"].predict_proba(
            self._model.named_steps["scaler"].transform(df)
        )[0][1])
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


# CatBoost → VotingEnsemble로 교체 (catboost 미설치 환경 대응)
CatBoostStrategy = VotingEnsembleStrategy
KMeansPCAStrategy = KNNStrategy  # 비지도 → KNN으로 대체


class RoseModelInteractor(RoseModelUseCase):

    def __init__(
        self,
        repository: RoseModelPort,
        strategy: SurvivalPredictionStrategy | None = None,
    ):
        self.repository = repository
        self.strategy = strategy or LogisticRegressionStrategy()

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        return await self.repository.introduce_myself(RoseModelQuery(
            id=schema.id,
            name=schema.name,
        ))

    async def predict_survival(self, features: PredictionFeatures) -> PredictionResult:
        logger.info("RoseModelInteractor: features=%s", features)
        result = self.strategy.predict(features)
        logger.info("RoseModelInteractor: result=%s", result)
        return result
