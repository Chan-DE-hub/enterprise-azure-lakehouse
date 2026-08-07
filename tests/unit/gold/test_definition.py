"""Tests for reusable Gold dataset definitions."""

import pytest

from enterprise_lakehouse.gold import (
    GoldDatasetType,
    GoldDefinition,
)


def test_gold_definition_stores_fact_contract() -> None:
    """A Gold fact definition should preserve its business grain."""
    definition = GoldDefinition(
        dataset_name="fact_order",
        dataset_type=GoldDatasetType.FACT,
        source_tables=("workspace.silver.silver_orders",),
        target_table="workspace.gold.fact_order",
        grain="one row per order",
        business_domain="sales",
    )

    assert definition.dataset_name == "fact_order"
    assert definition.dataset_type is GoldDatasetType.FACT
    assert definition.source_tables == ("workspace.silver.silver_orders",)
    assert definition.target_table == "workspace.gold.fact_order"
    assert definition.grain == "one row per order"
    assert definition.business_domain == "sales"


def test_gold_definition_supports_dimension_contract() -> None:
    """A Gold definition should support dimensional datasets."""
    definition = GoldDefinition(
        dataset_name="dim_customer",
        dataset_type=GoldDatasetType.DIMENSION,
        source_tables=("workspace.silver.silver_customers",),
        target_table="workspace.gold.dim_customer",
        grain="one row per current customer",
        business_domain="customer",
    )

    assert definition.dataset_type is GoldDatasetType.DIMENSION
    assert definition.grain == "one row per current customer"


def test_gold_definition_requires_source_tables() -> None:
    """Gold datasets must declare at least one trusted source."""
    with pytest.raises(
        ValueError,
        match="source_tables must contain at least one source",
    ):
        GoldDefinition(
            dataset_name="fact_order",
            dataset_type=GoldDatasetType.FACT,
            source_tables=(),
            target_table="workspace.gold.fact_order",
            grain="one row per order",
            business_domain="sales",
        )


def test_gold_definition_requires_grain() -> None:
    """Gold datasets must explicitly declare their business grain."""
    with pytest.raises(
        ValueError,
        match="grain must not be empty",
    ):
        GoldDefinition(
            dataset_name="fact_order",
            dataset_type=GoldDatasetType.FACT,
            source_tables=("workspace.silver.silver_orders",),
            target_table="workspace.gold.fact_order",
            grain="   ",
            business_domain="sales",
        )


def test_gold_definition_is_immutable() -> None:
    """Gold contracts should not mutate after construction."""
    definition = GoldDefinition(
        dataset_name="fact_order",
        dataset_type=GoldDatasetType.FACT,
        source_tables=("workspace.silver.silver_orders",),
        target_table="workspace.gold.fact_order",
        grain="one row per order",
        business_domain="sales",
    )

    with pytest.raises(AttributeError):
        definition.grain = "changed"


def test_gold_definition_requires_dataset_name() -> None:
    """Gold datasets must declare a logical dataset name."""
    with pytest.raises(
        ValueError,
        match="dataset_name must not be empty",
    ):
        GoldDefinition(
            dataset_name="   ",
            dataset_type=GoldDatasetType.FACT,
            source_tables=("workspace.silver.silver_orders",),
            target_table="workspace.gold.fact_order",
            grain="one row per order",
            business_domain="sales",
        )


def test_gold_definition_requires_target_table() -> None:
    """Gold datasets must declare a physical target table."""
    with pytest.raises(
        ValueError,
        match="target_table must not be empty",
    ):
        GoldDefinition(
            dataset_name="fact_order",
            dataset_type=GoldDatasetType.FACT,
            source_tables=("workspace.silver.silver_orders",),
            target_table="   ",
            grain="one row per order",
            business_domain="sales",
        )


def test_gold_definition_requires_business_domain() -> None:
    """Gold datasets must belong to a business domain."""
    with pytest.raises(
        ValueError,
        match="business_domain must not be empty",
    ):
        GoldDefinition(
            dataset_name="fact_order",
            dataset_type=GoldDatasetType.FACT,
            source_tables=("workspace.silver.silver_orders",),
            target_table="workspace.gold.fact_order",
            grain="one row per order",
            business_domain="   ",
        )


def test_gold_definition_rejects_blank_source_table() -> None:
    """Gold datasets must not contain blank source identifiers."""
    with pytest.raises(
        ValueError,
        match="source_tables must not contain empty values",
    ):
        GoldDefinition(
            dataset_name="fact_order",
            dataset_type=GoldDatasetType.FACT,
            source_tables=(
                "workspace.silver.silver_orders",
                "   ",
            ),
            target_table="workspace.gold.fact_order",
            grain="one row per order",
            business_domain="sales",
        )
