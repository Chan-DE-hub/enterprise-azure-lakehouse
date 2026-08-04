"""Standardize Bronze orders into typed Silver columns."""

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType


class OrdersStandardizationProcessor:
    """Apply deterministic technical standardization to orders."""

    def process(self, dataframe: DataFrame) -> DataFrame:
        """Return an orders DataFrame with standardized Silver columns."""
        return (
            dataframe.withColumn(
                "order_id",
                self.cast_long("order_id"),
            )
            .withColumn(
                "customer_id",
                self.cast_long("customer_id"),
            )
            .withColumn(
                "order_total",
                self.cast_decimal(
                    "order_total",
                    precision=18,
                    scale=2,
                ),
            )
            .withColumn(
                "modified_at",
                self.cast_timestamp("modified_at"),
            )
            .withColumn(
                "order_status",
                self.normalize_text("order_status"),
            )
        )

    def cast_long(self, column_name: str) -> Column:
        """Cast a source column to a long integer."""
        return F.col(column_name).cast("long")

    def cast_decimal(
        self,
        column_name: str,
        *,
        precision: int,
        scale: int,
    ) -> Column:
        """Cast a source column to a fixed-precision decimal."""
        return F.col(column_name).cast(
            DecimalType(
                precision=precision,
                scale=scale,
            )
        )

    def cast_timestamp(self, column_name: str) -> Column:
        """Cast a source column to a timestamp."""
        return F.to_timestamp(F.col(column_name))

    def normalize_text(self, column_name: str) -> Column:
        """Trim and lowercase a textual source column."""
        return F.lower(
            F.trim(
                F.col(column_name),
            )
        )
