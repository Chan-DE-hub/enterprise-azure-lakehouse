"""Gold customer dimension transformation."""

from pyspark.sql import DataFrame


class CustomerDimensionTransformer:
    """Transform trusted Silver customers into the Gold customer dimension."""

    def transform(
        self,
        dataframe: DataFrame,
    ) -> DataFrame:
        """Select current business-facing customer attributes."""
        return dataframe.select(
            "customer_id",
            "customer_name",
            "email",
            "customer_status",
            "modified_at",
        )
