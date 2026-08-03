"""Bronze streaming Delta table writer."""

from collections.abc import Mapping
from typing import Any


class BronzeStreamingWriter:
    """Write streaming DataFrames to Bronze Delta tables."""

    def write(
        self,
        *,
        dataframe: Any,
        table_name: str,
        mode: str,
        options: Mapping[str, Any],
    ) -> None:
        """Write a streaming DataFrame to a managed Delta table."""
        if not table_name.strip():
            raise ValueError("Table name must not be empty")

        if mode != "append":
            raise ValueError(
                f"Unsupported streaming output mode: {mode}",
            )

        writer_options = dict(options)

        checkpoint_location = writer_options.pop(
            "checkpointLocation",
            None,
        )

        if not checkpoint_location:
            raise ValueError(
                "checkpointLocation is required",
            )

        trigger = writer_options.pop(
            "trigger",
            "availableNow",
        )

        stream_writer = (
            dataframe.writeStream.format("delta")
            .outputMode(mode)
            .options(
                checkpointLocation=checkpoint_location,
                **writer_options,
            )
        )

        if trigger == "availableNow":
            stream_writer = stream_writer.trigger(
                availableNow=True,
            )
        else:
            stream_writer = stream_writer.trigger(
                processingTime=trigger,
            )

        query = stream_writer.toTable(table_name)
        query.awaitTermination()
