"""Silver processor contract."""

from typing import Protocol

from pyspark.sql import DataFrame


class Processor(Protocol):
    """Contract implemented by all Silver processors."""

    def process(
        self,
        dataframe: DataFrame,
    ) -> DataFrame:
        """Transform a Spark DataFrame."""
        ...
