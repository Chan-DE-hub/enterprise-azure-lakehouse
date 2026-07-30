"""Bronze ingestion orchestration engine."""

from enterprise_lakehouse.bronze.models import PipelineContext
from enterprise_lakehouse.bronze.readers import BaseReader
from enterprise_lakehouse.bronze.repositories import MetadataRepository


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
    ) -> None:
        """Execute a Bronze ingestion run.

        Args:
            context: Immutable execution context for the current pipeline run.

        Raises:
            NotImplementedError: Until orchestration behavior is implemented.
        """
        self._repository.load(source_name)

        raise NotImplementedError("Bronze ingestion orchestration is not implemented yet.")
