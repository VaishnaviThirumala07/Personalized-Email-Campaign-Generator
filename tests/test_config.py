"""
Test: Application configuration loads correctly.
"""

import pytest


def test_settings_defaults():
    """Verify default settings load without errors."""
    from app.core.config import Settings

    # Create settings with explicit values
    s = Settings(
        openai_api_key="test-key",
        llm_provider="openai",
        llm_model="gpt-4o-mini",
        _env_file=None,  # Don't load .env in tests
    )

    assert s.llm_provider == "openai"
    assert s.llm_model == "gpt-4o-mini"
    assert s.llm_temperature == 0.7
    assert s.llm_max_tokens == 2048
    assert s.app_port == 8000
    assert s.app_env == "development"
    assert s.ab_test_confidence_threshold == 0.95
    assert s.ab_test_max_iterations == 5
    assert s.ab_test_simulated_recipients == 1000


def test_settings_validation():
    """Verify settings reject invalid values."""
    from app.core.config import Settings

    with pytest.raises(Exception):
        Settings(
            openai_api_key="test",
            llm_temperature=5.0,  # Max is 2.0
            _env_file=None,
        )


def test_settings_anthropic_provider():
    """Verify Anthropic provider configuration."""
    from app.core.config import Settings

    s = Settings(
        anthropic_api_key="test-key",
        llm_provider="anthropic",
        llm_model="claude-3-5-sonnet-20241022",
        _env_file=None,
    )

    assert s.llm_provider == "anthropic"
def test_settings_google_provider():
    """Verify Google Gemini provider configuration."""
    from app.core.config import Settings

    s = Settings(
        google_api_key="test-key",
        llm_provider="google",
        llm_model="gemini-1.5-flash",
        _env_file=None,
    )

    assert s.llm_provider == "google"
    assert s.llm_model == "gemini-1.5-flash"
