"""Tests for metadata-driven file reading."""

from collections.abc import Mapping
from typing import Any

from enterprise_lakehouse.bronze.readers.file_loader import FileLoader
from enterprise_lakehouse.bronze.readers.metadata_file_reader import (
    MetadataFileReader,
)
from enterprise_lakehouse.common.metadata.models import (
    FileFormat,
    GovernanceMetadata,
    LoadType,
    SourceLocation,
    SourceMetadata,
    SourceType,
    TargetMetadata,
)


class FakeFileLoader:
    """Minimal file loader returned by the fake composer."""

    def __call__(
        self,
        *,
        path: str,
        file_format: str,
        options: Mapping[str, Any],
    ) -> Any:
        """Return the supplied loading arguments."""
        return {
            "path": path,
            "file_format": file_format,
            "options": dict(options),
        }


class FakeComposer:
    """Test double that records the requested ingestion mode."""

    def __init__(self) -> None:
        """Initialize the composer without a recorded call."""
        self.called_with: str | None = None
        self.loader = FakeFileLoader()

    def compose(self, *, ingestion_mode: str) -> FileLoader:
        """Record the ingestion mode and return a fake loader."""
        self.called_with = ingestion_mode
        return self.loader


def create_metadata(*, load_type: LoadType) -> SourceMetadata:
    """Create canonical metadata for loader-composition tests."""
    checkpoint_path = "/Volumes/checkpoints/orders" if load_type is LoadType.STREAMING else None

    return SourceMetadata(
        source_id="orders",
        source_system="erp",
        source_type=SourceType.FILE,
        load_type=load_type,
        location=SourceLocation(
            object_name="orders",
            path="/Volumes/raw/orders",
        ),
        target=TargetMetadata(
            catalog_name="dev_sales_lakehouse",
            bronze_table="orders",
            checkpoint_path=checkpoint_path,
        ),
        governance=GovernanceMetadata(
            business_domain="sales",
            owner="data_engineering",
        ),
        file_format=FileFormat.PARQUET,
    )


def test_batch_metadata_selects_batch_loader() -> None:
    """Non-streaming metadata should select the batch loader."""
    composer = FakeComposer()
    reader = MetadataFileReader(composer=composer)

    reader.compose_loader(
        metadata=create_metadata(load_type=LoadType.FULL),
    )

    assert composer.called_with == "batch"


def test_streaming_metadata_selects_streaming_loader() -> None:
    """Streaming metadata should select the streaming loader."""
    composer = FakeComposer()
    reader = MetadataFileReader(composer=composer)

    reader.compose_loader(
        metadata=create_metadata(load_type=LoadType.STREAMING),
    )

    assert composer.called_with == "streaming"
