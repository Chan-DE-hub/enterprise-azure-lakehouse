"""Tests for Gold definition composition."""

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
from enterprise_lakehouse.gold import (
    GoldDatasetType,
    GoldDefinitionFactory,
)


def build_metadata(
    *,
    gold_table: str | None = None,
) -> SourceMetadata:
    """Build representative metadata for Gold definition tests."""
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
            gold_table=gold_table,
            checkpoint_path="/Volumes/workspace/checkpoints/orders",
        ),
        governance=GovernanceMetadata(
            business_domain="sales",
            owner="data-platform",
            data_classification=DataClassification.INTERNAL,
        ),
        primary_keys=("order_id",),
        watermark_column="modified_at",
        file_format=FileFormat.JSON,
    )


def test_factory_builds_fact_definition_from_source_metadata() -> None:
    """The factory should resolve physical identifiers from source metadata."""
    metadata = build_metadata()

    definition = GoldDefinitionFactory().build(
        metadata=metadata,
        dataset_name="fact_order",
        dataset_type=GoldDatasetType.FACT,
        grain="one row per order",
    )

    assert definition.dataset_name == "fact_order"
    assert definition.dataset_type is GoldDatasetType.FACT
    assert definition.source_tables == ("workspace.silver.silver_orders",)
    assert definition.target_table == ("workspace.gold.fact_order")
    assert definition.grain == "one row per order"
    assert definition.business_domain == "sales"


def test_factory_uses_configured_gold_table_when_present() -> None:
    """Configured Gold table names should override the logical dataset name."""
    metadata = build_metadata(
        gold_table="fact_sales_order",
    )

    definition = GoldDefinitionFactory().build(
        metadata=metadata,
        dataset_name="fact_order",
        dataset_type=GoldDatasetType.FACT,
        grain="one row per order",
    )

    assert definition.target_table == ("workspace.gold.fact_sales_order")


def test_factory_requires_silver_source_table() -> None:
    """Gold datasets should be built from trusted Silver sources."""
    metadata = build_metadata().model_copy(
        update={
            "target": build_metadata().target.model_copy(
                update={
                    "silver_table": None,
                },
            ),
        },
    )

    try:
        GoldDefinitionFactory().build(
            metadata=metadata,
            dataset_name="fact_order",
            dataset_type=GoldDatasetType.FACT,
            grain="one row per order",
        )
    except ValueError as error:
        assert str(error) == ("silver_table is required for Gold processing.")
    else:
        raise AssertionError("GoldDefinitionFactory must require a Silver source table")
