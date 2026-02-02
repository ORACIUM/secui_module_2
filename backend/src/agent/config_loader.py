"""Configuration loader for the agent."""
import yaml
import os
from pathlib import Path
from typing import Dict, Any


DEFAULT_CONFIG = {
    "interval": 5,
    "server_url": "http://localhost:8000",
    "retry_attempts": 3,
    "retry_delay": 5,
    "buffer_size": 1000,
    "use_protobuf": True,
    "timeout": 10,
    "log_level": "INFO",
    "log_file": "agent.log",
    "collectors": {
        "cpu": True,
        "memory": True,
        "disk": True,
        "network": True,
    },
    "top_processes_limit": 5,
}


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing configuration values
    """
    config = DEFAULT_CONFIG.copy()

    if config_path is None:
        # Try to find config file in default locations
        possible_paths = [
            Path(__file__).parent.parent.parent / "config" / "agent.yml",
            Path("config/agent.yml"),
            Path("backend/config/agent.yml"),
        ]

        for path in possible_paths:
            if path.exists():
                config_path = str(path)
                break

    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    config.update(user_config)
        except Exception as e:
            print(f"Warning: Failed to load config from {config_path}: {e}")
            print("Using default configuration")

    return config


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration values.

    Args:
        config: Configuration dictionary

    Returns:
        True if valid, raises ValueError otherwise
    """
    if config["interval"] <= 0:
        raise ValueError("interval must be greater than 0")

    if config["retry_attempts"] < 0:
        raise ValueError("retry_attempts must be non-negative")

    if config["buffer_size"] <= 0:
        raise ValueError("buffer_size must be greater than 0")

    if config["timeout"] <= 0:
        raise ValueError("timeout must be greater than 0")

    if config["top_processes_limit"] <= 0:
        raise ValueError("top_processes_limit must be greater than 0")

    return True
