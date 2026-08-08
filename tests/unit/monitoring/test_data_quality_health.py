"""Tests for data-quality operational health evaluation."""

from enterprise_lakehouse.monitoring.health import (
    DataQualityHealthEvaluator,
    HealthStatus,
)
from enterprise_lakehouse.monitoring.models import ExpectationMetric


def build_metric(
    *,
    expectation_name: str = "valid_order_id",
    passed_records: int,
    failed_records: int,
) -> ExpectationMetric:
    """Build representative expectation evidence."""
    return ExpectationMetric(
        pipeline_id="pipeline-1",
        update_id="update-1",
        flow_name="silver_orders",
        dataset="silver_orders",
        expectation_name=expectation_name,
        passed_records=passed_records,
        failed_records=failed_records,
    )


def test_data_quality_health_is_healthy_without_failures() -> None:
    """Zero failed expectation records should be healthy."""
    health = DataQualityHealthEvaluator().evaluate(
        metrics=(
            build_metric(
                passed_records=100,
                failed_records=0,
            ),
        ),
        degraded_failure_rate=0.01,
        unhealthy_failure_rate=0.05,
    )

    assert health.status is HealthStatus.HEALTHY
    assert health.expectations_evaluated == 1
    assert health.worst_expectation_name == "valid_order_id"
    assert health.worst_failure_rate == 0.0


def test_data_quality_health_is_degraded_above_warning_threshold() -> None:
    """Moderate expectation failure rates should be degraded."""
    health = DataQualityHealthEvaluator().evaluate(
        metrics=(
            build_metric(
                passed_records=98,
                failed_records=2,
            ),
        ),
        degraded_failure_rate=0.01,
        unhealthy_failure_rate=0.05,
    )

    assert health.status is HealthStatus.DEGRADED
    assert health.worst_failure_rate == 0.02


def test_data_quality_health_is_unhealthy_above_failure_threshold() -> None:
    """High expectation failure rates should be unhealthy."""
    health = DataQualityHealthEvaluator().evaluate(
        metrics=(
            build_metric(
                passed_records=90,
                failed_records=10,
            ),
        ),
        degraded_failure_rate=0.01,
        unhealthy_failure_rate=0.05,
    )

    assert health.status is HealthStatus.UNHEALTHY
    assert health.worst_failure_rate == 0.1


def test_data_quality_health_uses_worst_expectation_rate() -> None:
    """Overall health should reflect the worst individual expectation."""
    health = DataQualityHealthEvaluator().evaluate(
        metrics=(
            build_metric(
                expectation_name="valid_order_id",
                passed_records=100,
                failed_records=0,
            ),
            build_metric(
                expectation_name="positive_order_total",
                passed_records=93,
                failed_records=7,
            ),
        ),
        degraded_failure_rate=0.01,
        unhealthy_failure_rate=0.05,
    )

    assert health.status is HealthStatus.UNHEALTHY
    assert health.expectations_evaluated == 2
    assert health.worst_expectation_name == "positive_order_total"
    assert health.worst_failure_rate == 0.07


def test_data_quality_health_is_unknown_without_metrics() -> None:
    """Missing expectation evidence should produce unknown health."""
    health = DataQualityHealthEvaluator().evaluate(
        metrics=(),
        degraded_failure_rate=0.01,
        unhealthy_failure_rate=0.05,
    )

    assert health.status is HealthStatus.UNKNOWN
    assert health.expectations_evaluated == 0
    assert health.worst_expectation_name is None
    assert health.worst_failure_rate is None
