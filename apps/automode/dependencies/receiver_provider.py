from __future__ import annotations

from apps.automode.adapter.outbound.repositories.receiver_repository import (
    InMemoryReceiverRepository,
)
from apps.automode.app.use_cases.receiver_interactor import ReceiverInteractor

_repository = InMemoryReceiverRepository()
_interactor = ReceiverInteractor(port=_repository)


def get_receiver_use_case() -> ReceiverInteractor:
    return _interactor
