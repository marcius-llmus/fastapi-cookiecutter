import os
from functools import lru_cache

from src.core.config.base import Settings
from src.core.config.dev import DevelopmentSettings
from src.core.config.prod import ProductionSettings
from src.core.config.test import TestSettings

_DEFAULT_ENVIRONMENT = "development"


def _resolve_environment(environment: str | None = None) -> str:
    raw = environment if environment is not None else os.getenv("ENVIRONMENT")
    if raw is None:
        return _DEFAULT_ENVIRONMENT
    normalized = raw.strip().casefold()
    if not normalized:
        return _DEFAULT_ENVIRONMENT
    if normalized in {"development", "dev"}:
        return "development"
    if normalized in {"production", "prod"}:
        return "production"
    if normalized in {"test", "testing"}:
        return "test"
    raise RuntimeError(f"unsupported ENVIRONMENT: {normalized!r}")


def build_settings(*, environment: str | None = None) -> Settings:
    resolved = _resolve_environment(environment)
    if resolved == "development":
        return DevelopmentSettings()
    if resolved == "production":
        return ProductionSettings()
    if resolved == "test":
        return TestSettings()
    raise RuntimeError(f"unsupported ENVIRONMENT: {resolved!r}")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return build_settings()


settings = get_settings()

__all__ = [
    "Settings",
    "build_settings",
    "get_settings",
    "settings",
]
