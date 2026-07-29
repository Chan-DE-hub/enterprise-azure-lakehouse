"""Configuration-related exceptions."""

from enterprise_lakehouse.common.exceptions.base import EnterpriseLakehouseError


class ConfigurationError(EnterpriseLakehouseError):
    """Base configuration exception."""


class ConfigurationFileNotFoundError(ConfigurationError):
    """Configuration file was not found."""


class ConfigurationParseError(ConfigurationError):
    """Configuration parsing failed."""


class ConfigurationValidationError(ConfigurationError):
    """Configuration validation failed."""
