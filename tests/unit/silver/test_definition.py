"""Tests for reusable Silver framework definitions."""

from enterprise_lakehouse.common.metadata.models import (
    SilverProcessingStrategy,
)
from enterprise_lakehouse.silver import SilverDefinition


def test_silver_definition_stores_composed_framework_components() -> None:
    """A Silver definition should contain reusable pipeline components."""
    processors = ("standardization", "deduplication")

    definition = SilverDefinition(
        source_table="workspace.bronze.bronze_orders",
        silver_table="silver_orders",
        quarantine_table="workspace.quarantine.silver_orders_quarantine",
        processors=processors,
        expectation_rules={
            "valid_order_id": "order_id IS NOT NULL",
        },
        quarantine_predicate="NOT (order_id IS NOT NULL)",
        processing_strategy=SilverProcessingStrategy.APPEND,
    )

    assert definition.source_table == "workspace.bronze.bronze_orders"
    assert definition.silver_table == "silver_orders"
    assert definition.quarantine_table == ("workspace.quarantine.silver_orders_quarantine")
    assert definition.processors == processors
    assert definition.expectation_rules == {
        "valid_order_id": "order_id IS NOT NULL",
    }
    assert definition.quarantine_predicate == ("NOT (order_id IS NOT NULL)")
    assert definition.processing_strategy is SilverProcessingStrategy.APPEND


def test_silver_definition_is_immutable() -> None:
    """Framework definitions should be immutable after construction."""
    definition = SilverDefinition(
        source_table="workspace.bronze.bronze_orders",
        silver_table="silver_orders",
        quarantine_table="workspace.quarantine.silver_orders_quarantine",
        processors=(),
        expectation_rules={},
        quarantine_predicate="FALSE",
        processing_strategy=SilverProcessingStrategy.APPEND,
    )

    try:
        definition.silver_table = "changed"
    except AttributeError:
        pass
    else:
        raise AssertionError("SilverDefinition must be immutable")
