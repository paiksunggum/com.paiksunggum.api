"""passengers bookings stub (파일 누락 복구)

Revision ID: 002_passengers_bookings
Revises: 001_titanic_person_booking
Create Date: 2026-06-04

"""

from typing import Sequence, Union

revision: str = "002_passengers_bookings"
down_revision: Union[str, Sequence[str], None] = "001_titanic_person_booking"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
