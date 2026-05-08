from src.core.config import settings
from src.core.db import DatabaseSessionManager

_sessionmanager: DatabaseSessionManager | None = None


async def init_session_manager() -> None:
    global _sessionmanager
    if _sessionmanager is not None:
        raise RuntimeError("sessionmanager already initialized")
    _sessionmanager = DatabaseSessionManager(
        settings.DATABASE_URL,
        {"echo": settings.DATABASE_ECHO},
    )


def build_session_manager() -> DatabaseSessionManager:
    if _sessionmanager is None:
        raise RuntimeError("sessionmanager not initialized; lifespan must run first")
    return _sessionmanager


async def close_session_manager() -> None:
    global _sessionmanager
    if _sessionmanager is None:
        raise RuntimeError("sessionmanager not initialized")
    await _sessionmanager.cleanup()
    _sessionmanager = None
