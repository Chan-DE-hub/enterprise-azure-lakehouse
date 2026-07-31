"""Contracts for loading file-based data."""

from collections.abc import Mapping
from typing import Any, Protocol


class FileLoader(Protocol):
    """Contract implemented by file-loading adapters."""

    def __call__(
        self,
        *,
        path: str,
        file_format: str,
        options: Mapping[str, Any],
    ) -> Any:
        """Load data from a file source."""
        ...
