from __future__ import annotations

import logging

from apps.automode.adapter.outbound.clients.exaone_slm_client import ExaoneSLMClient
from apps.automode.adapter.outbound.clients.telegram_client import TelegramClient
from apps.automode.adapter.outbound.gateways.n8n_email_gateway import N8nEmailGateway
from apps.automode.app.dtos.email_request_dto import EmailSendCommand
from apps.automode.app.dtos.telegram_dto import TelegramSendCommand
from apps.automode.app.use_cases.email_send_interactor import EmailSendInteractor
from apps.automode.app.use_cases.orchestrator_interactor import OrchestratorInteractor
from core.lol.faker_orchestrator import FakerOrchestrator

logger = logging.getLogger("apps")

_ORCHESTRATOR_MODEL = "exaone3.5:7.8b"


def get_orchestrator() -> OrchestratorInteractor:
    telegram_client = TelegramClient()
    email_uc = EmailSendInteractor(
        slm=ExaoneSLMClient(),  # 워커: 2.4B (기본값)
        gateway=N8nEmailGateway(),
        telegram=telegram_client,
    )

    faker = FakerOrchestrator()

    async def _email_send(to: str, to_name: str = "", prompt: str = "") -> dict:
        result = await email_uc.send(
            EmailSendCommand(to=to, prompt=prompt, to_name=to_name)
        )
        return {"to": result.to, "to_name": to_name, "subject": result.subject}

    async def _telegram_send(text: str) -> dict:
        result = await telegram_client.send_message(TelegramSendCommand(text=text))
        return {"ok": result.ok, "message_id": result.message_id}

    faker.register("email_send", _email_send)
    faker.register("telegram_send", _telegram_send)

    return OrchestratorInteractor(
        slm=ExaoneSLMClient(model=_ORCHESTRATOR_MODEL),  # 오케스트레이터: 7.8B
        orchestrator=faker,
    )
