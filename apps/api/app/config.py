from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GraphBoard API"
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://graphboard:graphboard@localhost:5432/graphboard"
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="GRAPHBOARD_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
