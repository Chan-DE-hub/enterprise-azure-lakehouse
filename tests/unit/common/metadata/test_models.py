"""Tests for typed metadata models."""

import pytest
from pydantic import ValidationError

from enterprise_lakehouse.common.metadata import (
    FileFormat,
    GovernanceMetadata,
    LoadType,
    SourceLocation,
    SourceMetadata,
    SourceType,
    TargetMetadata,
)


def create_target_metadata(
    *,
    checkpoint_path: str | None = None,
) -> TargetMetadata:
    """Create reusable target metadata for tests."""

    return TargetMetadata(
        catalog_name="dev_sales_lakehouse",
        bronze_table="orders",
        silver_table="orders",
        checkpoint_path=checkpoint_path,
        schema_location_path="/Volumes/dev/config/schemas/orders",
    )


def create_governance_metadata() -> GovernanceMetadata:
    """Create reusable governance metadata for tests."""

    return GovernanceMetadata(
        business_domain="sales",
        owner="data-platform-team",
        tags=("orders", "finance"),
        sla_minutes=60,
    )


def test_create_valid_file_source_metadata() -> None:
    metadata = SourceMetadata(
        source_id="sales_orders_file",
        source_system="sales_drop_zone",
        source_type=SourceType.FILE,
        load_type=LoadType.INCREMENTAL,
        location=SourceLocation(
            object_name="orders",
            path="/Volumes/dev/landing/orders",
        ),
        target=create_target_metadata(),
        governance=create_governance_metadata(),
        primary_keys=("order_id",),
        watermark_column="modified_at",
        file_format=FileFormat.JSON,
    )

    assert metadata.source_id == "sales_orders_file"
    assert metadata.file_format is FileFormat.JSON
    assert metadata.target.bronze_schema == "bronze"
    assert metadata.enabled is True
    assert metadata.priority == 100


def test_incremental_loading_requires_watermark_column() -> None:
    with pytest.raises(
        ValidationError,
        match="watermark_column is required",
    ):
        SourceMetadata(
            source_id="sales_orders",
            source_system="sales_db",
            source_type=SourceType.DATABASE,
            load_type=LoadType.INCREMENTAL,
            location=SourceLocation(
                database="sales",
                schema_name="dbo",
                object_name="orders",
            ),
            target=create_target_metadata(),
            governance=create_governance_metadata(),
            primary_keys=("order_id",),
        )


def test_cdc_loading_requires_primary_keys() -> None:
    with pytest.raises(
        ValidationError,
        match="primary_keys are required",
    ):
        SourceMetadata(
            source_id="sales_orders_cdc",
            source_system="sales_db",
            source_type=SourceType.DATABASE,
            load_type=LoadType.CDC,
            location=SourceLocation(
                database="sales",
                schema_name="dbo",
                object_name="orders",
            ),
            target=create_target_metadata(),
            governance=create_governance_metadata(),
            sequence_column="change_sequence",
            operation_column="operation",
        )


def test_streaming_loading_requires_checkpoint_path() -> None:
    with pytest.raises(
        ValidationError,
        match="checkpoint_path is required",
    ):
        SourceMetadata(
            source_id="sales_orders_stream",
            source_system="event_hub",
            source_type=SourceType.EVENT_HUB,
            load_type=LoadType.STREAMING,
            location=SourceLocation(
                object_name="orders",
                topic_name="sales-orders",
            ),
            target=create_target_metadata(),
            governance=create_governance_metadata(),
        )


def test_event_hub_source_requires_topic_name() -> None:
    with pytest.raises(
        ValidationError,
        match="topic_name is required",
    ):
        SourceMetadata(
            source_id="sales_orders_stream",
            source_system="event_hub",
            source_type=SourceType.EVENT_HUB,
            load_type=LoadType.STREAMING,
            location=SourceLocation(
                object_name="orders",
            ),
            target=create_target_metadata(
                checkpoint_path="/Volumes/dev/checkpoints/orders",
            ),
            governance=create_governance_metadata(),
        )


def test_file_source_requires_file_format() -> None:
    with pytest.raises(
        ValidationError,
        match="file_format is required",
    ):
        SourceMetadata(
            source_id="sales_orders_file",
            source_system="sales_drop_zone",
            source_type=SourceType.FILE,
            load_type=LoadType.FULL,
            location=SourceLocation(
                object_name="orders",
                path="/Volumes/dev/landing/orders",
            ),
            target=create_target_metadata(),
            governance=create_governance_metadata(),
        )


def test_unknown_metadata_fields_are_rejected() -> None:
    with pytest.raises(ValidationError, match="extra_forbidden"):
        SourceLocation(
            object_name="orders",
            unsupported_field="invalid",
        )


def test_metadata_is_immutable() -> None:
    metadata = SourceLocation(
        object_name="orders",
        path="/Volumes/dev/landing/orders",
    )

    with pytest.raises(ValidationError, match="frozen"):
        metadata.object_name = "customers"
