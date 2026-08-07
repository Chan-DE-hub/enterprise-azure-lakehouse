"""Tests for reusable Silver definition composition."""

from unittest.mock import Mock

from enterprise_lakehouse.common.metadata.models import (
    DataClassification,
    FileFormat,
    GovernanceMetadata,
    LoadType,
    SilverProcessingStrategy,
    SourceLocation,
    SourceMetadata,
    SourceType,
    StandardizationColumnMetadata,
    StandardizationMetadata,
    TargetMetadata,
)
from enterprise_lakehouse.silver import SilverDefinitionFactory
from enterprise_lakehouse.silver.metadata import ProcessingStrategyFactory
from enterprise_lakehouse.silver.models import StandardizationRule
from enterprise_lakehouse.silver.processors import StandardizationProcessor


def build_metadata() -> SourceMetadata:
    """Build representative metadata for Silver definition tests."""
    return SourceMetadata(
        source_id="sales_orders",
        source_system="erp",
        source_type=SourceType.FILE,
        load_type=LoadType.STREAMING,
        location=SourceLocation(
            object_name="sales_orders",
            path="/Volumes/workspace/landing/sales_orders",
        ),
        target=TargetMetadata(
            catalog_name="workspace",
            bronze_table="bronze_sales_orders",
            silver_table="silver_orders",
            checkpoint_path="/Volumes/workspace/checkpoints/sales_orders",
        ),
        governance=GovernanceMetadata(
            business_domain="sales",
            owner="data-engineering",
            data_classification=DataClassification.INTERNAL,
        ),
        primary_keys=("order_id",),
        watermark_column="modified_at",
        file_format=FileFormat.JSON,
        standardization=StandardizationMetadata(
            columns=(
                StandardizationColumnMetadata(
                    source_column="order_id",
                    data_type="long",
                ),
            ),
        ),
    )


def test_factory_composes_definition_from_source_metadata() -> None:
    """The factory should compose reusable Silver components."""
    metadata = build_metadata()

    additional_processor = Mock(name="additional_processor")

    standardization_rule = StandardizationRule(
        source_column="order_id",
        target_column=None,
        data_type="long",
    )

    standardization_factory = Mock()
    standardization_factory.build.return_value = (standardization_rule,)

    expectation_factory = Mock()
    expectation_factory.build.return_value = Mock(
        retain={
            "order_id_present": "order_id IS NOT NULL",
        },
        drop={
            "valid_order_id": "order_id > 0",
        },
    )

    quarantine_factory = Mock()
    quarantine_factory.build.return_value = "NOT((order_id > 0))"

    processing_strategy_factory = ProcessingStrategyFactory()

    factory = SilverDefinitionFactory(
        standardization_factory=standardization_factory,
        expectation_factory=expectation_factory,
        quarantine_factory=quarantine_factory,
        processing_strategy_factory=processing_strategy_factory,
    )

    definition = factory.build(
        metadata=metadata,
        additional_processors=(additional_processor,),
    )

    assert definition.source_table == ("workspace.bronze.bronze_sales_orders")
    assert definition.silver_table == "silver_orders"
    assert definition.quarantine_table == ("workspace.quarantine.silver_orders_quarantine")

    assert len(definition.processors) == 2

    assert isinstance(
        definition.processors[0],
        StandardizationProcessor,
    )

    assert definition.processors[1] is additional_processor

    assert definition.expectation_rules == {
        "order_id_present": "order_id IS NOT NULL",
        "valid_order_id": "order_id > 0",
    }

    assert definition.quarantine_predicate == ("NOT((order_id > 0))")

    assert definition.processing_strategy is SilverProcessingStrategy.APPEND

    standardization_factory.build.assert_called_once_with(
        metadata.standardization,
    )

    expectation_factory.build.assert_called_once_with(
        metadata.data_quality,
    )

    quarantine_factory.build.assert_called_once_with(
        {
            "valid_order_id": "order_id > 0",
        },
    )
