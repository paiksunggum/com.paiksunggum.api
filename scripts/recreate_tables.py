"""Run create_all_tables() against Neon."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.matrix.oracle_database import create_all_tables, dispose_engine, init_engine


async def main() -> None:
    init_engine()
    await create_all_tables()
    await dispose_engine()
    print("create_all_tables done.")


if __name__ == "__main__":
    asyncio.run(main())
