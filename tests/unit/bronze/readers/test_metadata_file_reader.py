"""Tests for metadata-driven file reading."""

from enterprise_lakehouse.bronze.readers.metadata_file_reader import (
    MetadataFileReader,
)


class FakeMetadata:
    """Fake source metadata."""

    ingestion_mode = "batch"


class FakeComposer:
    """Fake loader composer."""

    def __init__(self) -> None:
        self.called_with = None

    def compose(self, *, ingestion_mode: str):
        self.called_with = ingestion_mode
        return object()


def test_metadata_ingestion_mode_is_forwarded_to_composer() -> None:
    """MetadataFileReader should delegate loader selection to the composer."""
    composer = FakeComposer()

    reader = MetadataFileReader(composer=composer)

    reader.compose_loader(metadata=FakeMetadata())

    assert composer.called_with == "batch"
