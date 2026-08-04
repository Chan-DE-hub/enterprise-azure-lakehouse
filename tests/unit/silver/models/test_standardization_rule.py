"""Tests for Silver standardization rules."""

import pytest
from pydantic import ValidationError

from enterprise_lakehouse.silver.models.standardization_rule import (
    StandardizationRule,
)


def test_standardization_rule_stores_column_configuration() -> None:
    """The rule should store reusable column-standardization settings."""
    rule = StandardizationRule(
        column_name="order_total",
        data_type="decimal(18,2)",
        trim=False,
        lowercase=False,
    )

    assert rule.column_name == "order_total"
    assert rule.data_type == "decimal(18,2)"
    assert rule.trim is False
    assert rule.lowercase is False


def test_standardization_rule_defaults_optional_operations() -> None:
    """Optional text-normalization operations should default to disabled."""
    rule = StandardizationRule(
        column_name="order_id",
        data_type="long",
    )

    assert rule.trim is False
    assert rule.lowercase is False


def test_standardization_rule_is_immutable() -> None:
    """Standardization metadata should not mutate during processing."""
    rule = StandardizationRule(
        column_name="order_id",
        data_type="long",
    )

    with pytest.raises(ValidationError):
        rule.data_type = "string"


def test_standardization_rule_rejects_unknown_fields() -> None:
    """Unknown metadata fields should fail fast."""
    with pytest.raises(ValidationError):
        StandardizationRule(
            column_name="order_id",
            data_type="long",
            unsupported_setting=True,
        )
