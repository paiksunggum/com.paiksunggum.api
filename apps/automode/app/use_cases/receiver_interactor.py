from __future__ import annotations

import logging

from apps.automode.app.dtos.receiver_dto import ReceivedEmail, ReceivedEmailCommand
from apps.automode.app.ports.input.receiver_use_case import ReceiverUseCase
from apps.automode.app.ports.output.receiver_port import ReceiverPort

logger = logging.getLogger("apps")


class ReceiverInteractor(ReceiverUseCase):
    def __init__(self, port: ReceiverPort) -> None:
        self._port = port

    async def receive(self, command: ReceivedEmailCommand) -> ReceivedEmail:
        logger.info(
            "[receiver] 수신 from=%s subject=%s", command.sender, command.subject
        )
        return await self._port.save(command)

    async def list_emails(self) -> list[ReceivedEmail]:
        return await self._port.find_all()
