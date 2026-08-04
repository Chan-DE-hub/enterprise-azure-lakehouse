"""Tests for Silver orders standardization."""

from unittest.mock import Mock, call, patch

from enterprise_lakehouse.silver.processors.orders_standardization_processor import (
    OrdersStandardizationProcessor,
)


def test_processor_applies_order_column_standardization() -> None:
    """The processor should apply Silver transformations in order."""
    dataframe = Mock()
    dataframe.withColumn.return_value = dataframe

    processor = OrdersStandardizationProcessor()

    order_id_expression = object()
    customer_id_expression = object()
    order_total_expression = object()
    modified_at_expression = object()
    order_status_expression = object()

    with (
        patch.object(
            processor,
            "cast_long",
            side_effect=[
                order_id_expression,
                customer_id_expression,
            ],
        ) as cast_long,
        patch.object(
            processor,
            "cast_decimal",
            return_value=order_total_expression,
        ) as cast_decimal,
        patch.object(
            processor,
            "cast_timestamp",
            return_value=modified_at_expression,
        ) as cast_timestamp,
        patch.object(
            processor,
            "normalize_text",
            return_value=order_status_expression,
        ) as normalize_text,
    ):
        result = processor.process(dataframe)

    assert result is dataframe

    assert cast_long.call_args_list == [
        call("order_id"),
        call("customer_id"),
    ]
    cast_decimal.assert_called_once_with(
        "order_total",
        precision=18,
        scale=2,
    )
    cast_timestamp.assert_called_once_with("modified_at")
    normalize_text.assert_called_once_with("order_status")

    assert dataframe.withColumn.call_args_list == [
        call("order_id", order_id_expression),
        call("customer_id", customer_id_expression),
        call("order_total", order_total_expression),
        call("modified_at", modified_at_expression),
        call("order_status", order_status_expression),
    ]
