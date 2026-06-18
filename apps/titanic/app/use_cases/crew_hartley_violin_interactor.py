from __future__ import annotations
import io
import logging

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from apps.titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from apps.titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from apps.titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from apps.titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort

logger = logging.getLogger("apps")


class HartleyViolinInteractor(HartleyViolinUseCase):

    def __init__(self, repository: HartleyViolinPort):
        self.repository = repository

    def get_correlation_plot(self, df: pd.DataFrame) -> bytes:
        '''피처 상관관계 히트맵을 PNG 바이트로 반환'''
        numeric_df = df.select_dtypes(include="number")
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        return buf.read()

    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        '''왈리스 하틀리의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(HartleyViolinQuery(
            id=schema.id,
            name=schema.name
        ))
