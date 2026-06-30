from __future__ import annotations

from apps.automode.app.dtos.juso_dto import (
    JusoContactCommand,
    JusoContactItem,
    JusoContactUploadResult,
    JusoIntroduceQuery,
    JusoIntroduceResult,
)
from apps.automode.app.ports.input.i_juso_use_case import IJusoUseCase
from apps.automode.app.ports.output.i_juso_port import IJusoPort


class JusoInteractor(IJusoUseCase):
    def __init__(self, repository: IJusoPort) -> None:
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
