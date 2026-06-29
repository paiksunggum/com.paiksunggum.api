from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EmailSendCommand:
    to: str
    prompt: str


@dataclass
class EmailSendResult:
    to: str
    subject: str
    success: bool
