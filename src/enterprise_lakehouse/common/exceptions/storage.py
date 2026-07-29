"""Storage-related exceptions."""

from enterprise_lakehouse.common.exceptions.base import EnterpriseLakehouseError


class StorageError(EnterpriseLakehouseError):
    """Storage framework error."""
