"""
Application configuration using Pydantic BaseSettings.

Loads settings from environment variables and .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal


class Settings(BaseSettings):
    """Central configuration for the Email Campaign Generator."""

    # ── LLM Configuration ──────────────────────────────────────────
    openai_api_key: str = Field(default="", description="OpenAI API key")
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    google_api_key: str = Field(default="", description="Google Gemini API key")
    llm_provider: Literal["openai", "anthropic", "google", "gemini"] = Field(
        default="google",
        description="Which LLM provider to use",
    )
    llm_model: str = Field(
        default="gemini-1.5-flash",
        description="Model name for the selected provider",
    )
    llm_temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature for generation",
    )
    llm_max_tokens: int = Field(
        default=2048,
        ge=1,
        description="Maximum tokens in LLM response",
    )

    # ── MLflow ─────────────────────────────────────────────────────
    mlflow_tracking_uri: str = Field(
        default="",
        description="MLflow tracking server URI",
    )
    mlflow_experiment_name: str = Field(
        default="email_campaign_optimization",
        description="MLflow experiment name",
    )

    # ── FastAPI ────────────────────────────────────────────────────
    app_host: str = Field(default="0.0.0.0", description="API host")
    app_port: int = Field(default=8000, ge=1, le=65535, description="API port")
    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Application environment",
    )

    # ── A/B Testing ────────────────────────────────────────────────
    ab_test_confidence_threshold: float = Field(
        default=0.95,
        ge=0.5,
        le=1.0,
        description="Bayesian confidence threshold to declare a winner",
    )
    ab_test_max_iterations: int = Field(
        default=5,
        ge=1,
        description="Maximum optimization iterations per campaign",
    )
    ab_test_simulated_recipients: int = Field(
        default=1000,
        ge=100,
        description="Number of simulated recipients per variant",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }


# Singleton settings instance
settings = Settings()
