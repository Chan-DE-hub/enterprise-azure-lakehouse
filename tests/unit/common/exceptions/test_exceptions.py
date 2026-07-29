"""Tests for the shared exception hierarchy."""

from enterprise_lakehouse.common.exceptions import (
    AuditError,
    ConfigurationError,
    ConfigurationFileNotFoundError,
    EnterpriseLakehouseError,
    IngestionError,
    MetadataError,
    NonRetryableIngestionError,
    RetryableIngestionError,
    RetryLimitExceededError,
    StorageError,
    ValidationError,
    WatermarkError,
)


def test_platform_exceptions_inherit_from_base_exception() -> None:
    exception_types = (
        ConfigurationError,
        MetadataError,
        StorageError,
        ValidationError,
        WatermarkError,
        AuditError,
        IngestionError,
        RetryLimitExceededError,
    )

    for exception_type in exception_types:
        assert issubclass(exception_type, EnterpriseLakehouseError)


def test_configuration_file_not_found_inherits_from_configuration_error() -> None:
    assert issubclass(
        ConfigurationFileNotFoundError,
        ConfigurationError,
    )


def test_ingestion_exception_categories_inherit_from_ingestion_error() -> None:
    assert issubclass(RetryableIngestionError, IngestionError)
    assert issubclass(NonRetryableIngestionError, IngestionError)
