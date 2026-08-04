"""Tests for Silver orders standardization configuration."""

from enterprise_lakehouse.silver.models import StandardizationRule
from enterprise_lakehouse.silver.pipelines.silver_orders_config import (
    build_standardization_rules,
)


def test_build_standardization_rules_returns_orders_configuration() -> None:
    """Orders should expose deterministic reusable standardization rules."""
    rules = build_standardization_rules()

    assert rules == (
        StandardizationRule(
            column_name="order_id",
            data_type="long",
        ),
        StandardizationRule(
            column_name="customer_id",
            data_type="long",
        ),
        StandardizationRule(
            column_name="order_total",
            data_type="decimal(18,2)",
        ),
        StandardizationRule(
            column_name="modified_at",
            data_type="timestamp",
        ),
        StandardizationRule(
            column_name="order_status",
            data_type="string",
            trim=True,
            lowercase=True,
        ),
    )
