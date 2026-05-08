from fastapi import APIRouter

from src.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
    }
