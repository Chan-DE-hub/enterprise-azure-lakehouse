"""Tests for the Gold customer dimension transformation."""

from unittest.mock import Mock

from enterprise_lakehouse.gold.dimensions import (
    CustomerDimensionTransformer,
)


def test_customer_dimension_transformer_selects_business_columns() -> None:
    """The customer dimension should expose current business attributes."""
    dataframe = Mock(name="silver_customers_dataframe")

    transformer = CustomerDimensionTransformer()

    result = transformer.transform(dataframe)

    dataframe.select.assert_called_once_with(
        "customer_id",
        "customer_name",
        "email",
        "customer_status",
        "modified_at",
    )

    assert result is dataframe.select.return_value
