"""apply_3nf_fixes

Revision ID: apply_3nf_fixes
Revises:
Create Date: 2026-05-26

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "apply_3nf_fixes"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        DROP TABLE IF EXISTS feedback_frame_links CASCADE;
        DROP TABLE IF EXISTS feedback_video_links CASCADE;
        """
    )

    op.execute(
        """
        UPDATE feedbacks
        SET video_id = NULL
        WHERE frame_id IS NOT NULL AND video_id IS NOT NULL;
        """
    )

    op.alter_column(
        "feedbacks",
        "video_id",
        existing_type=sa.BigInteger(),
        nullable=True,
    )

    op.execute(
        """
        ALTER TABLE feedbacks
        DROP CONSTRAINT IF EXISTS ck_feedbacks_video_xor_frame;
        """
    )
    op.execute(
        """
        ALTER TABLE feedbacks
        ADD CONSTRAINT ck_feedbacks_video_xor_frame
        CHECK ((video_id IS NULL) <> (frame_id IS NULL));
        """
    )

    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN birthdate TYPE DATE
        USING (
            CASE
                WHEN birthdate ~ '^[0-9]{8}$' THEN TO_DATE(birthdate, 'YYYYMMDD')
                WHEN birthdate ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN birthdate::DATE
                ELSE DATE '1970-01-01'
            END
        );
        """
    )

    op.execute(
        """
        ALTER TABLE ad_stats_daily
        DROP CONSTRAINT IF EXISTS uq_ad_stats_daily_ad_date;
        """
    )
    op.execute(
        """
        ALTER TABLE ad_stats_daily
        ADD CONSTRAINT uq_ad_stats_daily_ad_date UNIQUE (ad_id, stat_date);
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE ad_stats_daily
        DROP CONSTRAINT IF EXISTS uq_ad_stats_daily_ad_date;
        """
    )

    op.execute(
        """
        ALTER TABLE users
        ALTER COLUMN birthdate TYPE VARCHAR(8)
        USING TO_CHAR(birthdate, 'YYYYMMDD');
        """
    )

    op.execute(
        """
        ALTER TABLE feedbacks
        DROP CONSTRAINT IF EXISTS ck_feedbacks_video_xor_frame;
        """
    )

    op.execute(
        """
        UPDATE feedbacks
        SET video_id = f.video_id
        FROM frames f
        WHERE feedbacks.frame_id = f.id AND feedbacks.video_id IS NULL;
        """
    )

    op.alter_column(
        "feedbacks",
        "video_id",
        existing_type=sa.BigInteger(),
        nullable=False,
    )
