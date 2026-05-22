import io
import logging
import os
import secrets
from decimal import Decimal
from pathlib import Path

import httpx
import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.secom.app.models.user import User
from apps.secom.app.security import hash_password

from ..models.ad_link_model import AdLink
from ..models.ads_model import Ad
from ..models.sports_model import Sport
from ..models.users_ad_model import UsersAd
from ..models.video_model import Video
from ..schemas.seed_schema import SeedDemoCsvResponse

logger = logging.getLogger("apps.forma.seed")

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_LOCAL_SAMPLE = _DATA_DIR / "country-list-sample.csv"
_DEFAULT_REMOTE_CSV = (
    "https://raw.githubusercontent.com/datasets/country-list/master/data.csv"
)
_DEMO_LOGIN_ID = "forma_csv_demo"


def _resolve_csv_url() -> str:
    return (os.getenv("FORMA_DEMO_CSV_URL") or "").strip() or _DEFAULT_REMOTE_CSV


def _name_code_columns(df: pd.DataFrame) -> tuple[str, str]:
    by_lower = {str(c).strip().lower(): str(c).strip() for c in df.columns}
    try:
        return by_lower["name"], by_lower["code"]
    except KeyError as e:
        raise ValueError(
            "CSV에 Name, Code 컬럼이 필요합니다 (datasets/country-list 형식)."
        ) from e


class FormaSeedService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def seed_demo_from_country_csv(
        self,
        limit: int = 15,
    ) -> SeedDemoCsvResponse:
        url = _resolve_csv_url()
        existing = await self.session.execute(
            select(User).where(User.login_id == _DEMO_LOGIN_ID)
        )
        if existing.scalar_one_or_none() is not None:
            return SeedDemoCsvResponse(
                status="already_seeded",
                source="n/a",
                csv_url=url,
                rows_used=0,
                message="forma_csv_demo 사용자가 이미 있습니다. 중복 시드를 생략했습니다.",
            )

        lim = max(1, min(limit, 250))
        source_label = "remote_csv"
        content: bytes | None = None
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                r = await client.get(url, follow_redirects=True)
                r.raise_for_status()
                content = r.content
        except Exception as e:
            logger.warning("원격 CSV 로드 실패, 로컬 표본 사용: %s", e)
            if not _LOCAL_SAMPLE.is_file():
                raise ValueError(
                    "원격 CSV를 받지 못했고 로컬 표본 파일도 없습니다."
                ) from e
            content = _LOCAL_SAMPLE.read_bytes()
            source_label = "local_fallback"

        df = pd.read_csv(io.BytesIO(content))
        name_col, code_col = _name_code_columns(df)
        df = df[[name_col, code_col]].dropna().head(lim)
        if df.empty:
            raise ValueError("CSV에서 유효한 Name/Code 행을 찾지 못했습니다.")

        pairs: list[tuple[str, str]] = []
        for _, row in df.iterrows():
            name = str(row[name_col]).strip()
            code = str(row[code_col]).strip().upper()
            if name and code:
                pairs.append((name, code))
        if not pairs:
            raise ValueError("적재할 데모 행이 없습니다.")

        user = User(
            login_id=_DEMO_LOGIN_ID,
            password_hash=hash_password(secrets.token_urlsafe(32)),
            email="forma_csv_demo@example.invalid",
            name="CSV Demo User",
            birthdate="00000000",
            gender="none",
            role="user",
        )
        sport = Sport(
            name="Demo Sport (CSV)",
            description="datasets/country-list 기반 데모 시드",
            is_active=True,
        )
        self.session.add(user)
        self.session.add(sport)
        await self.session.flush()

        assert user.id is not None
        assert sport.id is not None

        videos: list[Video] = []
        ads: list[Ad] = []
        for name, code in pairs:
            videos.append(
                Video(
                    user_id=user.id,
                    sports_id=sport.id,
                    title=f"Demo clip: {name}",
                    storage_url=f"https://example.net/forma-demo/video/{code.lower()}",
                    duration_sec=120,
                    visibility="public",
                )
            )
            ads.append(
                Ad(
                    title=f"Demo ad: {name}",
                    target_url=f"https://example.net/forma-demo/product/{code.lower()}",
                    image_url=None,
                    budget=Decimal("1000"),
                    status="active",
                )
            )

        for v, a in zip(videos, ads):
            self.session.add(v)
            self.session.add(a)
        await self.session.flush()

        ad_links: list[AdLink] = []
        users_ads: list[UsersAd] = []
        for v, a in zip(videos, ads):
            assert v.id is not None and a.id is not None
            users_ads.append(
                UsersAd(
                    user_id=user.id,
                    ad_id=a.id,
                    contract_status="active",
                    allocated_budget=Decimal("500"),
                )
            )
            ad_links.append(
                AdLink(
                    video_id=v.id,
                    ad_id=a.id,
                    placement_type="description",
                )
            )
        for ua in users_ads:
            self.session.add(ua)
        for link in ad_links:
            self.session.add(link)

        await self.session.commit()

        n_pairs = len(ad_links)
        return SeedDemoCsvResponse(
            status="ok",
            source=source_label,
            csv_url=url,
            rows_used=n_pairs,
            users_created=1,
            sports_created=1,
            videos_created=n_pairs,
            ads_created=n_pairs,
            ad_links_created=n_pairs,
            message=f"시드 완료 (원본: {url})",
        )
