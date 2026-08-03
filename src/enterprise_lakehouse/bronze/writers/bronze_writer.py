"""Contracts for writing Bronze data."""

from collections.abc import Mapping
from typing import Any, Protocol


class BronzeWriter(Protocol):
    """Contract implemented by Bronze write adapters."""

    def write(
        self,
        *,
        dataframe: Any,
        table_name: str,
        mode: str,
        options: Mapping[str, Any],
    ) -> None:
        """Write a DataFrame to a Bronze target."""
        ...
