"""Unit tests for config loader."""
import pytest
import sys
from pathlib import Path
import tempfile
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agent.config_loader import load_config, validate_config, DEFAULT_CONFIG


def test_load_default_config():
    """Test loading default configuration."""
    config = load_config(config_path="nonexistent.yml")

    assert config == DEFAULT_CONFIG
    assert config["interval"] == 5
    assert config["server_url"] == "http://localhost:8000"


def test_load_config_from_file():
    """Test loading configuration from file."""
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write("""
interval: 10
server_url: http://example.com:9000
log_level: DEBUG
""")
        temp_config = f.name

    try:
        config = load_config(temp_config)

        assert config["interval"] == 10
        assert config["server_url"] == "http://example.com:9000"
        assert config["log_level"] == "DEBUG"
        # Other values should be from defaults
        assert config["retry_attempts"] == DEFAULT_CONFIG["retry_attempts"]
    finally:
        os.unlink(temp_config)


def test_validate_config_valid():
    """Test validation with valid configuration."""
    config = DEFAULT_CONFIG.copy()
    assert validate_config(config) is True


def test_validate_config_invalid_interval():
    """Test validation with invalid interval."""
    config = DEFAULT_CONFIG.copy()
    config["interval"] = 0

    with pytest.raises(ValueError, match="interval must be greater than 0"):
        validate_config(config)


def test_validate_config_negative_retry():
    """Test validation with negative retry attempts."""
    config = DEFAULT_CONFIG.copy()
    config["retry_attempts"] = -1

    with pytest.raises(ValueError, match="retry_attempts must be non-negative"):
        validate_config(config)


def test_validate_config_invalid_buffer_size():
    """Test validation with invalid buffer size."""
    config = DEFAULT_CONFIG.copy()
    config["buffer_size"] = 0

    with pytest.raises(ValueError, match="buffer_size must be greater than 0"):
        validate_config(config)


def test_validate_config_invalid_timeout():
    """Test validation with invalid timeout."""
    config = DEFAULT_CONFIG.copy()
    config["timeout"] = -5

    with pytest.raises(ValueError, match="timeout must be greater than 0"):
        validate_config(config)
