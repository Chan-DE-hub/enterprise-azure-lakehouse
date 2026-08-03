"""Tests for the Bronze streaming Delta writer."""

from typing import Any

import pytest

from enterprise_lakehouse.bronze.writers.bronze_streaming_writer import (
    BronzeStreamingWriter,
)


class FakeStreamingQuery:
    """Fake streaming query returned by toTable."""

    def __init__(self) -> None:
        self.awaited = False

    def awaitTermination(self) -> None:
        """Record that the query was awaited."""
        self.awaited = True


class FakeDataStreamWriter:
    """Test double for Spark's DataStreamWriter."""

    def __init__(self) -> None:
        self.format_value: str | None = None
        self.output_mode_value: str | None = None
        self.options_value: dict[str, Any] = {}
        self.trigger_value: dict[str, Any] = {}
        self.table_name: str | None = None
        self.query = FakeStreamingQuery()

    def format(self, value: str) -> "FakeDataStreamWriter":
        self.format_value = value
        return self

    def outputMode(self, value: str) -> "FakeDataStreamWriter":
        self.output_mode_value = value
        return self

    def options(self, **options: Any) -> "FakeDataStreamWriter":
        self.options_value = options
        return self

    def trigger(self, **trigger: Any) -> "FakeDataStreamWriter":
        self.trigger_value = trigger
        return self

    def toTable(self, table_name: str) -> FakeStreamingQuery:
        self.table_name = table_name
        return self.query


class FakeStreamingDataFrame:
    """Fake streaming DataFrame."""

    def __init__(self) -> None:
        self.writeStream = FakeDataStreamWriter()


def test_streaming_writer_writes_available_now_to_delta_table() -> None:
    """The writer should configure and await an available-now stream."""
    dataframe = FakeStreamingDataFrame()
    writer = BronzeStreamingWriter()

    writer.write(
        dataframe=dataframe,
        table_name="workspace.bronze.bronze_orders",
        mode="append",
        options={
            "checkpointLocation": "/Volumes/workspace/checkpoints/orders",
            "trigger": "availableNow",
        },
    )

    assert dataframe.writeStream.format_value == "delta"
    assert dataframe.writeStream.output_mode_value == "append"
    assert dataframe.writeStream.options_value == {
        "checkpointLocation": "/Volumes/workspace/checkpoints/orders",
    }
    assert dataframe.writeStream.trigger_value == {
        "availableNow": True,
    }
    assert dataframe.writeStream.table_name == "workspace.bronze.bronze_orders"
    assert dataframe.writeStream.query.awaited is True


def test_streaming_writer_requires_checkpoint_location() -> None:
    """The writer should require a checkpoint location."""
    dataframe = FakeStreamingDataFrame()
    writer = BronzeStreamingWriter()

    with pytest.raises(
        ValueError,
        match="checkpointLocation is required",
    ):
        writer.write(
            dataframe=dataframe,
            table_name="workspace.bronze.bronze_orders",
            mode="append",
            options={
                "trigger": "availableNow",
            },
        )
