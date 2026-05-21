"""Drop Forma domain tables so create_tables can rebuild FKs to users."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
url = (os.getenv("DATABASE_URL") or "").replace("postgresql+psycopg://", "postgresql://")
if not url:
    raise SystemExit("DATABASE_URL not set")

import psycopg

FORMA = (
    "ad_links",
    "feedbacks",
    "frames",
    "practices",
    "videos",
    "subscriptions",
    "ads",
    "sports",
)

with psycopg.connect(url) as conn:
    with conn.cursor() as cur:
        for name in FORMA:
            cur.execute(f'DROP TABLE IF EXISTS "{name}" CASCADE')
            print(f"dropped: {name}")
    conn.commit()
print("Done.")
