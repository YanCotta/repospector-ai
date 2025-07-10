"""
Configuration management for RepoSpector AI.

This module provides centralized configuration management using Pydantic Settings
for loading environment variables and default values.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API Keys
    openai_api_key: str | None = Field(
        default=None,
        description="OpenAI API key for LLM access",
        min_length=1,
    )

    serpapi_api_key: str | None = Field(
        default=None,
        description="SerpAPI key for web search functionality",
    )

    # LLM Configuration
    llm_model: str = Field(
        default="gpt-4",
        description="OpenAI model to use for the agents",
    )

    llm_temperature: float = Field(
        default=0.1,
        ge=0.0,
        le=2.0,
        description="Temperature setting for LLM responses",
    )

    # Application Configuration
    app_name: str = Field(
        default="RepoSpector AI",
        description="Application name",
    )

    app_version: str = Field(
        default="0.1.0",
        description="Application version",
    )

    environment: str = Field(
        default="production",
        description="Application environment (development, staging, production)",
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    log_format: str = Field(
        default="json",
        description="Log format: 'json' or 'text'",
    )

    # Repository Analysis Settings
    max_file_size_kb: int = Field(
        default=1024,
        gt=0,
        description="Maximum file size to analyze in KB",
    )

    temp_dir_prefix: str = Field(
        default="repospector_",
        description="Prefix for temporary directories",
    )

    # CrewAI Configuration
    crew_verbose: bool = Field(
        default=True,
        description="Enable verbose output for CrewAI",
    )


# Global settings instance
settings = Settings()
