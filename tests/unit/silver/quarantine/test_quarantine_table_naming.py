"""Tests for Silver quarantine table naming."""

from enterprise_lakehouse.silver.quarantine import build_quarantine_table_name


def test_build_quarantine_table_name_appends_suffix() -> None:
    """The quarantine table name should derive from the Silver table name."""
    result = build_quarantine_table_name("silver_orders")

    assert result == "silver_orders_quarantine"
