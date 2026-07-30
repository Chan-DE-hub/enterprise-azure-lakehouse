"""Domain model describing a Bronze source."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any


@dataclass(frozen=True, slots=True)
class SourceMetadata:
    """Immutable configuration describing a Bronze source."""

    source_name: str
    source_type: str
    load_mode: str
    primary_keys: tuple[str, ...]
    watermark_column: str | None
    event_timestamp_column: str | None
    options: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Convert mutable mappings into read-only mappings."""
        object.__setattr__(
            self,
            "options",
            MappingProxyType(dict(self.options)),
        )
