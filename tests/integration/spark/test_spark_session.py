"""Integration tests for the local PySpark environment."""

import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession


def test_local_spark_session_executes_dataframe_operation() -> None:
    """The local Spark environment should execute real DataFrame logic."""
    spark = (
        SparkSession.builder.master("local[1]")
        .appName("enterprise-lakehouse-tests")
        .config("spark.ui.enabled", "false")
        .config("spark.pyspark.python", sys.executable)
        .config("spark.pyspark.driver.python", sys.executable)
        .getOrCreate()
    )

    try:
        dataframe = spark.createDataFrame(
            [
                (1, "orders"),
                (2, "customers"),
            ],
            schema=["source_id", "source_name"],
        )

        assert dataframe.count() == 2
        assert dataframe.columns == [
            "source_id",
            "source_name",
        ]
    finally:
        spark.stop()
