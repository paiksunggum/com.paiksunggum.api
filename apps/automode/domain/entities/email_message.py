from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EmailMessage:
    to: str
    subject: str
    body: str
