from __future__ import annotations

from abc import ABC, abstractmethod

from apps.admin.app.dtos.users_ad_dto import UsersAdQuery, UsersAdResponse


class UsersAdRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: UsersAdQuery) -> UsersAdResponse:
        '''users_ad 의 자기 소개 레포지토리 추상 메소드'''
        pass
