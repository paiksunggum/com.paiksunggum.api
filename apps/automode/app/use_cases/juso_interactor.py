from __future__ import annotations

from apps.automode.app.dtos.juso_dto import (
    JusoContactCommand,
    JusoContactItem,
    JusoContactUploadResult,
    JusoIntroduceQuery,
    JusoIntroduceResult,
)
from apps.automode.app.ports.input.juso_use_case import JusoUseCase
from apps.automode.app.ports.output.juso_port import JusoPort


class JusoInteractor(JusoUseCase):
    def __init__(self, repository: JusoPort) -> None:
        self._repository = repository

    async def introduce_myself(self, query: JusoIntroduceQuery) -> JusoIntroduceResult:
        return await self._repository.introduce_myself(query)

    async def upload_contacts(
        self, contacts: list[JusoContactCommand]
    ) -> JusoContactUploadResult:
        inserted = await self._repository.save_contacts(contacts)
        return JusoContactUploadResult(inserted=inserted)

    async def list_contacts(self) -> list[JusoContactItem]:
        return await self._repository.list_contacts()
