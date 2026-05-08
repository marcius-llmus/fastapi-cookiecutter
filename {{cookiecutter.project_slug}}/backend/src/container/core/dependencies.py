from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from src.container.core.db import build_session_manager


async def get_db() -> AsyncIterator[AsyncSession]:
    sessionmanager = build_session_manager()
    async with sessionmanager.session() as session:
        yield session
