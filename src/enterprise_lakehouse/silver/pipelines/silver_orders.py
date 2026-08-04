"""Lakeflow declarative Silver orders dataset."""

from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession

from enterprise_lakehouse.silver.pipelines import SilverPipeline
from enterprise_lakehouse.silver.processors import (
    OrdersStandardizationProcessor,
)


def get_spark_session() -> SparkSession:
    """Return the active Spark session for the Silver pipeline."""
    spark = SparkSession.getActiveSession()

    if spark is None:
        raise RuntimeError(
            "No active Spark session is available for the Silver pipeline.",
        )

    return spark


@dp.table(
    name="silver_orders",
    comment="Typed and standardized sales orders from the Bronze layer.",
)
def silver_orders() -> DataFrame:
    """Define the Silver orders streaming table."""
    spark = get_spark_session()

    source_dataframe = spark.readStream.table(
        "workspace.bronze.bronze_orders",
    )

    pipeline = SilverPipeline(
        processors=(OrdersStandardizationProcessor(),),
    )

    return pipeline.run(source_dataframe)
