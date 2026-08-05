"""Tests for Silver deduplication rules."""

import pytest
from pydantic import ValidationError

from enterprise_lakehouse.silver.models import DeduplicationRule


def test_deduplication_rule_stores_streaming_configuration() -> None:
    """The rule should preserve deterministic streaming deduplication settings."""
    rule = DeduplicationRule(
        keys=("order_id",),
        event_time_column="modified_at",
        watermark_delay="10 minutes",
    )

    assert rule.keys == ("order_id",)
    assert rule.event_time_column == "modified_at"
    assert rule.watermark_delay == "10 minutes"


def test_deduplication_rule_requires_at_least_one_key() -> None:
    """Deduplication must have at least one identifying key."""
    with pytest.raises(
        ValidationError,
        match="keys",
    ):
        DeduplicationRule(
            keys=(),
            event_time_column="modified_at",
            watermark_delay="10 minutes",
        )


def test_deduplication_rule_is_immutable() -> None:
    """Deduplication configuration should not change after creation."""
    rule = DeduplicationRule(
        keys=("order_id",),
        event_time_column="modified_at",
        watermark_delay="10 minutes",
    )

    with pytest.raises(ValidationError):
        rule.watermark_delay = "1 hour"
