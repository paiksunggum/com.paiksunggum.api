from __future__ import annotations

from abc import ABC, abstractmethod


class SLMPort(ABC):
    @abstractmethod
    async def ask(self, prompt: str) -> str:
        pass
