"""Drop all tables in public schema (CASCADE)."""
import os
url = (os.getenv("DATABASE_URL") or "").replace("postgresql+psycopg://", "postgresql://")
if not url:
    raise SystemExit("DATABASE_URL not set")

import psycopg

with psycopg.connect(url) as conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename
            """
        )
        tables = [row[0] for row in cur.fetchall()]
        if not tables:
            print("No tables in public schema.")
        else:
            for name in tables:
                cur.execute(f'DROP TABLE IF EXISTS "{name}" CASCADE')
                print(f"dropped: {name}")
    conn.commit()
print(f"Done. Dropped {len(tables)} table(s).")
