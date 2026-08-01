"""Tests for the Bronze Delta writer."""

from typing import Any

import pytest

from enterprise_lakehouse.bronze.writers.bronze_delta_writer import (
    BronzeDeltaWriter,
)


class FakeDataFrameWriter:
    """Test double for Spark's DataFrameWriter."""

    def __init__(self) -> None:
        """Initialize recorded writer configuration."""
        self.format_value: str | None = None
        self.mode_value: str | None = None
        self.options_value: dict[str, Any] = {}
        self.table_name: str | None = None

    def format(self, value: str) -> "FakeDataFrameWriter":
        """Record the requested output format."""
        self.format_value = value
        return self

    def mode(self, value: str) -> "FakeDataFrameWriter":
        """Record the requested write mode."""
        self.mode_value = value
        return self

    def options(self, **options: Any) -> "FakeDataFrameWriter":
        """Record the supplied writer options."""
        self.options_value = options
        return self

    def saveAsTable(self, table_name: str) -> None:
        """Record the destination table name."""
        self.table_name = table_name


class FakeDataFrame:
    """Test double exposing a Spark-compatible write property."""

    def __init__(self) -> None:
        """Initialize the fake DataFrame writer."""
        self.write = FakeDataFrameWriter()


def test_bronze_delta_writer_writes_to_delta_table() -> None:
    """The writer must configure and execute a Delta table write."""
    dataframe = FakeDataFrame()
    writer = BronzeDeltaWriter()

    writer.write(
        dataframe=dataframe,
        table_name="dev_sales_lakehouse.bronze.sales_orders",
        mode="append",
        options={
            "mergeSchema": "true",
        },
    )

    assert dataframe.write.format_value == "delta"
    assert dataframe.write.mode_value == "append"
    assert dataframe.write.options_value == {
        "mergeSchema": "true",
    }
    assert dataframe.write.table_name == "dev_sales_lakehouse.bronze.sales_orders"


def test_bronze_delta_writer_rejects_unsupported_mode() -> None:
    """The writer must reject unsupported write modes."""
    dataframe = FakeDataFrame()
    writer = BronzeDeltaWriter()

    with pytest.raises(
        ValueError,
        match="Unsupported write mode: overwrite_table",
    ):
        writer.write(
            dataframe=dataframe,
            table_name="dev_sales_lakehouse.bronze.sales_orders",
            mode="overwrite_table",
            options={},
        )


def test_bronze_delta_writer_rejects_blank_table_name() -> None:
    """The writer must reject blank destination table names."""
    dataframe = FakeDataFrame()
    writer = BronzeDeltaWriter()

    with pytest.raises(
        ValueError,
        match="Table name must not be empty",
    ):
        writer.write(
            dataframe=dataframe,
            table_name="",
            mode="append",
            options={},
        )
