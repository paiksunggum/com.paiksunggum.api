from __future__ import annotations

from apps.automode.adapter.outbound.clients.telegram_client import TelegramClient
from apps.automode.app.ports.input.telegram_use_case import TelegramUseCase
from apps.automode.app.ports.output.telegram_port import TelegramPort
from apps.automode.app.use_cases.telegram_interactor import TelegramInteractor


def get_telegram_client() -> TelegramPort:
    return TelegramClient()


def get_telegram_use_case() -> TelegramUseCase:
    return TelegramInteractor(repository=get_telegram_client())
