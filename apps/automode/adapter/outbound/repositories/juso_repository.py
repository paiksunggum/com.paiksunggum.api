from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.automode.adapter.outbound.orm.juso_contact_orm import JusoContactORM
from apps.automode.app.dtos.juso_dto import (
    JusoContactCommand,
    JusoContactItem,
    JusoIntroduceQuery,
    JusoIntroduceResult,
)
from apps.automode.app.ports.output.juso_port import JusoPort

logger = logging.getLogger("apps")


class JusoRepository(JusoPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JusoIntroduceQuery) -> JusoIntroduceResult:
        return JusoIntroduceResult(id=query.id, name="주소 검색 서비스")

    async def save_contacts(self, contacts: list[JusoContactCommand]) -> int:
        rows = [
            JusoContactORM(
                first_name=c.first_name or None,
                middle_name=c.middle_name or None,
                last_name=c.last_name or None,
                nickname=c.nickname or None,
                organization_name=c.organization_name or None,
                organization_title=c.organization_title or None,
                birthday=c.birthday or None,
                labels=c.labels or None,
                email=c.email or None,
                phone=c.phone or None,
            )
            for c in contacts
        ]
        self.session.add_all(rows)
        await self.session.commit()
        logger.info("[JusoRepository] 연락처 저장 완료 | %d건", len(rows))
        return len(rows)

    async def list_contacts(self) -> list[JusoContactItem]:
        result = await self.session.execute(
            select(JusoContactORM).order_by(JusoContactORM.id)
        )
        rows = result.scalars().all()
        items: list[JusoContactItem] = []
        for row in rows:
            name = (
                row.nickname
                or f"{row.last_name or ''}{row.first_name or ''}".strip()
                or row.organization_name
                or ""
            )
            email = row.email or ""
            if name:
                items.append(JusoContactItem(name=name, email=email))
        return items
