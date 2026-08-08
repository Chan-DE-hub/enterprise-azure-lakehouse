"""Tests for pipeline operational health evaluation."""

from datetime import UTC, datetime, timedelta

from enterprise_lakehouse.monitoring.health import (
    HealthStatus,
    PipelineHealthEvaluator,
)
from enterprise_lakehouse.monitoring.models import PipelineUpdate


def build_update(
    *,
    final_status: str,
    completed_at: datetime | None,
) -> PipelineUpdate:
    """Build representative pipeline update evidence."""
    return PipelineUpdate(
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
        update_id="update-1",
        started_at=datetime(
            2026,
            8,
            8,
            10,
            0,
            tzinfo=UTC,
        ),
        completed_at=completed_at,
        final_status=final_status,
        duration_seconds=60.0,
        error_message=None,
    )


def test_evaluator_returns_healthy_when_success_is_within_sla() -> None:
    """Recent successful execution should be healthy."""
    observed_at = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    update = build_update(
        final_status="COMPLETED",
        completed_at=observed_at - timedelta(minutes=30),
    )

    health = PipelineHealthEvaluator().evaluate(
        updates=(update,),
        observed_at=observed_at,
        sla_minutes=60,
    )

    assert health.status is HealthStatus.HEALTHY
    assert health.minutes_since_success == 30.0


def test_evaluator_returns_degraded_when_success_exceeds_sla() -> None:
    """Stale successful execution should be degraded."""
    observed_at = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    update = build_update(
        final_status="COMPLETED",
        completed_at=observed_at - timedelta(minutes=90),
    )

    health = PipelineHealthEvaluator().evaluate(
        updates=(update,),
        observed_at=observed_at,
        sla_minutes=60,
    )

    assert health.status is HealthStatus.DEGRADED
    assert health.minutes_since_success == 90.0


def test_evaluator_returns_unhealthy_when_latest_update_failed() -> None:
    """A latest failed update should make the pipeline unhealthy."""
    observed_at = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    successful_update = build_update(
        final_status="COMPLETED",
        completed_at=observed_at - timedelta(minutes=20),
    )

    failed_update = PipelineUpdate(
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
        update_id="update-2",
        started_at=observed_at - timedelta(minutes=10),
        completed_at=observed_at - timedelta(minutes=5),
        final_status="FAILED",
        duration_seconds=300.0,
        error_message="pipeline failed",
    )

    health = PipelineHealthEvaluator().evaluate(
        updates=(
            successful_update,
            failed_update,
        ),
        observed_at=observed_at,
        sla_minutes=60,
    )

    assert health.status is HealthStatus.UNHEALTHY
    assert health.last_success_at == successful_update.completed_at


def test_evaluator_returns_unknown_without_successful_updates() -> None:
    """Missing successful execution evidence should produce unknown freshness."""
    observed_at = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    health = PipelineHealthEvaluator().evaluate(
        updates=(),
        observed_at=observed_at,
        sla_minutes=60,
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
    )

    assert health.status is HealthStatus.UNKNOWN
    assert health.last_success_at is None
    assert health.minutes_since_success is None


def test_evaluator_normalizes_naive_runtime_timestamps_to_utc() -> None:
    """Naive Spark timestamps should be interpreted consistently as UTC."""
    observed_at = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    update = PipelineUpdate(
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
        update_id="update-1",
        started_at=datetime(
            2026,
            8,
            8,
            11,
            20,
        ),
        completed_at=datetime(
            2026,
            8,
            8,
            11,
            30,
        ),
        final_status="COMPLETED",
        duration_seconds=600.0,
        error_message=None,
    )

    health = PipelineHealthEvaluator().evaluate(
        updates=(update,),
        observed_at=observed_at,
        sla_minutes=60,
    )

    assert health.status is HealthStatus.HEALTHY
    assert health.minutes_since_success == 30.0
    assert health.last_success_at == datetime(
        2026,
        8,
        8,
        11,
        30,
        tzinfo=UTC,
    )
