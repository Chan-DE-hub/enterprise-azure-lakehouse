"""Factory for Silver deduplication rules."""

from enterprise_lakehouse.common.metadata.models import SourceMetadata
from enterprise_lakehouse.silver.models import DeduplicationRule


class DeduplicationRuleFactory:
    """Build runtime deduplication rules from source metadata."""

    def __init__(
        self,
        *,
        watermark_delay: str,
    ) -> None:
        """Initialize the factory with a bounded-state watermark delay."""
        self._watermark_delay = watermark_delay

    def build(
        self,
        metadata: SourceMetadata,
    ) -> DeduplicationRule:
        """Build a streaming deduplication rule from source metadata."""
        if not metadata.primary_keys:
            raise ValueError(
                "primary_keys are required for deduplication.",
            )

        if metadata.watermark_column is None:
            raise ValueError(
                "watermark_column is required for streaming deduplication.",
            )

        return DeduplicationRule(
            keys=metadata.primary_keys,
            event_time_column=metadata.watermark_column,
            watermark_delay=self._watermark_delay,
        )
