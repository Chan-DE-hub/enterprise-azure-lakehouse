"""Tests for the structured JSON formatter."""

from __future__ import annotations

import json
import logging
from typing import Any

from enterprise_lakehouse.common.logging import JsonFormatter


def _build_record(
    message: str,
    *,
    extra: dict[str, Any] | None = None,
) -> logging.LogRecord:
    record = logging.LogRecord(
        name="enterprise_lakehouse.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg=message,
        args=(),
        exc_info=None,
    )

    for key, value in (extra or {}).items():
        setattr(record, key, value)

    return record


def test_json_formatter_contains_required_fields() -> None:
    formatter = JsonFormatter()
    record = _build_record("Pipeline completed")

    payload = json.loads(formatter.format(record))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "enterprise_lakehouse.test"
    assert payload["message"] == "Pipeline completed"
    assert "timestamp" in payload


def test_json_formatter_includes_structured_fields() -> None:
    formatter = JsonFormatter()
    record = _build_record(
        "Records processed",
        extra={
            "pipeline_name": "bronze_orders",
            "record_count": 125,
        },
    )

    payload = json.loads(formatter.format(record))

    assert payload["pipeline_name"] == "bronze_orders"
    assert payload["record_count"] == 125
