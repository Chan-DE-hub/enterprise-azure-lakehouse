"""Immutable configuration for Bronze Delta writes."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True, slots=True)
class BronzeWriteConfig:
    """Configuration describing how Bronze data should be written."""

    table_name: str
    mode: str
    options: Mapping[str, Any] = field(default_factory=dict)
    partition_columns: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate and freeze the write configuration."""
        if not self.table_name.strip():
            raise ValueError("Table name must not be empty")

        if not self.mode.strip():
            raise ValueError("Write mode must not be empty")

        object.__setattr__(
            self,
            "options",
            MappingProxyType(dict(self.options)),
        )
