"""Tests for the generic Silver deduplication processor."""

from unittest.mock import Mock, call

from enterprise_lakehouse.silver.models import DeduplicationRule
from enterprise_lakehouse.silver.processors import DeduplicationProcessor


def test_processor_applies_watermark_and_streaming_deduplication() -> None:
    """The processor should apply bounded streaming deduplication."""
    source_dataframe = Mock(name="source_dataframe")
    watermarked_dataframe = Mock(name="watermarked_dataframe")
    deduplicated_dataframe = Mock(name="deduplicated_dataframe")

    source_dataframe.withWatermark.return_value = watermarked_dataframe
    watermarked_dataframe.dropDuplicatesWithinWatermark.return_value = deduplicated_dataframe

    rule = DeduplicationRule(
        keys=("order_id",),
        event_time_column="modified_at",
        watermark_delay="10 minutes",
    )

    processor = DeduplicationProcessor(rule=rule)

    result = processor.process(source_dataframe)

    assert result is deduplicated_dataframe

    assert source_dataframe.withWatermark.call_args_list == [
        call("modified_at", "10 minutes"),
    ]
    assert watermarked_dataframe.dropDuplicatesWithinWatermark.call_args_list == [
        call(["order_id"]),
    ]


def test_processor_supports_composite_keys() -> None:
    """The processor should deduplicate using all configured keys."""
    dataframe = Mock()
    dataframe.withWatermark.return_value = dataframe
    dataframe.dropDuplicatesWithinWatermark.return_value = dataframe

    processor = DeduplicationProcessor(
        rule=DeduplicationRule(
            keys=("order_id", "line_number"),
            event_time_column="modified_at",
            watermark_delay="10 minutes",
        ),
    )

    result = processor.process(dataframe)

    assert result is dataframe
    dataframe.dropDuplicatesWithinWatermark.assert_called_once_with(
        ["order_id", "line_number"],
    )
