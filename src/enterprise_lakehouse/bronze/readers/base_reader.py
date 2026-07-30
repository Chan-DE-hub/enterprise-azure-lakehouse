"""Base contract for Bronze source readers."""

from abc import ABC, abstractmethod
from typing import Any


class BaseReader(ABC):
    """Abstract contract implemented by every Bronze source reader.

    A reader is responsible only for retrieving source data and returning it
    to the ingestion engine. It must not contain Bronze write logic, audit
    persistence, quarantine handling, or orchestration behavior.
    """

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Return the unique source type handled by this reader."""

    @abstractmethod
    def read(self, *, options: dict[str, Any]) -> Any:
        """Read data from the source.

        Args:
            options: Source-specific read configuration.

        Returns:
            The source data object consumed by the ingestion engine.

        Raises:
            ValueError: If required options are missing or invalid.
            RuntimeError: If the source cannot be read.
        """
