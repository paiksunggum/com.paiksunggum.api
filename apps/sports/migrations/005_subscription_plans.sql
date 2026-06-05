-- subscription_plans: 구독 요금제 마스터 (subscriptions.plan_code 참조)

CREATE TABLE IF NOT EXISTS subscription_plans (
    id               BIGSERIAL PRIMARY KEY,
    plan_code        VARCHAR(50) NOT NULL,
    name             VARCHAR(100) NOT NULL,
    description      VARCHAR(500),
    price_cents      BIGINT NOT NULL CHECK (price_cents >= 0),
    currency         VARCHAR(3) NOT NULL DEFAULT 'KRW',
    billing_interval VARCHAR(20) NOT NULL DEFAULT 'monthly',
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_subscription_plans_plan_code UNIQUE (plan_code)
);

CREATE INDEX IF NOT EXISTS ix_subscription_plans_plan_code ON subscription_plans (plan_code);

-- 기존 구독 row가 있어도 테이블 생성은 가능. 신규 row부터 FK 검증.
ALTER TABLE subscriptions
    DROP CONSTRAINT IF EXISTS fk_subscriptions_plan_code;

ALTER TABLE subscriptions
    ADD CONSTRAINT fk_subscriptions_plan_code
    FOREIGN KEY (plan_code) REFERENCES subscription_plans (plan_code)
    ON DELETE RESTRICT
    NOT VALID;
