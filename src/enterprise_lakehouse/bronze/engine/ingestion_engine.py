"""Bronze ingestion orchestration engine."""

from typing import Any

from enterprise_lakehouse.bronze.models import PipelineContext
from enterprise_lakehouse.bronze.readers import BaseReader
from enterprise_lakehouse.common.metadata.repository import MetadataRepository


class IngestionEngine:
    """Coordinate a Bronze ingestion workflow."""

    def __init__(
        self,
        reader: BaseReader,
        repository: MetadataRepository,
    ) -> None:
        """Initialize the engine with its required dependencies."""
        self._reader = reader
        self._repository = repository

    @property
    def reader(self) -> BaseReader:
        """Return the reader used by this engine."""
        return self._reader

    def run(
        self,
        context: PipelineContext,
        source_name: str,
    ) -> Any:
        """Execute a Bronze ingestion run.

        Args:
            context:
                Immutable execution context for the current pipeline run.

            source_name:
                Unique source identifier used to retrieve metadata.

        Returns:
            The source data object returned by the configured reader.
        """
        metadata = self._repository.get(source_name)

        return self._reader.read(
            context=context,
            metadata=metadata,
        )
