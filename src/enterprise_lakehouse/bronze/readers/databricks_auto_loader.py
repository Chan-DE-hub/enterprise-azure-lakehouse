"""Databricks Auto Loader implementation."""

from collections.abc import Mapping
from typing import Any


class DatabricksAutoLoader:
    """Load streaming file data using Databricks Auto Loader."""

    def __init__(self, *, spark: Any) -> None:
        """Initialize the loader with a Spark-compatible session."""
        self._spark = spark

    def __call__(
        self,
        *,
        path: str,
        file_format: str,
        options: Mapping[str, Any],
    ) -> Any:
        """Load streaming file data using the cloudFiles source."""
        auto_loader_options = dict(options)
        auto_loader_options["cloudFiles.format"] = file_format

        return self._spark.readStream.format("cloudFiles").options(**auto_loader_options).load(path)
