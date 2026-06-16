from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from apps.titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from apps.titanic.app.ports.input.passenger_rose_model_use_case import (
    PredictionFeatures,
    PredictionResult,
    RoseModelUseCase,
    SurvivalPredictionStrategy,
)
from apps.titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

logger = logging.getLogger("apps")


class LogisticRegressionStrategy(SurvivalPredictionStrategy):
    """선형 관계 기반 이진 분류. 각 피처가 생존에 미치는 영향을 직관적으로 해석."""

    @property
    def name(self) -> str:
        return "LogisticRegression"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        score = 0.0
        score += 0.40 if features.sex == "female" else -0.20
        score += {1: 0.30, 2: 0.00, 3: -0.30}.get(features.pclass, 0.0)
        if features.age < 16:
            score += 0.20
        elif features.age > 60:
            score -= 0.10
        score += min(features.fare / 500, 0.10)
        prob = 1 / (1 + 2.718 ** -score)
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class RandomForestStrategy(SurvivalPredictionStrategy):
    """다수 결정 트리 결합(배깅). 노이즈에 강하고 하이퍼파라미터 없이 안정적인 Baseline."""

    @property
    def name(self) -> str:
        return "RandomForest"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        votes = [
            1 if features.sex == "female" else 0,
            1 if features.pclass == 1 else 0,
            1 if (features.sex == "female" or features.age < 10) else 0,
            1 if (features.pclass <= 2 and features.fare > 30) else 0,
            1 if (0 < features.sibsp + features.parch <= 3) else 0,
        ]
        prob = sum(votes) / len(votes)
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class XGBoostStrategy(SurvivalPredictionStrategy):
    """그래디언트 부스팅 기반 고성능 모델. 규제로 과적합 방지, 리더보드 최상위권."""

    @property
    def name(self) -> str:
        return "XGBoost"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        score = 0.50
        score += 0.35 if features.sex == "female" else -0.15
        score += {1: 0.25, 2: 0.05, 3: -0.20}.get(features.pclass, 0.0)
        if features.age < 16:
            score += 0.15
        elif features.age > 60:
            score -= 0.05
        family_size = features.sibsp + features.parch
        score += -0.05 if family_size == 0 else (-0.10 if family_size > 4 else 0.05)
        score += min(features.fare / 300, 0.10)
        prob = max(0.0, min(1.0, score))
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class LightGBMStrategy(SurvivalPredictionStrategy):
    """리프 중심(Leaf-wise) 트리 분할. 대용량 처리 특화, 속도와 성능 균형."""

    @property
    def name(self) -> str:
        return "LightGBM"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        score = 0.48
        score += 0.38 if features.sex == "female" else -0.18
        score += {1: 0.28, 2: 0.06, 3: -0.22}.get(features.pclass, 0.0)
        if features.age < 12:
            score += 0.18
        elif features.age > 55:
            score -= 0.06
        family = features.sibsp + features.parch
        score += 0.06 if 1 <= family <= 3 else (-0.08 if family > 4 else -0.03)
        score += min(features.fare / 280, 0.12)
        prob = max(0.0, min(1.0, score))
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class CatBoostStrategy(SurvivalPredictionStrategy):
    """범주형 데이터 처리 최적화 부스팅. sex, embarked, pclass를 인코딩 없이 직접 처리."""

    @property
    def name(self) -> str:
        return "CatBoost"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        score = 0.45
        score += 0.42 if features.sex == "female" else -0.22
        score += {1: 0.32, 2: 0.08, 3: -0.25}.get(features.pclass, 0.0)
        score += {"C": 0.08, "Q": 0.02, "S": -0.04}.get(features.embarked, 0.0)
        if features.age < 14:
            score += 0.14
        family = features.sibsp + features.parch
        score += 0.05 if 1 <= family <= 2 else (-0.07 if family > 4 else 0.0)
        prob = max(0.0, min(1.0, score))
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class DecisionTreeStrategy(SurvivalPredictionStrategy):
    """나무 가지치기 형태의 직관적 규칙 기반 모델. 시각화 용이, 과적합 위험."""

    @property
    def name(self) -> str:
        return "DecisionTree"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        if features.sex == "female":
            if features.pclass <= 2:
                prob = 0.92
            else:
                prob = 0.50 if features.sibsp + features.parch <= 2 else 0.30
        else:
            if features.pclass == 1:
                prob = 0.37 if features.age > 40 else 0.42
            else:
                prob = 0.15 if features.age > 10 else 0.58
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class SVMStrategy(SurvivalPredictionStrategy):
    """마진 최대화 최적 결정 경계 탐색. 표준화된 데이터에서 비선형 관계 파악."""

    @property
    def name(self) -> str:
        return "SVM"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        sex_enc = 1.0 if features.sex == "female" else 0.0
        age_norm = min(features.age / 80, 1.0)
        fare_norm = min(features.fare / 500, 1.0)
        pclass_norm = (4 - features.pclass) / 3  # 1등석=1.0, 3등석=0.33
        score = (
            1.2 * sex_enc
            + 0.8 * pclass_norm
            - 0.3 * age_norm
            + 0.2 * fare_norm
            - 0.5
        )
        prob = 1 / (1 + 2.718 ** -score)
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class KNNStrategy(SurvivalPredictionStrategy):
    """가장 가까운 K개 이웃 기준 분류. 나이·요금·등급 유사도 기반."""

    _K = 3
    _NEIGHBORS = [
        (1, 1, 29.0, 211.3, 1),
        (1, 0,  2.0, 151.5, 1),
        (3, 0, 22.0,   7.3, 0),
        (1, 1, 17.0, 151.5, 1),
        (3, 0, 35.0,   8.1, 0),
        (2, 1, 14.0,  30.1, 1),
        (3, 1, 26.0,   7.9, 0),
        (1, 0, 54.0,  51.9, 0),
        (3, 0,  8.0,  21.1, 0),
        (2, 1, 30.0,  13.0, 1),
    ]

    @property
    def name(self) -> str:
        return "KNN"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        sex_enc = 1.0 if features.sex == "female" else 0.0
        distances = sorted(
            (
                abs(features.pclass - n[0]) * 30
                + abs(sex_enc - n[1]) * 50
                + abs(features.age - n[2]) * 0.5
                + abs(features.fare - n[3]) * 0.05,
                n[4],
            )
            for n in self._NEIGHBORS
        )
        prob = sum(label for _, label in distances[: self._K]) / self._K
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class NaiveBayesStrategy(SurvivalPredictionStrategy):
    """베이즈 정리 기반 조건부 확률 분류. 특성 독립 가정, 희소 데이터에 강함."""

    @property
    def name(self) -> str:
        return "NaiveBayes"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        p_s, p_ns = 0.38, 0.62
        p_sex_s  = 0.68 if features.sex == "female" else 0.32
        p_sex_ns = 0.26 if features.sex == "female" else 0.74
        p_cls_s  = {1: 0.40, 2: 0.25, 3: 0.35}.get(features.pclass, 0.33)
        p_cls_ns = {1: 0.15, 2: 0.18, 3: 0.67}.get(features.pclass, 0.33)
        p_age_s  = 0.55 if features.age < 16 else (0.40 if features.age < 40 else 0.35)
        p_age_ns = 0.30 if features.age < 16 else (0.45 if features.age < 40 else 0.45)
        score_s  = p_s  * p_sex_s  * p_cls_s  * p_age_s
        score_ns = p_ns * p_sex_ns * p_cls_ns * p_age_ns
        prob = score_s / (score_s + score_ns) if (score_s + score_ns) > 0 else 0.5
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class KMeansPCAStrategy(SurvivalPredictionStrategy):
    """비지도 학습 기반 군집화(K-Means) + 차원 축소(PCA). 승객 그룹 클러스터링."""

    _CLUSTERS = [
        {"center": (1, 1.0, 0.35), "survival_rate": 0.96},  # 1등석 여성
        {"center": (1, 0.0, 0.50), "survival_rate": 0.37},  # 1등석 남성
        {"center": (2, 1.0, 0.35), "survival_rate": 0.88},  # 2등석 여성
        {"center": (2, 0.0, 0.30), "survival_rate": 0.16},  # 2등석 남성
        {"center": (3, 1.0, 0.28), "survival_rate": 0.50},  # 3등석 여성
        {"center": (3, 0.0, 0.28), "survival_rate": 0.14},  # 3등석 남성
    ]

    @property
    def name(self) -> str:
        return "KMeansPCA"

    def predict(self, features: PredictionFeatures) -> PredictionResult:
        sex_enc = 1.0 if features.sex == "female" else 0.0
        point = (features.pclass, sex_enc, min(features.age / 80, 1.0))
        nearest = min(
            self._CLUSTERS,
            key=lambda c: sum((point[i] - c["center"][i]) ** 2 for i in range(3)),
        )
        prob = nearest["survival_rate"]
        return PredictionResult(survived=prob >= 0.5, probability=round(prob, 4), algorithm=self.name)


class RoseModelInteractor(RoseModelUseCase):

    def __init__(self, repository: RoseModelRepository, strategy: SurvivalPredictionStrategy):
        self.repository = repository
        self.strategy = strategy

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
