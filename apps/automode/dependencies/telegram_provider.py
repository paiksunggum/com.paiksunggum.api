from __future__ import annotations

from apps.automode.adapter.outbound.clients.telegram_client import TelegramClient
from apps.automode.app.ports.input.i_telegram_use_case import ITelegramUseCase
from apps.automode.app.ports.output.i_telegram_port import ITelegramPort
from apps.automode.app.use_cases.telegram_interactor import TelegramInteractor


def get_telegram_client() -> ITelegramPort:
    return TelegramClient()


def get_telegram_use_case() -> ITelegramUseCase:
    return TelegramInteractor(repository=get_telegram_client())
