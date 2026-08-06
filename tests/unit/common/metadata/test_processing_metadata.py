"""Tests for Silver processing metadata."""

from enterprise_lakehouse.common.metadata import (
    SilverProcessingStrategy,
)
from enterprise_lakehouse.common.metadata.models import (
    ProcessingMetadata,
)


def test_processing_metadata_defaults_to_append() -> None:
    """Append should be the default Silver strategy."""
    metadata = ProcessingMetadata()

    assert metadata.strategy is SilverProcessingStrategy.APPEND


def test_processing_metadata_supports_auto_cdc() -> None:
    """AUTO CDC should be configurable."""
    metadata = ProcessingMetadata(
        strategy=SilverProcessingStrategy.AUTO_CDC,
    )

    assert metadata.strategy is SilverProcessingStrategy.AUTO_CDC
