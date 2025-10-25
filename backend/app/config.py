"""Application configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str = "change-me-in-production"

    # Database
    DATABASE_URL: str = "sqlite:///./mcpcc.db"

    # MCP Integration
    MCP_BASE_URL: str = "http://localhost:8001"
    MCP_TOKEN: str = ""

    # GitHub Integration
    GITHUB_TOKEN: str = ""
    GITHUB_SYNC_ENABLED: bool = False

    # Redis for job queue
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
