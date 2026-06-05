-- apply_3nf_fixes: feedbacks XOR, users.birthdate DATE, ad_stats_daily UK
-- Alembic revision: apply_3nf_fixes

DROP TABLE IF EXISTS feedback_frame_links CASCADE;
DROP TABLE IF EXISTS feedback_video_links CASCADE;

UPDATE feedbacks
SET video_id = NULL
WHERE frame_id IS NOT NULL AND video_id IS NOT NULL;

ALTER TABLE feedbacks
    ALTER COLUMN video_id DROP NOT NULL;

ALTER TABLE feedbacks
    DROP CONSTRAINT IF EXISTS ck_feedbacks_video_xor_frame;

ALTER TABLE feedbacks
    ADD CONSTRAINT ck_feedbacks_video_xor_frame
    CHECK ((video_id IS NULL) <> (frame_id IS NULL));

ALTER TABLE users
    ALTER COLUMN birthdate TYPE DATE
    USING (
        CASE
            WHEN birthdate::TEXT ~ '^[0-9]{8}$' THEN TO_DATE(birthdate::TEXT, 'YYYYMMDD')
            WHEN birthdate::TEXT ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN birthdate::TEXT::DATE
            ELSE DATE '1970-01-01'
        END
    );

ALTER TABLE ad_stats_daily
    DROP CONSTRAINT IF EXISTS uq_ad_stats_daily_ad_date;

ALTER TABLE ad_stats_daily
    ADD CONSTRAINT uq_ad_stats_daily_ad_date UNIQUE (ad_id, stat_date);
