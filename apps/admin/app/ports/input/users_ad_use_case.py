from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.admin.adapter.inbound.api.schemas.users_ad_schema import UsersAdSchema
from apps.admin.app.dtos.users_ad_dto import UsersAdResponse


class UsersAdUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: UsersAdSchema) -> UsersAdResponse:
        '''users_ad 의 자기소개 메소드'''
        pass
