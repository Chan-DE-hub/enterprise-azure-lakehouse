"""Gold customer order summary transformation."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


class CustomerOrderSummaryTransformer:
    """Aggregate Gold order facts at one-row-per-customer grain."""

    def transform(
        self,
        dataframe: DataFrame,
    ) -> DataFrame:
        """Aggregate customer-level order measures."""
        return dataframe.groupBy(
            "customer_id",
        ).agg(
            F.count("*").alias(
                "order_count",
            ),
            F.sum(
                "order_total",
            ).alias(
                "total_order_amount",
            ),
            F.avg(
                "order_total",
            ).alias(
                "average_order_value",
            ),
        )
