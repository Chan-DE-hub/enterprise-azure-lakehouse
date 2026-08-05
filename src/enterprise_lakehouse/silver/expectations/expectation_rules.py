"""Grouped Lakeflow expectation rules."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ExpectationRules:
    """Expectation constraints grouped by their execution policy."""

    retain: dict[str, str] = field(default_factory=dict)
    drop: dict[str, str] = field(default_factory=dict)
