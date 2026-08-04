"""Silver pipeline orchestration."""

from collections.abc import Iterable

from pyspark.sql import DataFrame

from enterprise_lakehouse.silver.processors import Processor


class SilverPipeline:
    """Apply ordered Silver processors to a source DataFrame."""

    def __init__(
        self,
        *,
        processors: Iterable[Processor],
    ) -> None:
        """Initialize the pipeline with ordered processors."""
        self._processors = tuple(processors)

    def run(
        self,
        dataframe: DataFrame,
    ) -> DataFrame:
        """Apply each configured processor sequentially."""
        result = dataframe

        for processor in self._processors:
            result = processor.process(result)

        return result
