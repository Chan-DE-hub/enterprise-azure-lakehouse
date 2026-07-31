"""Tests for the SourceMetadata model."""

from dataclasses import FrozenInstanceError

import pytest

from enterprise_lakehouse.bronze.models import SourceMetadata


def test_source_metadata_stores_source_configuration() -> None:
    """SourceMetadata should preserve source-level configuration."""

    metadata = SourceMetadata(
        source_name="sales_orders",
        source_type="file",
        ingestion_mode="batch",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column="event_timestamp",
        options={
            "format": "parquet",
            "path": "/Volumes/dev/raw/orders",
        },
    )

    assert metadata.source_name == "sales_orders"
    assert metadata.source_type == "file"
    assert metadata.ingestion_mode == "batch"
    assert metadata.load_mode == "incremental"
    assert metadata.primary_keys == ("order_id",)
    assert metadata.watermark_column == "updated_at"
    assert metadata.event_timestamp_column == "event_timestamp"
    assert metadata.options["format"] == "parquet"
    assert metadata.options["path"] == "/Volumes/dev/raw/orders"


def test_source_metadata_supports_optional_incremental_fields() -> None:
    """Full-load sources should not require incremental columns."""

    metadata = SourceMetadata(
        source_name="product_master",
        source_type="file",
        ingestion_mode="batch",
        load_mode="full",
        primary_keys=("product_id",),
        watermark_column=None,
        event_timestamp_column=None,
        options={"format": "csv"},
    )

    assert metadata.watermark_column is None
    assert metadata.event_timestamp_column is None


def test_source_metadata_primary_keys_are_immutable() -> None:
    """Primary keys should use an immutable tuple."""

    metadata = SourceMetadata(
        source_name="customers",
        source_type="jdbc",
        ingestion_mode="batch",
        load_mode="incremental",
        primary_keys=("customer_id",),
        watermark_column="updated_at",
        event_timestamp_column=None,
        options={"table": "dbo.customers"},
    )

    assert isinstance(metadata.primary_keys, tuple)


def test_source_metadata_options_are_read_only() -> None:
    """Source options should reject mutation after construction."""

    metadata = SourceMetadata(
        source_name="sales_orders",
        source_type="file",
        ingestion_mode="batch",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column=None,
        options={"format": "parquet"},
    )

    with pytest.raises(TypeError):
        metadata.options["format"] = "csv"  # type: ignore[index]


def test_source_metadata_is_immutable() -> None:
    """SourceMetadata should reject attribute reassignment."""

    metadata = SourceMetadata(
        source_name="sales_orders",
        source_type="file",
        ingestion_mode="batch",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column=None,
        options={"format": "parquet"},
    )

    with pytest.raises(FrozenInstanceError):
        metadata.load_mode = "full"  # type: ignore[misc]


def test_equal_source_metadata_instances_compare_as_equal() -> None:
    """Metadata objects with identical values should compare as equal."""

    first_metadata = SourceMetadata(
        source_name="sales_orders",
        source_type="file",
        ingestion_mode="batch",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column=None,
        options={"format": "parquet"},
    )
    second_metadata = SourceMetadata(
        source_name="sales_orders",
        source_type="file",
        ingestion_mode="batch",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column=None,
        options={"format": "parquet"},
    )

    assert first_metadata == second_metadata


def test_source_metadata_stores_ingestion_mode() -> None:
    """Source metadata should preserve the configured ingestion mode."""
    metadata = SourceMetadata(
        source_name="sales_orders",
        source_type="file",
        ingestion_mode="batch",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column="event_timestamp",
        options={"format": "parquet"},
    )

    assert metadata.ingestion_mode == "batch"
