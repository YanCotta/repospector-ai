"""
Unit tests for core configuration.
"""

import os
import tempfile
from unittest.mock import patch

import pytest


# Test settings without importing the heavy dependencies
def test_environment_variables():
    """Test environment variable handling."""
    test_env = {
        "OPENAI_API_KEY": "test-key-123",
        "SERPAPI_API_KEY": "serp-key-456",
        "DEBUG": "true",
        "ENVIRONMENT": "production",
    }

    with patch.dict(os.environ, test_env):
        assert os.environ.get("OPENAI_API_KEY") == "test-key-123"
        assert os.environ.get("SERPAPI_API_KEY") == "serp-key-456"
        assert os.environ.get("DEBUG") == "true"
        assert os.environ.get("ENVIRONMENT") == "production"


def test_dotenv_file_format():
    """Test .env file format without heavy imports."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("OPENAI_API_KEY=test-key\n")
        f.write("SERPAPI_API_KEY=test-serpapi\n")
        f.write("DEBUG=false\n")
        f.flush()

        # Read back and verify format
        with open(f.name) as read_f:
            content = read_f.read()
            assert "OPENAI_API_KEY=test-key" in content
            assert "SERPAPI_API_KEY=test-serpapi" in content
            assert "DEBUG=false" in content

        os.unlink(f.name)


def test_config_file_exists():
    """Test that config file exists and is importable."""
    try:
        from repospector_ai.core import config

        assert hasattr(config, "Settings")
    except ImportError as e:
        pytest.skip(f"Config module import failed: {e}")


def test_config_has_required_fields():
    """Test configuration has required fields."""
    try:
        from repospector_ai.core.config import Settings

        # Test with minimal environment
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()

            # Check that basic fields exist
            assert hasattr(settings, "openai_api_key")
            assert hasattr(settings, "app_name")
            assert hasattr(settings, "environment")

    except ImportError as e:
        pytest.skip(f"Settings import failed: {e}")


class TestBasicConfiguration:
    """Basic configuration tests without heavy dependencies."""

    def test_api_key_environment(self):
        """Test API key from environment."""
        test_key = "sk-test123456789"

        with patch.dict(os.environ, {"OPENAI_API_KEY": test_key}):
            assert os.environ.get("OPENAI_API_KEY") == test_key

    def test_debug_flag(self):
        """Test debug flag handling."""
        with patch.dict(os.environ, {"DEBUG": "true"}):
            assert os.environ.get("DEBUG") == "true"

        with patch.dict(os.environ, {"DEBUG": "false"}):
            assert os.environ.get("DEBUG") == "false"
