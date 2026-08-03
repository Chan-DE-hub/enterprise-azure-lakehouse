"""Metadata repository abstractions."""

from __future__ import annotations

from abc import ABC, abstractmethod

from enterprise_lakehouse.common.metadata.models import SourceMetadata


class MetadataRepository(ABC):
    """Abstract metadata repository."""

    @abstractmethod
    def load(self) -> list[SourceMetadata]:
        """Load all metadata definitions."""

    def get(self, source_id: str) -> SourceMetadata:
        """Return one enabled source by its unique identifier.

        Args:
            source_id:
                Unique metadata identifier of the requested source.

        Returns:
            The enabled source metadata matching the requested identifier.

        Raises:
            ValueError:
                If the source identifier is blank, missing, disabled,
                or duplicated.
        """
        normalized_source_id = source_id.strip()

        if not normalized_source_id:
            raise ValueError("Source ID must not be empty")

        matches = [
            metadata
            for metadata in self.load()
            if metadata.source_id == normalized_source_id and metadata.enabled
        ]

        if not matches:
            raise ValueError(
                f"Enabled source metadata not found: {normalized_source_id}",
            )

        if len(matches) > 1:
            raise ValueError(
                f"Duplicate enabled source metadata found: {normalized_source_id}",
            )

        return matches[0]
