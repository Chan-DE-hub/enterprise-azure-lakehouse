"""Tests for backward-compatible configuration exception imports."""

from enterprise_lakehouse.common.config.exceptions import (
    ConfigurationError as LegacyConfigurationError,
)
from enterprise_lakehouse.common.exceptions import ConfigurationError


def test_config_exception_import_is_backward_compatible() -> None:
    assert LegacyConfigurationError is ConfigurationError
