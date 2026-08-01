"""Tests for Bronze write configuration."""

import pytest

from enterprise_lakehouse.bronze.models.bronze_write_config import (
    BronzeWriteConfig,
)


def test_bronze_write_config_stores_write_settings() -> None:
    """The configuration should preserve Bronze write settings."""
    config = BronzeWriteConfig(
        table_name="dev_sales_lakehouse.bronze.sales_orders",
        mode="append",
        options={
            "mergeSchema": "true",
        },
        partition_columns=("ingestion_date",),
    )

    assert config.table_name == "dev_sales_lakehouse.bronze.sales_orders"
    assert config.mode == "append"
    assert config.options == {
        "mergeSchema": "true",
    }
    assert config.partition_columns == ("ingestion_date",)


def test_bronze_write_config_options_are_read_only() -> None:
    """Write options should reject mutation after construction."""
    config = BronzeWriteConfig(
        table_name="dev_sales_lakehouse.bronze.sales_orders",
        mode="append",
        options={"mergeSchema": "true"},
    )

    with pytest.raises(TypeError):
        config.options["mergeSchema"] = "false"  # type: ignore[index]


def test_bronze_write_config_rejects_blank_table_name() -> None:
    """Blank table names should not be accepted."""
    with pytest.raises(
        ValueError,
        match="Table name must not be empty",
    ):
        BronzeWriteConfig(
            table_name="",
            mode="append",
        )


def test_bronze_write_config_rejects_blank_mode() -> None:
    """Blank write modes should not be accepted."""
    with pytest.raises(
        ValueError,
        match="Write mode must not be empty",
    ):
        BronzeWriteConfig(
            table_name="dev_sales_lakehouse.bronze.sales_orders",
            mode="",
        )
