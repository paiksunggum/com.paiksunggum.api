from __future__ import annotations

from pydantic import BaseModel


class OrchestrateSchema(BaseModel):
    message: str


class OrchestrateResponseSchema(BaseModel):
    tool: str
    message: str
