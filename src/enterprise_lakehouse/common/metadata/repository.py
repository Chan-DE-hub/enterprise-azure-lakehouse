"""Metadata repository abstractions."""

from __future__ import annotations

from abc import ABC, abstractmethod

from enterprise_lakehouse.common.metadata.models import SourceMetadata


class MetadataRepository(ABC):
    """Abstract metadata repository."""

    @abstractmethod
    def load(self) -> list[SourceMetadata]:
        """Load all enabled metadata definitions."""
