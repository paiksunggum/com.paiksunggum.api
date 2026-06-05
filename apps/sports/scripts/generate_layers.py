"""One-off generator for Forma CRUD layers. Run from backend/: python apps/forma/scripts/generate_layers.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "app"

NEW = [
    ("analysis_history", "AnalysisHistory"),
    ("feedback_comments", "FeedbackComment"),
    ("video_practice_match", "VideoPracticeMatch"),
    ("user_skills", "UserSkill"),
    ("payment_logs", "PaymentLog"),
    ("users_ad", "UsersAd"),
    ("ad_stats_daily", "AdStatsDaily"),
]


def write_repo(mod: str, cls: str) -> None:
    path = ROOT / "repositories" / f"{mod}_repository.py"
    path.write_text(
        f"""from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.{mod}_model import {cls}


class {cls}Repository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: {cls}) -> {cls}:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[{cls}]:
        result = await self.session.execute(select({cls}).order_by({cls}.id.desc()))
        return list(result.scalars().all())
""",
        encoding="utf-8",
    )


def write_service(mod: str, cls: str) -> None:
    path = ROOT / "services" / f"{mod}_service.py"
    path.write_text(
        f"""from sqlalchemy.ext.asyncio import AsyncSession

from ..models.{mod}_model import {cls}
from ..repositories.{mod}_repository import {cls}Repository
from ..schemas.{mod}_schema import {cls}CreateRequest


class {cls}Service:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = {cls}Repository(session)

    async def create_{mod}(self, req: {cls}CreateRequest) -> {cls}:
        row = {cls}.model_validate(req.model_dump())
        return await self.repository.create(row)

    async def list_{mod}s(self) -> list[{cls}]:
        return await self.repository.list_all()
""",
        encoding="utf-8",
    )


def write_controller(mod: str, cls: str) -> None:
    path = ROOT / "controllers" / f"{mod}_controller.py"
    path.write_text(
        f"""from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.{mod}_schema import {cls}CreateRequest
from ..services.{mod}_service import {cls}Service


class {cls}Controller:
    def __init__(self, session: AsyncSession) -> None:
        self.service = {cls}Service(session)

    async def create_{mod}(self, req: {cls}CreateRequest):
        return await self.service.create_{mod}(req)

    async def list_{mod}s(self):
        return await self.service.list_{mod}s()
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    for mod, cls in NEW:
        write_repo(mod, cls)
        write_service(mod, cls)
        write_controller(mod, cls)
        print(mod)
