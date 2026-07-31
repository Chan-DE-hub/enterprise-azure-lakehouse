"""Base contract for Bronze source readers."""

from abc import ABC, abstractmethod
from typing import Any

from enterprise_lakehouse.bronze.models import (
    PipelineContext,
    SourceMetadata,
)


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
    def read(
        self,
        *,
        context: PipelineContext,
        metadata: SourceMetadata,
    ) -> Any:
        """Read data from the source.

        Args:
            context:
                Execution context for the current pipeline run.

            metadata:
                Immutable metadata describing the configured source.

        Returns:
            The source data object consumed by the ingestion engine.

        Raises:
            ValueError:
                If the metadata is invalid.

            RuntimeError:
                If the source cannot be read.
        """
