from __future__ import annotations

import logging
from typing import Any
from kiwipiepy import Kiwi

from apps.titanic.app.constants.intent_map import INTENT_MAP
from apps.titanic.adapter.inbound.api.schemas.crew_a_architect_schema import AArchitectSchema
from apps.titanic.app.dtos.crew_a_architect_dto import AArchitectQuery, AArchitectResponse
from apps.titanic.app.ports.input.crew_a_architect_use_case import AArchitectUseCase
from apps.titanic.app.ports.output.crew_a_architect_port import AArchitectPort

logger = logging.getLogger("apps")


class AArchitectInteractor(AArchitectUseCase):
    
    def __init__(self, repository: AArchitectPort):
        self.repository = repository
        self.kiwi = Kiwi()

    def analyze_intent(self, question: str) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 프론트 질문의 의도를 파악하는 메소드

        반환값:
            intent   : 감지된 의도 (SURVIVAL_PREDICT / STATISTICS / PASSENGER_SEARCH / MODEL_TRAIN / UNKNOWN)
            keywords : 분석에 사용된 핵심 형태소 목록
            scores   : 의도별 매칭 점수
            tokens   : Kiwi가 분석한 전체 (형태소, 품사) 쌍 목록
        '''
        # 명사(NN*), 동사 어간(VV/VA), 파생어근(XR)만 의도 판별에 사용
        tokens = self.kiwi.tokenize(question)
        keywords = [t.form for t in tokens if t.tag.startswith(("NN", "VV", "VA", "XR"))]

        scores: dict[str, int] = {intent: 0 for intent in INTENT_MAP}
        for keyword in keywords:
            for intent, kw_set in INTENT_MAP.items():
                if keyword in kw_set:
                    scores[intent] += 1

        best_intent = max(scores, key=lambda k: scores[k])
        intent = best_intent if scores[best_intent] > 0 else "UNKNOWN"

        logger.info(
            f"[AArchitectInteractor] analyze_intent | question={question!r} "
            f"intent={intent} scores={scores}"
        )
        return {
            "intent": intent,
            "keywords": keywords,
            "scores": scores,
            "tokens": [(t.form, str(t.tag)) for t in tokens],
        }

    async def introduce_myself(self, schema: AArchitectSchema) -> AArchitectResponse:
        '''토마스 에이 아키텍트의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(AArchitectQuery(
            id = schema.id,
            name = schema.name
        ))




