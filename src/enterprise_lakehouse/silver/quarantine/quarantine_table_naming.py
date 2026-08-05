"""Naming helpers for Silver quarantine datasets."""


def build_quarantine_table_name(silver_table_name: str) -> str:
    """Return the deterministic quarantine table name for a Silver table."""
    return f"{silver_table_name}_quarantine"
