"""Spark implementation of the file loader contract."""

from collections.abc import Mapping
from typing import Any


class SparkFileLoader:
    """Load batch file data using a Spark-compatible session."""

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
        """Load file data using Spark's batch DataFrameReader."""
        return self._spark.read.format(file_format).options(**dict(options)).load(path)
