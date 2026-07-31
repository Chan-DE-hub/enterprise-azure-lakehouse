"""Tests for the Databricks Auto Loader implementation."""

from typing import Any

from enterprise_lakehouse.bronze.readers.databricks_auto_loader import (
    DatabricksAutoLoader,
)


class FakeDataStreamReader:
    """Test double for Spark's DataStreamReader."""

    def __init__(self) -> None:
        """Initialize recorded streaming reader configuration."""
        self.source_format: str | None = None
        self.options_value: dict[str, Any] = {}
        self.path: str | None = None

    def format(self, source: str) -> "FakeDataStreamReader":
        """Record the requested streaming source format."""
        self.source_format = source
        return self

    def options(self, **options: Any) -> "FakeDataStreamReader":
        """Record the requested streaming reader options."""
        self.options_value = options
        return self

    def load(self, path: str) -> object:
        """Record the source path and return fake streaming data."""
        self.path = path
        return {"streaming": True}


class FakeSparkSession:
    """Test double exposing a Spark-compatible readStream property."""

    def __init__(self) -> None:
        """Initialize the fake streaming reader."""
        self.readStream = FakeDataStreamReader()


def test_databricks_auto_loader_configures_cloud_files_source() -> None:
    """The loader must configure and invoke Databricks Auto Loader."""
    spark = FakeSparkSession()
    loader = DatabricksAutoLoader(spark=spark)

    result = loader(
        path="/Volumes/raw/orders",
        file_format="json",
        options={
            "cloudFiles.schemaLocation": "/Volumes/checkpoints/orders/schema",
            "cloudFiles.schemaEvolutionMode": "addNewColumns",
            "rescuedDataColumn": "_rescued_data",
        },
    )

    assert result == {"streaming": True}
    assert spark.readStream.source_format == "cloudFiles"
    assert spark.readStream.options_value == {
        "cloudFiles.format": "json",
        "cloudFiles.schemaLocation": "/Volumes/checkpoints/orders/schema",
        "cloudFiles.schemaEvolutionMode": "addNewColumns",
        "rescuedDataColumn": "_rescued_data",
    }
    assert spark.readStream.path == "/Volumes/raw/orders"
