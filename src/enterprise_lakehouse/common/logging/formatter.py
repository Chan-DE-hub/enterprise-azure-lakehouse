"""JSON log formatter for structured application logging."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any, Final

_STANDARD_LOG_RECORD_ATTRIBUTES: Final[frozenset[str]] = frozenset(
    {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "taskName",
        "thread",
        "threadName",
    }
)


class JsonFormatter(logging.Formatter):
    """Format log records as one-line JSON documents."""

    def format(self, record: logging.LogRecord) -> str:
        """Convert a log record into a serialized JSON object."""
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                tz=UTC,
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        payload.update(self._extract_extra_fields(record))

        if record.exc_info is not None:
            payload["exception"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            payload["stack_trace"] = self.formatStack(record.stack_info)

        return json.dumps(
            payload,
            default=str,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    @staticmethod
    def _extract_extra_fields(record: logging.LogRecord) -> dict[str, Any]:
        """Return application-specific fields attached to the log record."""
        return {
            key: value
            for key, value in record.__dict__.items()
            if key not in _STANDARD_LOG_RECORD_ATTRIBUTES and not key.startswith("_")
        }
