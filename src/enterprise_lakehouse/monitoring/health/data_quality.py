"""Evaluate operational data-quality health."""

from __future__ import annotations

from collections.abc import Iterable

from pydantic import BaseModel, ConfigDict, Field

from enterprise_lakehouse.monitoring.health.models import HealthStatus
from enterprise_lakehouse.monitoring.models import ExpectationMetric


class DataQualityHealth(BaseModel):
    """Immutable operational health derived from expectation evidence."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    status: HealthStatus
    expectations_evaluated: int = Field(ge=0)

    worst_expectation_name: str | None = None
    worst_failure_rate: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )


class DataQualityHealthEvaluator:
    """Evaluate data-quality health using per-expectation failure rates."""

    def evaluate(
        self,
        *,
        metrics: Iterable[ExpectationMetric],
        degraded_failure_rate: float,
        unhealthy_failure_rate: float,
    ) -> DataQualityHealth:
        """Return health based on the worst expectation failure rate."""
        metric_list = tuple(metrics)

        if not metric_list:
            return DataQualityHealth(
                status=HealthStatus.UNKNOWN,
                expectations_evaluated=0,
                worst_expectation_name=None,
                worst_failure_rate=None,
            )

        expectation_rates = tuple(
            (
                metric.expectation_name,
                self._failure_rate(metric),
            )
            for metric in metric_list
        )

        worst_expectation_name, worst_failure_rate = max(
            expectation_rates,
            key=lambda item: item[1],
        )

        if worst_failure_rate >= unhealthy_failure_rate:
            status = HealthStatus.UNHEALTHY
        elif worst_failure_rate >= degraded_failure_rate:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.HEALTHY

        return DataQualityHealth(
            status=status,
            expectations_evaluated=len(metric_list),
            worst_expectation_name=worst_expectation_name,
            worst_failure_rate=worst_failure_rate,
        )

    @staticmethod
    def _failure_rate(
        metric: ExpectationMetric,
    ) -> float:
        """Return the failure rate for one expectation."""
        evaluated_records = metric.passed_records + metric.failed_records

        if evaluated_records == 0:
            return 0.0

        return metric.failed_records / evaluated_records
