"""add_automode_contacts

Revision ID: 7bf5881339f5
Revises: 002_passengers_bookings
Create Date: 2026-06-30 15:51:13.376731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7bf5881339f5'
down_revision: Union[str, Sequence[str], None] = '002_passengers_bookings'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'automode_contacts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('middle_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('nickname', sa.String(), nullable=True),
        sa.Column('organization_name', sa.String(), nullable=True),
        sa.Column('organization_title', sa.String(), nullable=True),
        sa.Column('birthday', sa.String(), nullable=True),
        sa.Column('labels', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('automode_contacts')
