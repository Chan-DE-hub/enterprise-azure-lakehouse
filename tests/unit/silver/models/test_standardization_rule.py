"""Tests for Silver standardization rules."""

import pytest
from pydantic import ValidationError

from enterprise_lakehouse.silver.models import (
    StandardizationRule,
    TextCase,
)


def test_standardization_rule_stores_column_configuration() -> None:
    """The rule should store reusable column-standardization settings."""
    rule = StandardizationRule(
        source_column="Order Total",
        target_column="order_total",
        data_type="decimal(18,2)",
        trim=False,
        text_case=TextCase.NONE,
    )

    assert rule.source_column == "Order Total"
    assert rule.target_column == "order_total"
    assert rule.resolved_target_column == "order_total"
    assert rule.data_type == "decimal(18,2)"
    assert rule.trim is False
    assert rule.text_case is TextCase.NONE


def test_standardization_rule_defaults_optional_operations() -> None:
    """Optional standardization operations should default safely."""
    rule = StandardizationRule(
        source_column="order_id",
        data_type="long",
    )

    assert rule.resolved_target_column == "order_id"
    assert rule.trim is False
    assert rule.text_case is TextCase.NONE
    assert rule.parse_format is None


def test_standardization_rule_supports_parse_format() -> None:
    """Timestamp and date parsing may use an explicit source format."""
    rule = StandardizationRule(
        source_column="modified_at",
        data_type="timestamp",
        parse_format="yyyy-MM-dd'T'HH:mm:ssX",
    )

    assert rule.parse_format == "yyyy-MM-dd'T'HH:mm:ssX"


def test_standardization_rule_is_immutable() -> None:
    """Standardization rules should not mutate during processing."""
    rule = StandardizationRule(
        source_column="order_id",
        data_type="long",
    )

    with pytest.raises(ValidationError):
        rule.data_type = "string"


def test_standardization_rule_rejects_unknown_fields() -> None:
    """Unknown standardization fields should fail fast."""
    with pytest.raises(ValidationError):
        StandardizationRule(
            source_column="order_id",
            data_type="long",
            unsupported_setting=True,
        )
