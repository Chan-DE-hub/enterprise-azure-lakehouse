"""Tests for the Silver processing strategy factory."""

from enterprise_lakehouse.common.metadata.models import (
    ProcessingMetadata,
    SilverProcessingStrategy,
)
from enterprise_lakehouse.silver.metadata import ProcessingStrategyFactory


def test_factory_returns_configured_append_strategy() -> None:
    """The factory should preserve append processing semantics."""
    strategy = ProcessingStrategyFactory().build(
        ProcessingMetadata(
            strategy=SilverProcessingStrategy.APPEND,
        ),
    )

    assert strategy is SilverProcessingStrategy.APPEND


def test_factory_returns_configured_auto_cdc_strategy() -> None:
    """The factory should preserve AUTO CDC processing semantics."""
    strategy = ProcessingStrategyFactory().build(
        ProcessingMetadata(
            strategy=SilverProcessingStrategy.AUTO_CDC,
        ),
    )

    assert strategy is SilverProcessingStrategy.AUTO_CDC
