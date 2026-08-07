"""Reusable Silver framework definition."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from enterprise_lakehouse.common.metadata.models import (
    SilverProcessingStrategy,
)


@dataclass(frozen=True, slots=True)
class SilverDefinition:
    """Immutable configuration composed for one Silver pipeline."""

    source_table: str
    silver_table: str
    quarantine_table: str
    processors: tuple[Any, ...]
    expectation_rules: Mapping[str, str]
    quarantine_predicate: str
    processing_strategy: SilverProcessingStrategy

    def __post_init__(self) -> None:
        """Protect mutable mappings after construction."""
        object.__setattr__(
            self,
            "expectation_rules",
            MappingProxyType(
                dict(self.expectation_rules),
            ),
        )
