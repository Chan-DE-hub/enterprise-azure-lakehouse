"""Factory for resolving Silver processing strategies."""

from enterprise_lakehouse.common.metadata.models import (
    ProcessingMetadata,
    SilverProcessingStrategy,
)


class ProcessingStrategyFactory:
    """Resolve the configured Silver processing strategy."""

    def build(
        self,
        metadata: ProcessingMetadata,
    ) -> SilverProcessingStrategy:
        """Return the configured Silver processing strategy."""
        return metadata.strategy
