"""Tests for the Gold customer order summary transformation."""

from unittest.mock import Mock, patch

from enterprise_lakehouse.gold.aggregates import (
    CustomerOrderSummaryTransformer,
)


def test_customer_order_summary_aggregates_orders_by_customer() -> None:
    """The summary should aggregate order measures at customer grain."""
    dataframe = Mock(name="fact_order_dataframe")

    grouped_dataframe = Mock(name="grouped_dataframe")
    aggregated_dataframe = Mock(name="aggregated_dataframe")

    dataframe.groupBy.return_value = grouped_dataframe
    grouped_dataframe.agg.return_value = aggregated_dataframe

    order_count_expression = Mock(name="order_count_expression")
    total_amount_expression = Mock(name="total_amount_expression")
    average_value_expression = Mock(name="average_value_expression")

    order_count_alias = Mock(name="order_count_alias")
    total_amount_alias = Mock(name="total_amount_alias")
    average_value_alias = Mock(name="average_value_alias")

    order_count_expression.alias.return_value = order_count_alias
    total_amount_expression.alias.return_value = total_amount_alias
    average_value_expression.alias.return_value = average_value_alias

    transformer = CustomerOrderSummaryTransformer()

    with (
        patch(
            "enterprise_lakehouse.gold.aggregates.customer_order_summary.F.count",
            return_value=order_count_expression,
        ) as count_mock,
        patch(
            "enterprise_lakehouse.gold.aggregates.customer_order_summary.F.sum",
            return_value=total_amount_expression,
        ) as sum_mock,
        patch(
            "enterprise_lakehouse.gold.aggregates.customer_order_summary.F.avg",
            return_value=average_value_expression,
        ) as avg_mock,
    ):
        result = transformer.transform(dataframe)

    dataframe.groupBy.assert_called_once_with(
        "customer_id",
    )

    count_mock.assert_called_once_with("*")
    sum_mock.assert_called_once_with("order_total")
    avg_mock.assert_called_once_with("order_total")

    order_count_expression.alias.assert_called_once_with(
        "order_count",
    )
    total_amount_expression.alias.assert_called_once_with(
        "total_order_amount",
    )
    average_value_expression.alias.assert_called_once_with(
        "average_order_value",
    )

    grouped_dataframe.agg.assert_called_once_with(
        order_count_alias,
        total_amount_alias,
        average_value_alias,
    )

    assert result is aggregated_dataframe
