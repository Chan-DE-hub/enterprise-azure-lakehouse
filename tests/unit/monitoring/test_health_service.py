"""Tests for pipeline health orchestration."""

from datetime import UTC, datetime
from unittest.mock import Mock

from enterprise_lakehouse.monitoring.health import (
    HealthStatus,
    PipelineHealth,
    PipelineHealthService,
)


def test_health_service_loads_updates_and_evaluates_health() -> None:
    """The service should connect monitoring evidence to health evaluation."""
    repository = Mock()
    evaluator = Mock()

    observed_at = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    completed_at = datetime(
        2026,
        8,
        8,
        11,
        45,
        tzinfo=UTC,
    )

    row = Mock()
    row.asDict.return_value = {
        "pipeline_id": "pipeline-1",
        "pipeline_name": "silver_orders",
        "update_id": "update-1",
        "started_at": datetime(
            2026,
            8,
            8,
            11,
            44,
            tzinfo=UTC,
        ),
        "completed_at": completed_at,
        "final_status": "COMPLETED",
        "duration_seconds": 60.0,
        "error_message": None,
    }

    update_dataframe = Mock(name="update_dataframe")
    update_dataframe.collect.return_value = [
        row,
    ]

    repository.pipeline_updates.return_value = update_dataframe

    expected_health = PipelineHealth(
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
        status=HealthStatus.HEALTHY,
        observed_at=observed_at,
        last_success_at=completed_at,
        minutes_since_success=15.0,
        sla_minutes=60,
    )

    evaluator.evaluate.return_value = expected_health

    service = PipelineHealthService(
        repository=repository,
        evaluator=evaluator,
    )

    health = service.evaluate(
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
        observed_at=observed_at,
        sla_minutes=60,
    )

    repository.pipeline_updates.assert_called_once_with(
        pipeline_id="pipeline-1",
    )

    update_dataframe.collect.assert_called_once_with()
    row.asDict.assert_called_once_with(recursive=True)

    evaluator.evaluate.assert_called_once()

    evaluate_arguments = evaluator.evaluate.call_args.kwargs

    assert len(evaluate_arguments["updates"]) == 1

    update = evaluate_arguments["updates"][0]

    assert update.pipeline_id == "pipeline-1"
    assert update.pipeline_name == "silver_orders"
    assert update.update_id == "update-1"
    assert update.final_status == "COMPLETED"
    assert update.completed_at == completed_at

    assert evaluate_arguments["observed_at"] == observed_at
    assert evaluate_arguments["sla_minutes"] == 60

    assert health is expected_health


def test_health_service_returns_unknown_when_no_updates_exist() -> None:
    """A pipeline without update history should have unknown health."""
    repository = Mock()
    evaluator = Mock()

    observed_at = datetime(
        2026,
        8,
        8,
        12,
        0,
        tzinfo=UTC,
    )

    update_dataframe = Mock(name="update_dataframe")
    update_dataframe.collect.return_value = []

    repository.pipeline_updates.return_value = update_dataframe

    expected_health = PipelineHealth(
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
        status=HealthStatus.UNKNOWN,
        observed_at=observed_at,
        last_success_at=None,
        minutes_since_success=None,
        sla_minutes=60,
    )

    evaluator.evaluate.return_value = expected_health

    service = PipelineHealthService(
        repository=repository,
        evaluator=evaluator,
    )

    health = service.evaluate(
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
        observed_at=observed_at,
        sla_minutes=60,
    )

    evaluator.evaluate.assert_called_once_with(
        updates=(),
        observed_at=observed_at,
        sla_minutes=60,
        pipeline_id="pipeline-1",
        pipeline_name="silver_orders",
    )

    assert health is expected_health
