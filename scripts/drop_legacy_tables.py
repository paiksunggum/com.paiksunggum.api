"""Drop passengers, legacy forma user, and forma rows that still FK to user."""
import os
url = (os.getenv("DATABASE_URL") or "").replace("postgresql+psycopg://", "postgresql://")
if not url:
    raise SystemExit("DATABASE_URL not set")

import psycopg

LEGACY = ("passengers", "user")

with psycopg.connect(url) as conn:
    with conn.cursor() as cur:
        for name in LEGACY:
            cur.execute(f'DROP TABLE IF EXISTS "{name}" CASCADE')
            print(f"dropped: {name}")
    conn.commit()
print("Done.")
