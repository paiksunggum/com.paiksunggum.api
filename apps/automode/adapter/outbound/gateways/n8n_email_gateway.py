from __future__ import annotations

import os

import httpx

from apps.automode.app.ports.output.email_gateway_port import EmailGatewayPort
from apps.automode.domain.entities.email_message import EmailMessage


class N8nEmailGateway(EmailGatewayPort):
    def __init__(self) -> None:
        self._webhook_url = os.getenv("N8N_WEBHOOK_URL", "")

    async def send(self, message: EmailMessage) -> None:
        async with httpx.AsyncClient() as client:
            await client.post(
                self._webhook_url,
                json={
                    "to": message.to,
                    "subject": message.subject,
                    "body": message.body,
                },
                timeout=10.0,
            )
