from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.core.config.base import Settings


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8", case_sensitive=True)

    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["http://testserver"])
    ENVIRONMENT: str = "test"
    LOG_LEVEL: str = "WARNING"
