"""Tests for the Gold order fact transformation."""

from unittest.mock import Mock

from enterprise_lakehouse.gold.facts import OrderFactTransformer


def test_order_fact_transformer_selects_business_columns() -> None:
    """The order fact should expose only business-facing fact columns."""
    dataframe = Mock(name="silver_orders_dataframe")

    transformer = OrderFactTransformer()

    result = transformer.transform(dataframe)

    dataframe.select.assert_called_once_with(
        "order_id",
        "customer_id",
        "order_total",
        "order_status",
        "modified_at",
    )

    assert result is dataframe.select.return_value
