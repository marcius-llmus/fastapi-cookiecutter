import contextlib
import logging
from collections.abc import AsyncIterator
from contextlib import AbstractAsyncContextManager
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None) -> None:
        self._engine: AsyncEngine | None = create_async_engine(host, **(engine_kwargs or {}))
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = async_sessionmaker(
            self._engine,
            autocommit=False,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        if self._engine is None:
            raise RuntimeError("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    async def cleanup(self) -> None:
        if self._engine is not None:
            logger.warning("Closing database connection pool.")
            await self.close()

    def session(self) -> AbstractAsyncContextManager[AsyncSession]:
        # (pycharm only, mypy safe)
        # noinspection PyArgumentList
        return self._session()

    @contextlib.asynccontextmanager
    async def _session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise RuntimeError("DatabaseSessionManager is not initialized")
        async with self._sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
