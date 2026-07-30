"""Bronze ingestion orchestration engine."""

from enterprise_lakehouse.bronze.models import PipelineContext
from enterprise_lakehouse.bronze.readers import BaseReader


class IngestionEngine:
    """Coordinate a Bronze ingestion workflow."""

    def __init__(self, reader: BaseReader) -> None:
        """Initialize the engine with a source reader."""
        self._reader = reader

    @property
    def reader(self) -> BaseReader:
        """Return the reader used by this engine."""
        return self._reader

    def run(self, context: PipelineContext) -> None:
        """Execute a Bronze ingestion run.

        Args:
            context: Immutable execution context for the current pipeline run.

        Raises:
            NotImplementedError: Until orchestration behavior is implemented.
        """
        raise NotImplementedError("Bronze ingestion orchestration is not implemented yet.")
