from src.container.core.db import (
    close_session_manager,
    init_session_manager,
)


async def init_core() -> None:
    await init_session_manager()


async def close_core() -> None:
    await close_session_manager()
