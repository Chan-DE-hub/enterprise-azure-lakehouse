"""Tests for the metadata repository contract."""

from typing import override

import pytest

from enterprise_lakehouse.bronze.models import SourceMetadata
from enterprise_lakehouse.bronze.repositories import MetadataRepository


def build_metadata() -> SourceMetadata:
    """Create reusable metadata for repository tests."""

    return SourceMetadata(
        source_name="sales_orders",
        source_type="file",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column="event_timestamp",
        options={"format": "parquet"},
    )


def test_repository_cannot_be_instantiated() -> None:
    """Abstract repositories cannot be instantiated."""

    with pytest.raises(TypeError):
        MetadataRepository()  # type: ignore[abstract]


class FakeMetadataRepository(MetadataRepository):
    """Simple repository implementation for testing."""

    @override
    def load(self, source_name: str) -> SourceMetadata:
        return build_metadata()


def test_load_returns_source_metadata() -> None:
    """Repository implementations should return SourceMetadata."""

    repository = FakeMetadataRepository()

    metadata = repository.load("sales_orders")

    assert isinstance(metadata, SourceMetadata)


def test_load_returns_requested_source() -> None:
    """Repository should return metadata for the requested source."""

    repository = FakeMetadataRepository()

    metadata = repository.load("sales_orders")

    assert metadata.source_name == "sales_orders"
