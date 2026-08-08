"""Tests for operational monitoring health models."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from enterprise_lakehouse.monitoring.health import (
    HealthStatus,
    PipelineHealth,
)


def test_pipeline_health_stores_operational_state() -> None:
    """Pipeline health should preserve actionable operational evidence."""
    observed_at = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    health = PipelineHealth(
        pipeline_id="9b1fffe2-cdfb-4ce5-934f-de9474f51131",
        pipeline_name="silver_orders",
        status=HealthStatus.HEALTHY,
        observed_at=observed_at,
        last_success_at=observed_at,
        minutes_since_success=0.0,
        sla_minutes=60,
    )

    assert health.pipeline_name == "silver_orders"
    assert health.status is HealthStatus.HEALTHY
    assert health.last_success_at == observed_at
    assert health.minutes_since_success == 0.0
    assert health.sla_minutes == 60


def test_pipeline_health_is_immutable() -> None:
    """Operational health evidence must be immutable after creation."""
    health = PipelineHealth(
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
        status=HealthStatus.UNKNOWN,
        observed_at=datetime(
            2026,
            8,
            8,
            tzinfo=UTC,
        ),
        last_success_at=None,
        minutes_since_success=None,
        sla_minutes=60,
    )

    with pytest.raises(ValidationError):
        health.status = HealthStatus.HEALTHY  # type: ignore[misc]


def test_pipeline_health_rejects_negative_freshness() -> None:
    """Freshness age cannot be negative."""
    with pytest.raises(ValidationError):
        PipelineHealth(
            pipeline_id="pipeline-1",
            pipeline_name="silver_orders",
            status=HealthStatus.HEALTHY,
            observed_at=datetime(
                2026,
                8,
                8,
                tzinfo=UTC,
            ),
            last_success_at=datetime(
                2026,
                8,
                8,
                tzinfo=UTC,
            ),
            minutes_since_success=-1.0,
            sla_minutes=60,
        )
