"""List public tables in Neon/Postgres."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
url = (os.getenv("DATABASE_URL") or "").replace("postgresql+psycopg://", "postgresql://")
if not url:
    raise SystemExit("DATABASE_URL not set")

import psycopg

with psycopg.connect(url) as conn:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename"
        )
        for (name,) in cur.fetchall():
            print(name)
