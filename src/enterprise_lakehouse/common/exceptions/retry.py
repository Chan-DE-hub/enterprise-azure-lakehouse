"""Retry-related exceptions."""

from enterprise_lakehouse.common.exceptions.base import EnterpriseLakehouseError


class RetryLimitExceededError(EnterpriseLakehouseError):
    """Maximum retry attempts exceeded."""
