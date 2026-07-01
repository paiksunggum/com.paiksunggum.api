from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from apps.automode.adapter.inbound.api.schemas.orchestrate_schema import (
    OrchestrateResponseSchema,
    OrchestrateSchema,
)
from apps.automode.app.ports.input.juso_use_case import JusoUseCase
from apps.automode.app.ports.input.orchestrator_use_case import OrchestratorUseCase
from apps.automode.dependencies.juso_provider import get_juso_use_case
from apps.automode.dependencies.orchestrator_provider import get_orchestrator

logger = logging.getLogger("apps")

orchestrate_router = APIRouter(prefix="/orchestrate", tags=["automode"])


@orchestrate_router.post("/", response_model=OrchestrateResponseSchema)
async def orchestrate(
    schema: OrchestrateSchema,
    interactor: OrchestratorUseCase = Depends(get_orchestrator),
    juso: JusoUseCase = Depends(get_juso_use_case),
) -> OrchestrateResponseSchema:
    logger.info("[orchestrator] 명령 수신: %s", schema.message)

    contacts_list = await juso.list_contacts()
    contacts = {c.name: c.email for c in contacts_list}

    result = await interactor.handle(message=schema.message, contacts=contacts)

    tool = result["tool"]
    r = result["result"]

    if tool == "email_send":
        recipient = r.get("to_name") or r["to"]
        msg = f"{recipient}에게 이메일이 발송되었습니다. 제목: {r['subject']}"
    elif tool == "telegram_send":
        msg = "텔레그램 메시지 전송 완료"
    else:
        msg = "처리 완료"

    logger.info("[orchestrator] 완료 tool=%s", tool)
    return OrchestrateResponseSchema(tool=tool, message=msg)
