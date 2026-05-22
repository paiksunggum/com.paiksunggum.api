-- Forma domain schema (16 tables) — canonical PLURAL table names
-- PK: BIGSERIAL id | timestamps: TIMESTAMPTZ
-- If singular duplicates exist (video, frame, ...): run 002_drop_singular_duplicate_tables.sql first.

-- ---------------------------------------------------------------------------
-- users (shared with Secom; login_id is business login key)
-- ---------------------------------------------------------------------------
ALTER TABLE IF EXISTS users
    RENAME COLUMN user_id TO login_id;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW();

CREATE UNIQUE INDEX IF NOT EXISTS ix_users_login_id ON users (login_id);

-- ---------------------------------------------------------------------------
-- 1. sports
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sports (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(500),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- 3. videos
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS videos (
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    sport_id     BIGINT NOT NULL REFERENCES sports (id) ON DELETE RESTRICT,
    title        VARCHAR(200) NOT NULL,
    video_url    VARCHAR(1000) NOT NULL,
    duration_sec INTEGER,
    visibility   VARCHAR(20) NOT NULL DEFAULT 'public',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_videos_user_id ON videos (user_id);
CREATE INDEX IF NOT EXISTS ix_videos_sport_id ON videos (sport_id);

-- ---------------------------------------------------------------------------
-- 4. analysis_history
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS analysis_history (
    id           BIGSERIAL PRIMARY KEY,
    video_id     BIGINT NOT NULL REFERENCES videos (id) ON DELETE CASCADE,
    status       VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    round_number INTEGER NOT NULL DEFAULT 1,
    started_at   TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_analysis_history_status
        CHECK (status IN ('PENDING', 'SUCCESS', 'FAILED'))
);

CREATE INDEX IF NOT EXISTS ix_analysis_history_video_id ON analysis_history (video_id);

-- ---------------------------------------------------------------------------
-- 5. frames
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS frames (
    id                  BIGSERIAL PRIMARY KEY,
    analysis_history_id BIGINT NOT NULL REFERENCES analysis_history (id) ON DELETE CASCADE,
    video_id            BIGINT NOT NULL REFERENCES videos (id) ON DELETE CASCADE,
    frame_index         INTEGER NOT NULL,
    timestamp_sec       DOUBLE PRECISION NOT NULL,
    keypoints           JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_frames_analysis_history_id ON frames (analysis_history_id);
CREATE INDEX IF NOT EXISTS ix_frames_video_id ON frames (video_id);

-- ---------------------------------------------------------------------------
-- 6. feedbacks
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS feedbacks (
    id          BIGSERIAL PRIMARY KEY,
    video_id    BIGINT NOT NULL REFERENCES videos (id) ON DELETE CASCADE,
    frame_id    BIGINT REFERENCES frames (id) ON DELETE SET NULL,
    source_type VARCHAR(20) NOT NULL DEFAULT 'system',
    comment     VARCHAR(2000) NOT NULL,
    score       DOUBLE PRECISION,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_feedback_score CHECK (score IS NULL OR (score >= 0 AND score <= 100))
);

CREATE INDEX IF NOT EXISTS ix_feedbacks_video_id ON feedbacks (video_id);

-- ---------------------------------------------------------------------------
-- 7. feedback_comments
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS feedback_comments (
    id                BIGSERIAL PRIMARY KEY,
    feedback_id       BIGINT NOT NULL REFERENCES feedbacks (id) ON DELETE CASCADE,
    user_id           BIGINT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    parent_comment_id BIGINT REFERENCES feedback_comments (id) ON DELETE CASCADE,
    body              VARCHAR(2000) NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_feedback_comments_feedback_id ON feedback_comments (feedback_id);

-- ---------------------------------------------------------------------------
-- 8. practices (recommended posture catalog)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS practices (
    id          BIGSERIAL PRIMARY KEY,
    sport_id    BIGINT NOT NULL REFERENCES sports (id) ON DELETE RESTRICT,
    title       VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    guide_json  JSONB,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_practices_sport_id ON practices (sport_id);

-- ---------------------------------------------------------------------------
-- 9. video_practice_match
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS video_practice_match (
    id          BIGSERIAL PRIMARY KEY,
    video_id    BIGINT NOT NULL REFERENCES videos (id) ON DELETE CASCADE,
    practice_id BIGINT NOT NULL REFERENCES practices (id) ON DELETE RESTRICT,
    match_score DOUBLE PRECISION,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_video_practice_match UNIQUE (video_id, practice_id)
);

-- ---------------------------------------------------------------------------
-- 10. user_skills
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_skills (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    practice_id BIGINT NOT NULL REFERENCES practices (id) ON DELETE CASCADE,
    ai_level    SMALLINT NOT NULL DEFAULT 0,
    coach_level SMALLINT NOT NULL DEFAULT 0,
    assessed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_skills_user_practice UNIQUE (user_id, practice_id)
);

-- ---------------------------------------------------------------------------
-- 11. subscriptions (plan per user)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS subscriptions (
    id         BIGSERIAL PRIMARY KEY,
    user_id    BIGINT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    plan_code  VARCHAR(50) NOT NULL,
    status     VARCHAR(20) NOT NULL DEFAULT 'active',
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at   TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_subscriptions_user_id ON subscriptions (user_id);

-- ---------------------------------------------------------------------------
-- 12. payment_logs
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS payment_logs (
    id                BIGSERIAL PRIMARY KEY,
    subscription_id   BIGINT NOT NULL REFERENCES subscriptions (id) ON DELETE RESTRICT,
    user_id           BIGINT NOT NULL REFERENCES users (id) ON DELETE RESTRICT,
    amount_cents      BIGINT NOT NULL,
    currency          VARCHAR(3) NOT NULL DEFAULT 'KRW',
    pg_transaction_id VARCHAR(100) NOT NULL,
    status            VARCHAR(20) NOT NULL DEFAULT 'pending',
    paid_at           TIMESTAMPTZ,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_payment_logs_subscription_id ON payment_logs (subscription_id);

-- ---------------------------------------------------------------------------
-- 13. ads
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ads (
    id         BIGSERIAL PRIMARY KEY,
    title      VARCHAR(200) NOT NULL,
    image_url  VARCHAR(1000),
    target_url VARCHAR(1000) NOT NULL,
    budget     NUMERIC(14, 2) NOT NULL DEFAULT 0,
    status     VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- 14. ad_links (video exposure log)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ad_links (
    id             BIGSERIAL PRIMARY KEY,
    video_id       BIGINT NOT NULL REFERENCES videos (id) ON DELETE CASCADE,
    ad_id          BIGINT NOT NULL REFERENCES ads (id) ON DELETE CASCADE,
    placement_type VARCHAR(30) NOT NULL DEFAULT 'overlay',
    exposed_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_ad_links_video_id ON ad_links (video_id);

-- ---------------------------------------------------------------------------
-- 15. users_ad (user-ad contract)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users_ad (
    id                BIGSERIAL PRIMARY KEY,
    user_id           BIGINT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    ad_id             BIGINT NOT NULL REFERENCES ads (id) ON DELETE CASCADE,
    contract_status   VARCHAR(20) NOT NULL DEFAULT 'active',
    allocated_budget  NUMERIC(14, 2) NOT NULL DEFAULT 0,
    started_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at          TIMESTAMPTZ,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_users_ad_user_ad UNIQUE (user_id, ad_id)
);

-- ---------------------------------------------------------------------------
-- 16. ad_stats_daily
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ad_stats_daily (
    id          BIGSERIAL PRIMARY KEY,
    ad_id       BIGINT NOT NULL REFERENCES ads (id) ON DELETE CASCADE,
    stat_date   DATE NOT NULL,
    impressions BIGINT NOT NULL DEFAULT 0,
    clicks      BIGINT NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_ad_stats_daily_ad_date UNIQUE (ad_id, stat_date)
);
