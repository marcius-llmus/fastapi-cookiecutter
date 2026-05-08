import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apps.health.routes import router as health_router
from src.container.lifecycle import close_core, init_core
from src.core.config import settings


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logging.basicConfig(level=settings.LOG_LEVEL)
    await init_core()
    try:
        yield
    finally:
        await close_core()


def create_app() -> FastAPI:
    application = FastAPI(
        title="{{ cookiecutter.project_name }}",
        description="{{ cookiecutter.project_description }}",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health_router, prefix="/api/v1")

    return application


app = create_app()
