from pydantic_settings import SettingsConfigDict

from src.core.config.base import Settings


class ProductionSettings(Settings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8", case_sensitive=True)

    ENVIRONMENT: str = "production"
