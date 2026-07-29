"""Audit-related exceptions."""

from enterprise_lakehouse.common.exceptions.base import EnterpriseLakehouseError


class AuditError(EnterpriseLakehouseError):
    """Audit framework error."""
