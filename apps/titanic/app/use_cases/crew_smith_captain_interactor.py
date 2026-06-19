from __future__ import annotations
import logging
import pandas as pd

from apps.chat.app.iris_model import IrisModel
from apps.titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatSchema,
    SmithCaptainChatRequestSchema,
    SmithCaptainResponseSchema,
)
from apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse, SmithCaptainChatResult
from apps.titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from apps.titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort
from apps.titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from apps.titanic.app.ports.input.crew_andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.app.ports.input.crew_a_architect_use_case import AArchitectUseCase
from apps.titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from apps.titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase


logger = logging.getLogger("apps")

# 서버 기동 후 첫 채팅 때 1회 훈련 → 이후 재사용 (socket hang up 방지)
_STATS_CACHE: dict = {}

_CAPTAIN_PERSONA = [
    {
        "role": "user",
        "parts": [
            "당신은 RMS 타이타닉호의 선장 에드워드 존 스미스입니다. "
            "타이타닉의 침몰은 이미 역사적 사실이며, 당신은 그 모든 역사를 알고 있습니다. 어떠한 질문을 받으면, "
            "프롬프트 앞부분에 제공된 [타이타닉 실제 DB 통계] 수치를 핵심 숫자 1~2개만 인용하여 답하세요. "
            "'아직 일어나지 않은 일'이라는 표현은 쓰지 마세요. "
            "답변은 반드시 3문장 이내로 간결하게 마치세요. "
            "선장으로서의 무게감을 담되, 길게 설명하지 마세요."
        ],
    },
    {
        "role": "model",
        "parts": [
            "알겠소. 나는 에드워드 존 스미스 선장이오. "
            "타이타닉의 비극은 이미 역사에 기록된 사실이오. "
            "그날 밤의 일, 승객들의 기록, 무엇이든 물어보시오."
        ],
    },
]


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
        self,
        repository: SmithCaptainPort,
        a: AArchitectUseCase,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
        cal: CalTesterUseCase,
        andrew: AndrewBlueprintUseCase,
        lowe: LoweBoatUseCase,
        hartley: HartleyViolinUseCase,
    ):
        self.repository = repository
        self.a: AArchitectUseCase = a
        self.jack: JackTrainerUseCase = jack
        self.rose: RoseModelUseCase = rose
        self.cal: CalTesterUseCase = cal
        self.andrew: AndrewBlueprintUseCase = andrew
        self.lowe: LoweBoatUseCase = lowe
        self.hartley: HartleyViolinUseCase = hartley

    async def _build_stats_cache(self) -> None:
        """첫 채팅 요청 시 1회만 실행 — 모델 훈련 + 통계 계산 결과를 모듈 캐시에 저장."""
        train_set: pd.DataFrame = await self.andrew.get_train_set()
        test_set:  pd.DataFrame = await self.andrew.get_test_set()

        if train_set.empty:
            _STATS_CACHE["context"] = "[타이타닉 DB에 데이터가 없습니다. 데이터 수집 페이지에서 CSV를 먼저 업로드해 주세요.]"
            _STATS_CACHE["best_algo"] = "없음"
            _STATS_CACHE["best_acc"] = 0.0
            logger.warning("SmithCaptainInteractor: DB가 비어 있어 통계 캐시를 빌드할 수 없습니다.")
            return

        X, y        = self.lowe.feature_engineering(train_set, test_set)
        trained_set = self.jack.train_model(X, y)
        tested_set  = self.cal.test_model(trained_set)

        best_algo = tested_set.get("algorithm", "XGBoost")
        best_acc  = tested_set.get("accuracy", 0.0)

        df = train_set.copy()
        df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
        df["age"]      = pd.to_numeric(df["age"],      errors="coerce")
        df["pclass"]   = pd.to_numeric(df["pclass"],   errors="coerce")

        total          = len(df)
        survived_count = int(df["survived"].sum())

        gender_rate = df.groupby("gender")["survived"].mean() * 100
        female_rate = gender_rate.get("female", 0.0)
        male_rate   = gender_rate.get("male",   0.0)

        pclass_rate = df.groupby("pclass")["survived"].mean() * 100

        bins   = [0, 12, 18, 35, 60, 120]
        labels = ["0~12세(어린이)", "13~18세(청소년)", "19~35세(청년)", "36~60세(중장년)", "60세 이상"]
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)
        age_rate  = df.groupby("age_group", observed=True)["survived"].mean() * 100
        combo     = df.groupby(["gender", "pclass"])["survived"].mean() * 100
        corr      = X.apply(pd.to_numeric, errors="coerce").corrwith(
            pd.Series(y, index=X.index)
        ).abs().sort_values(ascending=False)

        _STATS_CACHE["context"] = (
            f"[타이타닉 실제 DB 통계 — 891명]\n"
            f"총 승객: {total}명 | 생존: {survived_count}명 ({survived_count/total:.1%}) | 사망: {total - survived_count}명\n\n"
            f"[성별 생존율]\n  여성: {female_rate:.1f}%\n  남성: {male_rate:.1f}%\n\n"
            f"[객실 등급별 생존율]\n"
            + "\n".join(f"  {int(pc)}등석: {r:.1f}%" for pc, r in sorted(pclass_rate.items()))
            + f"\n\n[나이대별 생존율]\n"
            + "\n".join(f"  {g}: {r:.1f}%" for g, r in age_rate.items() if not pd.isna(r))
            + f"\n\n[성별 × 등급 조합 생존율]\n"
            + "\n".join(f"  {g} {int(pc)}등석: {r:.1f}%" for (g, pc), r in sorted(combo.items()))
            + f"\n\n[생존 예측 피처 중요도 — 상관계수 절댓값 순]\n"
            + "\n".join(f"  {i+1}위 {col}: {val:.3f}" for i, (col, val) in enumerate(corr.items()))
            + f"\n\n[ML 최고 알고리즘: {best_algo} | CV 정확도: {best_acc:.1%}]"
        )
        _STATS_CACHE["best_algo"] = best_algo
        _STATS_CACHE["best_acc"]  = best_acc
        logger.info("SmithCaptainInteractor: 통계 캐시 빌드 완료")

    async def chat(self, schema: ChatSchema) -> SmithCaptainChatResult:
        question = schema.message

        if not _STATS_CACHE:
            await self._build_stats_cache()

        context   = _STATS_CACHE["context"]
        best_algo = _STATS_CACHE["best_algo"]
        best_acc  = _STATS_CACHE["best_acc"]

        prompt = f"{context}\n\n질문: {question}"
        try:
            answer = IrisModel().generate_reply(history=_CAPTAIN_PERSONA, last_user_text=prompt)
        except Exception as e:
            logger.warning("SmithCaptainInteractor: Gemini 호출 실패 | %s", e)
            answer = "지금은 답변하기 어렵소. 잠시 후 다시 물어보시오."
        return SmithCaptainChatResult(answer=answer)

    async def introduce_myself(self, schema: SmithCaptainResponseSchema) -> SmithCaptainResponse:
        '''에드워드 스미스의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name
        ))
