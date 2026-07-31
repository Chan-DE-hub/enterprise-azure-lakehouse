"""Tests for loader composition."""

from enterprise_lakehouse.bronze.readers.databricks_auto_loader import (
    DatabricksAutoLoader,
)
from enterprise_lakehouse.bronze.readers.loader_composer import LoaderComposer
from enterprise_lakehouse.bronze.readers.spark_file_loader import SparkFileLoader


class FakeSpark:
    """Fake Spark session."""


def test_returns_batch_loader() -> None:
    """Batch ingestion should use SparkFileLoader."""
    composer = LoaderComposer(spark=FakeSpark())

    loader = composer.compose(ingestion_mode="batch")

    assert isinstance(loader, SparkFileLoader)


def test_returns_streaming_loader() -> None:
    """Streaming ingestion should use DatabricksAutoLoader."""
    composer = LoaderComposer(spark=FakeSpark())

    loader = composer.compose(ingestion_mode="streaming")

    assert isinstance(loader, DatabricksAutoLoader)
