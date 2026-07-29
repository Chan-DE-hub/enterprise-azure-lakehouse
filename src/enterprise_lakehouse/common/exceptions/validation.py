"""Validation-related exceptions."""

from enterprise_lakehouse.common.exceptions.base import EnterpriseLakehouseError


class ValidationError(EnterpriseLakehouseError):
    """Validation framework error."""
