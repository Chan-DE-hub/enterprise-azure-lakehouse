"""Ingestion-related exceptions."""

from enterprise_lakehouse.common.exceptions.base import EnterpriseLakehouseError


class IngestionError(EnterpriseLakehouseError):
    """Generic ingestion failure."""


class RetryableIngestionError(IngestionError):
    """Failure that may be retried safely."""


class NonRetryableIngestionError(IngestionError):
    """Failure that should fail immediately."""
