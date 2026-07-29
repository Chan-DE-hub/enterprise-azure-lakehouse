"""Logger construction and structured context handling."""

from __future__ import annotations

import logging
import sys
from collections.abc import Mapping, MutableMapping
from typing import Any, Final

from enterprise_lakehouse.common.logging.formatter import JsonFormatter

_DEFAULT_LOG_LEVEL: Final[int] = logging.INFO


class StructuredLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter that attaches reusable structured context."""

    def process(
        self,
        msg: object,
        kwargs: MutableMapping[str, Any],
    ) -> tuple[object, MutableMapping[str, Any]]:
        """Merge adapter context with per-call structured fields."""
        call_extra = kwargs.get("extra", {})

        if call_extra is None:
            call_extra = {}

        if not isinstance(call_extra, Mapping):
            raise TypeError("The logging 'extra' argument must be a mapping.")

        adapter_extra: Mapping[str, Any] = self.extra or {}

        kwargs["extra"] = {
            **adapter_extra,
            **call_extra,
        }

        return msg, kwargs


def configure_logging(
    *,
    level: int = _DEFAULT_LOG_LEVEL,
) -> None:
    """Configure the root application logger for JSON output."""
    root_logger = logging.getLogger()

    root_logger.handlers.clear()
    root_logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(JsonFormatter())

    root_logger.addHandler(handler)


def get_logger(
    name: str,
    *,
    context: Mapping[str, Any] | None = None,
) -> StructuredLoggerAdapter:
    """Return a logger with optional persistent structured context."""
    logger = logging.getLogger(name)

    return StructuredLoggerAdapter(
        logger,
        dict(context or {}),
    )
