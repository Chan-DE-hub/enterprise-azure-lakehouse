"""Gold order fact transformation."""

from pyspark.sql import DataFrame


class OrderFactTransformer:
    """Transform trusted Silver orders into the Gold order fact."""

    def transform(
        self,
        dataframe: DataFrame,
    ) -> DataFrame:
        """Select business-facing columns at one-row-per-order grain."""
        return dataframe.select(
            "order_id",
            "customer_id",
            "order_total",
            "order_status",
            "modified_at",
        )
