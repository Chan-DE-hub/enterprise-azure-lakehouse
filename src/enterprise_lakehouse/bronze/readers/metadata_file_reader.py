"""Metadata-driven file reader composition."""

from typing import Protocol

from enterprise_lakehouse.bronze.readers.file_loader import FileLoader


class LoaderComposerProtocol(Protocol):
    """Contract for composing file loaders."""

    def compose(self, *, ingestion_mode: str) -> FileLoader:
        """Return the loader for the requested ingestion mode."""
        ...


class MetadataProtocol(Protocol):
    """Minimum metadata required for loader composition."""

    ingestion_mode: str


class MetadataFileReader:
    """Select a file loader using source metadata."""

    def __init__(self, *, composer: LoaderComposerProtocol) -> None:
        """Initialize with a loader composer."""
        self._composer = composer

    def compose_loader(self, *, metadata: MetadataProtocol) -> FileLoader:
        """Compose the appropriate loader from metadata."""
        return self._composer.compose(
            ingestion_mode=metadata.ingestion_mode,
        )
