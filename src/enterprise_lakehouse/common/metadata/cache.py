"""Cached metadata repository implementation."""

from __future__ import annotations

from enterprise_lakehouse.common.metadata.decorators import (
    MetadataRepositoryDecorator,
)
from enterprise_lakehouse.common.metadata.models import SourceMetadata
from enterprise_lakehouse.common.metadata.repository import MetadataRepository


class CachedMetadataRepository(
    MetadataRepositoryDecorator,
):
    """Cache metadata loaded by another repository."""

    def __init__(
        self,
        repository: MetadataRepository,
    ) -> None:
        """Initialize the cached repository decorator."""

        super().__init__(repository)
        self._cache: list[SourceMetadata] | None = None

    def load(
        self,
    ) -> list[SourceMetadata]:
        """Load metadata from cache or the wrapped repository."""

        if self._cache is None:
            self._cache = self._repository.load()

        return self._cache

    def clear_cache(
        self,
    ) -> None:
        """Invalidate cached metadata."""

        self._cache = None
