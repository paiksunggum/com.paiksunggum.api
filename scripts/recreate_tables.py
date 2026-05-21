"""Run create_tables() against Neon."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from apps.database import create_tables, dispose_engine


async def main() -> None:
    await create_tables()
    await dispose_engine()
    print("create_tables done.")


if __name__ == "__main__":
    asyncio.run(main())
