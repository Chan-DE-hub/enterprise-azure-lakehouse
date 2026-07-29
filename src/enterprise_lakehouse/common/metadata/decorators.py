"""Base decorator implementations for metadata repositories."""

from __future__ import annotations

from enterprise_lakehouse.common.metadata.models import SourceMetadata
from enterprise_lakehouse.common.metadata.repository import MetadataRepository


class MetadataRepositoryDecorator(MetadataRepository):
    """Base class for repository decorators."""

    def __init__(
        self,
        repository: MetadataRepository,
    ) -> None:
        self._repository = repository

    def load(
        self,
    ) -> list[SourceMetadata]:
        return self._repository.load()
