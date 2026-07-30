"""Tests for the PipelineContext model."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from enterprise_lakehouse.bronze.models import PipelineContext


def test_pipeline_context_stores_values() -> None:
    """PipelineContext should preserve the values passed to it."""

    run_id = uuid4()
    started_at = datetime.now(UTC)

    context = PipelineContext(
        pipeline_name="bronze_orders",
        run_id=run_id,
        environment="dev",
        started_at=started_at,
    )

    assert context.pipeline_name == "bronze_orders"
    assert context.run_id == run_id
    assert context.environment == "dev"
    assert context.started_at == started_at


def test_pipeline_context_is_immutable() -> None:
    """PipelineContext should be immutable after creation."""

    context = PipelineContext(
        pipeline_name="bronze_orders",
        run_id=uuid4(),
        environment="dev",
        started_at=datetime.now(UTC),
    )

    with pytest.raises(FrozenInstanceError):
        context.environment = "prod"  # type: ignore[misc]
