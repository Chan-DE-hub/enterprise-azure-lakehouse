"""Tests for the Spark file loader."""

from typing import Any

from enterprise_lakehouse.bronze.readers.spark_file_loader import SparkFileLoader


class FakeDataFrameReader:
    """Test double for Spark's DataFrameReader."""

    def __init__(self) -> None:
        self.file_format: str | None = None
        self.options_value: dict[str, Any] = {}
        self.path: str | None = None

    def format(self, source: str) -> "FakeDataFrameReader":
        self.file_format = source
        return self

    def options(self, **options: Any) -> "FakeDataFrameReader":
        self.options_value = options
        return self

    def load(self, path: str) -> object:
        self.path = path
        return {"rows": 10}


class FakeSparkSession:
    """Fake SparkSession."""

    def __init__(self) -> None:
        self.read = FakeDataFrameReader()


def test_spark_file_loader_reads_file() -> None:
    """The loader should delegate to Spark's DataFrameReader."""
    spark = FakeSparkSession()

    loader = SparkFileLoader(spark=spark)

    result = loader(
        path="/Volumes/raw/orders",
        file_format="csv",
        options={
            "header": "true",
            "inferSchema": "false",
        },
    )

    assert result == {"rows": 10}

    assert spark.read.file_format == "csv"

    assert spark.read.options_value == {
        "header": "true",
        "inferSchema": "false",
    }

    assert spark.read.path == "/Volumes/raw/orders"
