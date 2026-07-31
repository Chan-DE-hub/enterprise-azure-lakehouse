"""Compose the appropriate file loader based on ingestion mode."""

from typing import Any

from enterprise_lakehouse.bronze.readers.databricks_auto_loader import (
    DatabricksAutoLoader,
)
from enterprise_lakehouse.bronze.readers.file_loader import FileLoader
from enterprise_lakehouse.bronze.readers.spark_file_loader import SparkFileLoader


class LoaderComposer:
    """Compose the appropriate file loader."""

    def __init__(self, *, spark: Any) -> None:
        """Initialize the composer with a Spark-compatible session."""
        self._spark = spark

    def compose(self, *, ingestion_mode: str) -> FileLoader:
        """Return the appropriate loader for the requested ingestion mode."""
        if ingestion_mode == "batch":
            return SparkFileLoader(spark=self._spark)

        if ingestion_mode == "streaming":
            return DatabricksAutoLoader(spark=self._spark)

        raise ValueError(f"Unsupported ingestion mode: {ingestion_mode}")
