"""Configuration loading and validation utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from enterprise_lakehouse.common.config.models import ApplicationSettings
from enterprise_lakehouse.common.exceptions.configuration import (
    ConfigurationFileNotFoundError,
    ConfigurationParseError,
    ConfigurationValidationError,
)


def load_settings(config_path: str | Path) -> ApplicationSettings:
    """Load and validate application settings from a YAML file."""
    path = Path(config_path)

    if not path.is_file():
        raise ConfigurationFileNotFoundError(f"Configuration file does not exist: {path}")

    try:
        raw_config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigurationParseError(f"Failed to parse configuration file: {path}") from exc

    if raw_config is None:
        raise ConfigurationParseError(f"Configuration file is empty: {path}")

    if not isinstance(raw_config, dict):
        raise ConfigurationParseError(f"Configuration root must be a mapping: {path}")

    try:
        return ApplicationSettings.model_validate(_normalize_config(raw_config))
    except ValidationError as exc:
        raise ConfigurationValidationError(f"Configuration validation failed for: {path}") from exc


def _normalize_config(raw_config: dict[str, Any]) -> dict[str, Any]:
    """Return a defensive copy before validation."""
    return dict(raw_config)
