"""Tests for the Silver standardization rule factory."""

from enterprise_lakehouse.common.metadata.models import (
    StandardizationMetadata,
    TextCase,
)
from enterprise_lakehouse.silver.metadata.standardization_rule_factory import (
    StandardizationRuleFactory,
)
from enterprise_lakehouse.silver.models import StandardizationRule


def test_factory_builds_standardization_rules_from_typed_metadata() -> None:
    """The factory should convert typed metadata into domain rules."""
    metadata = StandardizationMetadata(
        columns=(
            {
                "source_column": "order_id",
                "data_type": "long",
            },
            {
                "source_column": "Order Status",
                "target_column": "order_status",
                "data_type": "string",
                "trim": True,
                "text_case": "lower",
            },
        )
    )

    result = StandardizationRuleFactory().build(metadata)

    assert result == (
        StandardizationRule(
            source_column="order_id",
            data_type="long",
        ),
        StandardizationRule(
            source_column="Order Status",
            target_column="order_status",
            data_type="string",
            trim=True,
            text_case=TextCase.LOWER,
        ),
    )


def test_factory_returns_empty_rules_when_no_columns_exist() -> None:
    """The factory should return no rules when metadata has no columns."""
    result = StandardizationRuleFactory().build(
        StandardizationMetadata(),
    )

    assert result == ()
