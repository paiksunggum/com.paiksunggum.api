from __future__ import annotations

from dataclasses import dataclass

from apps.star_craft.domain.ontology.spam.spam_category import SpamCategory


@dataclass
class EmailSendCommand:
    to: str
    prompt: str


@dataclass
class EmailSendResult:
    to: str
    subject: str
    success: bool


@dataclass
class EmailClassifyCommand:
    subject: str
    body: str


@dataclass
class EmailClassifyResult:
    category: SpamCategory
    matched_keywords: list[str]
    is_spam: bool


@dataclass(frozen=True)
class EmailIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class EmailIntroduceResult:
    id: int
    name: str
