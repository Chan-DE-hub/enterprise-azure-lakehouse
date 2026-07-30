"""Abstract repository contract for Bronze source metadata."""

from abc import ABC, abstractmethod

from enterprise_lakehouse.bronze.models import SourceMetadata


class MetadataRepository(ABC):
    """Define how Bronze source metadata is retrieved."""

    @abstractmethod
    def load(self, source_name: str) -> SourceMetadata:
        """Load metadata for a single source.

        Args:
            source_name: Logical name of the source configuration.

        Returns:
            Metadata describing the requested Bronze source.
        """
        raise NotImplementedError
