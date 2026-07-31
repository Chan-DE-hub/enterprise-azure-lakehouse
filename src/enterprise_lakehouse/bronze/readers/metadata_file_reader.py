"""Metadata-driven file reader composition."""

from typing import Any, Protocol

from enterprise_lakehouse.bronze.models import (
    PipelineContext,
    SourceMetadata,
)
from enterprise_lakehouse.bronze.readers.base_reader import BaseReader
from enterprise_lakehouse.bronze.readers.file_loader import FileLoader
from enterprise_lakehouse.bronze.readers.file_reader import FileReader


class LoaderComposerProtocol(Protocol):
    """Contract for composing file loaders."""

    def compose(self, *, ingestion_mode: str) -> FileLoader:
        """Return the loader for the requested ingestion mode."""
        ...


class MetadataFileReader(BaseReader):
    """Select and execute a file loader using source metadata."""

    def __init__(self, *, composer: LoaderComposerProtocol) -> None:
        """Initialize with a loader composer."""
        self._composer = composer

    @property
    def source_type(self) -> str:
        """Return the source type handled by this reader."""
        return "file"

    def compose_loader(self, *, metadata: SourceMetadata) -> FileLoader:
        """Compose the appropriate loader from source metadata."""
        return self._composer.compose(
            ingestion_mode=metadata.ingestion_mode,
        )

    def read(
        self,
        *,
        context: PipelineContext,
        metadata: SourceMetadata,
    ) -> Any:
        """Select a loader and read the configured file source."""
        loader = self.compose_loader(metadata=metadata)
        reader = FileReader(loader=loader)

        return reader.read(
            context=context,
            metadata=metadata,
        )
