from pydantic import Field
from pydantic_settings import SettingsConfigDict

from src.core.config.base import Settings


class DevelopmentSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    {%- if cookiecutter.database == "postgres" %}
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/{{ cookiecutter.project_slug }}"
    {%- else %}
    DATABASE_URL: str = "sqlite+aiosqlite:///./{{ cookiecutter.project_slug }}.db"
    {%- endif %}
    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["http://localhost:3000", "http://localhost:5173"])
    ENVIRONMENT: str = "development"
