"""Tests for structured logger construction."""

from __future__ import annotations

import logging

import pytest

from enterprise_lakehouse.common.logging import (
    StructuredLoggerAdapter,
    get_logger,
)


def test_get_logger_returns_structured_adapter() -> None:
    logger = get_logger(
        "enterprise_lakehouse.test",
        context={"environment": "dev"},
    )

    assert isinstance(logger, StructuredLoggerAdapter)
    assert logger.extra == {"environment": "dev"}


def test_adapter_merges_persistent_and_per_call_context(
    caplog: pytest.LogCaptureFixture,
) -> None:
    logger = get_logger(
        "enterprise_lakehouse.test",
        context={
            "environment": "dev",
            "pipeline_name": "bronze_orders",
        },
    )

    with caplog.at_level(logging.INFO):
        logger.info(
            "Pipeline completed",
            extra={
                "record_count": 250,
                "pipeline_name": "bronze_customers",
            },
        )

    record = caplog.records[0]

    assert record.environment == "dev"
    assert record.pipeline_name == "bronze_customers"
    assert record.record_count == 250


def test_adapter_rejects_non_mapping_extra() -> None:
    logger = get_logger("enterprise_lakehouse.test")

    with pytest.raises(
        TypeError,
        match="must be a mapping",
    ):
        logger.process(
            "Invalid context",
            {
                "extra": "not-a-mapping",
            },
        )
