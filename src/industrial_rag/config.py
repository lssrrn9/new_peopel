"""Configuración central del pipeline RAG industrial."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "industrial_manuals"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    # Dimensión de BAAI/bge-small-en-v1.5
    embedding_dim: int = 384

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    equipment_registry_path: Path = Path("data/equipment_registry.json")
    sample_chunks_path: Path = Path("data/sample_chunks")

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"

    search_limit: int = 3
    use_memory_qdrant: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
