from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    CORS_ORIGINS: list[str] = Field(default_factory=list)
    ENVIRONMENT: str
    LOG_LEVEL: str = "INFO"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.casefold() == "production"
