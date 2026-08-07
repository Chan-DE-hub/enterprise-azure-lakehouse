"""Tests for operational monitoring domain models."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from enterprise_lakehouse.monitoring import (
    ExpectationMetric,
    FlowMetric,
    PipelineUpdate,
)


def test_pipeline_update_stores_run_health_metrics() -> None:
    """Pipeline updates should preserve run-level operational metrics."""
    update = PipelineUpdate(
        pipeline_id="pipeline-123",
        pipeline_name="silver_orders",
        update_id="update-456",
        started_at=datetime(2026, 8, 6, 8, 0, tzinfo=UTC),
        completed_at=datetime(2026, 8, 6, 8, 5, tzinfo=UTC),
        final_status="COMPLETED",
        duration_seconds=300.0,
    )

    assert update.pipeline_name == "silver_orders"
    assert update.final_status == "COMPLETED"
    assert update.duration_seconds == 300.0


def test_flow_metric_supports_nullable_native_metrics() -> None:
    """Flow metrics should allow Lakeflow metrics that are not always emitted."""
    metric = FlowMetric(
        pipeline_id="pipeline-123",
        update_id="update-456",
        flow_name="silver_orders",
        final_status="COMPLETED",
        output_rows=100,
        upserted_rows=None,
        deleted_rows=None,
        expectation_dropped_rows=4,
    )

    assert metric.output_rows == 100
    assert metric.upserted_rows is None
    assert metric.expectation_dropped_rows == 4


def test_expectation_metric_stores_rule_results() -> None:
    """Expectation metrics should preserve per-rule pass and fail counts."""
    metric = ExpectationMetric(
        pipeline_id="pipeline-123",
        update_id="update-456",
        flow_name="silver_orders",
        dataset="silver_orders",
        expectation_name="valid_order_id",
        passed_records=98,
        failed_records=2,
    )

    assert metric.expectation_name == "valid_order_id"
    assert metric.passed_records == 98
    assert metric.failed_records == 2


def test_monitoring_models_are_immutable() -> None:
    """Operational evidence must not change after model creation."""
    update = PipelineUpdate(
        pipeline_id="pipeline-123",
        pipeline_name="silver_orders",
        update_id="update-456",
        final_status="COMPLETED",
    )

    with pytest.raises(ValidationError):
        update.final_status = "FAILED"
