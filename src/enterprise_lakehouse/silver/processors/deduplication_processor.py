"""Generic Silver streaming deduplication processor."""

from pyspark.sql import DataFrame

from enterprise_lakehouse.silver.models import DeduplicationRule


class DeduplicationProcessor:
    """Apply bounded streaming deduplication using event-time state."""

    def __init__(
        self,
        *,
        rule: DeduplicationRule,
    ) -> None:
        """Initialize the processor with one immutable rule."""
        self._rule = rule

    def process(self, dataframe: DataFrame) -> DataFrame:
        """Apply watermarking and deduplicate within the watermark."""
        watermarked_dataframe = dataframe.withWatermark(
            self._rule.event_time_column,
            self._rule.watermark_delay,
        )

        return watermarked_dataframe.dropDuplicatesWithinWatermark(
            list(self._rule.keys),
        )
