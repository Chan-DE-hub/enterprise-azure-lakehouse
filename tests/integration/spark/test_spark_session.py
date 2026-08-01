"""Integration tests for the local PySpark environment."""

from pyspark.sql import SparkSession


def test_local_spark_session_executes_dataframe_operation(
    spark: SparkSession,
) -> None:
    """The local Spark environment should execute real DataFrame logic."""
    dataframe = spark.createDataFrame(
        [
            (1, "orders"),
            (2, "customers"),
        ],
        schema=[
            "source_id",
            "source_name",
        ],
    )

    assert dataframe.count() == 2
    assert dataframe.columns == [
        "source_id",
        "source_name",
    ]
