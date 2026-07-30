"""Tests for the Bronze ingestion engine."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from enterprise_lakehouse.bronze.engine import IngestionEngine
from enterprise_lakehouse.bronze.models import PipelineContext
from enterprise_lakehouse.bronze.readers import BaseReader


class FakeReader(BaseReader):
    """Minimal reader used to test engine dependency wiring."""

    @property
    def source_type(self) -> str:
        return "fake"

    def read(self, *, options: dict[str, Any]) -> Any:
        return options


def create_context() -> PipelineContext:
    """Create a reusable PipelineContext for engine tests."""
    return PipelineContext(
        pipeline_name="bronze_orders",
        run_id=uuid4(),
        environment="dev",
        started_at=datetime.now(UTC),
    )


def test_engine_stores_reader_dependency() -> None:
    """The engine should preserve its injected reader dependency."""
    reader = FakeReader()

    engine = IngestionEngine(reader)

    assert engine.reader is reader


def test_run_accepts_pipeline_context() -> None:
    """The skeleton run method should accept a PipelineContext."""
    engine = IngestionEngine(FakeReader())
    context = create_context()

    with pytest.raises(
        NotImplementedError,
        match="Bronze ingestion orchestration is not implemented yet",
    ):
        engine.run(context)
