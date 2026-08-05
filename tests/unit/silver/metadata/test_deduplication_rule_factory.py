"""Tests for the Silver deduplication rule factory."""

import pytest

from enterprise_lakehouse.common.metadata.models import (
    DataClassification,
    FileFormat,
    GovernanceMetadata,
    LoadType,
    SourceLocation,
    SourceMetadata,
    SourceType,
    TargetMetadata,
)
from enterprise_lakehouse.silver.metadata import DeduplicationRuleFactory


def build_source_metadata(
    *,
    primary_keys: tuple[str, ...] = ("order_id",),
    watermark_column: str | None = "modified_at",
) -> SourceMetadata:
    """Build valid source metadata for deduplication tests."""
    return SourceMetadata(
        source_id="sales_orders",
        source_system="sales",
        source_type=SourceType.FILE,
        load_type=LoadType.STREAMING,
        location=SourceLocation(
            object_name="orders",
            path="/Volumes/workspace/landing/source_files/orders",
        ),
        target=TargetMetadata(
            catalog_name="workspace",
            bronze_table="bronze_orders",
            silver_table="silver_orders",
            checkpoint_path="/Volumes/workspace/checkpoints/orders",
        ),
        governance=GovernanceMetadata(
            business_domain="sales",
            owner="data-platform",
            data_classification=DataClassification.INTERNAL,
        ),
        primary_keys=primary_keys,
        watermark_column=watermark_column,
        file_format=FileFormat.JSON,
    )


def test_factory_builds_rule_from_source_metadata() -> None:
    """The factory should derive runtime deduplication configuration."""
    metadata = build_source_metadata()

    rule = DeduplicationRuleFactory(
        watermark_delay="10 minutes",
    ).build(metadata)

    assert rule.keys == ("order_id",)
    assert rule.event_time_column == "modified_at"
    assert rule.watermark_delay == "10 minutes"


def test_factory_requires_primary_keys() -> None:
    """Deduplication cannot run without identifying keys."""
    metadata = build_source_metadata(primary_keys=())

    with pytest.raises(
        ValueError,
        match="primary_keys",
    ):
        DeduplicationRuleFactory(
            watermark_delay="10 minutes",
        ).build(metadata)


def test_factory_requires_watermark_column() -> None:
    """Streaming deduplication requires an event-time column."""
    metadata = build_source_metadata(watermark_column=None)

    with pytest.raises(
        ValueError,
        match="watermark_column",
    ):
        DeduplicationRuleFactory(
            watermark_delay="10 minutes",
        ).build(metadata)
