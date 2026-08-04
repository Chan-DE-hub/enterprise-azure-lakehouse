"""Tests for the generic Silver standardization processor."""

from unittest.mock import Mock, call, patch

from enterprise_lakehouse.silver.models import StandardizationRule
from enterprise_lakehouse.silver.processors.standardization_processor import (
    StandardizationProcessor,
)


def test_processor_applies_rules_in_order() -> None:
    """The processor should apply standardization rules sequentially."""
    dataframe = Mock()
    dataframe.withColumn.return_value = dataframe

    rules = (
        StandardizationRule(
            column_name="order_id",
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

    processor = StandardizationProcessor(rules=rules)

    order_id_expression = object()
    order_total_expression = object()
    modified_at_expression = object()
    order_status_expression = object()

    with patch.object(
        processor,
        "build_expression",
        side_effect=[
            order_id_expression,
            order_total_expression,
            modified_at_expression,
            order_status_expression,
        ],
    ) as build_expression:
        result = processor.process(dataframe)

    assert result is dataframe

    assert build_expression.call_args_list == [
        call(rules[0]),
        call(rules[1]),
        call(rules[2]),
        call(rules[3]),
    ]

    assert dataframe.withColumn.call_args_list == [
        call("order_id", order_id_expression),
        call("order_total", order_total_expression),
        call("modified_at", modified_at_expression),
        call("order_status", order_status_expression),
    ]


def test_processor_returns_source_when_no_rules_exist() -> None:
    """The processor should preserve the source when no rules are configured."""
    dataframe = Mock()

    processor = StandardizationProcessor(rules=())

    result = processor.process(dataframe)

    assert result is dataframe
    dataframe.withColumn.assert_not_called()
