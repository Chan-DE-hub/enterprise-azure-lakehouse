"""Bronze Delta table writer."""

from collections.abc import Mapping
from typing import Any

SUPPORTED_WRITE_MODES = frozenset(
    {
        "append",
        "overwrite",
        "error",
        "errorifexists",
        "ignore",
    }
)


class BronzeDeltaWriter:
    """Write batch DataFrames to Bronze Delta tables."""

    def write(
        self,
        *,
        dataframe: Any,
        table_name: str,
        mode: str,
        options: Mapping[str, Any],
    ) -> None:
        """Write a DataFrame to a managed or external Delta table."""
        if not table_name.strip():
            raise ValueError("Table name must not be empty")

        if mode not in SUPPORTED_WRITE_MODES:
            raise ValueError(f"Unsupported write mode: {mode}")

        (
            dataframe.write.format("delta")
            .mode(mode)
            .options(**dict(options))
            .saveAsTable(table_name)
        )
