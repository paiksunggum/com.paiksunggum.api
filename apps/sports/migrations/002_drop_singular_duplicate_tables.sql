-- Remove duplicate singular tables (keep plural canonical names).
-- Run after backup. Child tables referencing singular names are dropped CASCADE.

DROP TABLE IF EXISTS video CASCADE;
DROP TABLE IF EXISTS frame CASCADE;
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS practice CASCADE;
DROP TABLE IF EXISTS ad_link CASCADE;
