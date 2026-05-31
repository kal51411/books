"""Runtime configuration."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    env: str = Field(default="local", alias="NYAYAGPT_ENV")
    database_url: str = "postgresql+asyncpg://nyayagpt:nyayagpt@localhost:5432/nyayagpt"
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: str = "http://localhost:6333"
    jwt_secret: str = "dev-only-change-me"
    jwt_algorithm: str = "HS256"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    gemini_api_key: str | None = None
    local_llama_base_url: str = "http://localhost:11434"
    default_llm_provider: str = "openai"
    default_model: str = "gpt-4.1"
    max_context_chunks: int = 12
    min_citation_confidence: float = 0.72


@lru_cache
def get_settings() -> Settings:
    return Settings()
