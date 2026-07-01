from __future__ import annotations

import uuid
from datetime import datetime

from apps.automode.app.dtos.receiver_dto import ReceivedEmail, ReceivedEmailCommand
from apps.automode.app.ports.output.receiver_port import ReceiverPort


class InMemoryReceiverRepository(ReceiverPort):
    def __init__(self) -> None:
        self._store: list[ReceivedEmail] = []

    async def save(self, command: ReceivedEmailCommand) -> ReceivedEmail:
        email = ReceivedEmail(
            id=str(uuid.uuid4()),
            subject=command.subject,
            body=command.body,
            sender=command.sender,
            source=command.source,
            received_at=datetime.utcnow(),
        )
        self._store.append(email)
        return email

    async def find_all(self) -> list[ReceivedEmail]:
        return list(reversed(self._store))
