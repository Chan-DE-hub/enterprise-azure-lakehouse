"""Runtime validation for the monitoring and observability framework."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime

from pyspark.sql import DataFrame, SparkSession

from enterprise_lakehouse.monitoring import (
    ExpectationMetric,
    MonitoringRepository,
    PipelineUpdate,
)
from enterprise_lakehouse.monitoring.health import (
    DataQualityHealthEvaluator,
    PipelineHealthEvaluator,
)

DEFAULT_SLA_MINUTES = 60
DEFAULT_DEGRADED_FAILURE_RATE = 0.01
DEFAULT_UNHEALTHY_FAILURE_RATE = 0.05


@dataclass(frozen=True, slots=True)
class MonitoringValidationArguments:
    """Runtime arguments for monitoring validation."""

    pipeline_ids: tuple[str, ...]


def parse_arguments() -> MonitoringValidationArguments:
    """Parse pipeline identifiers supplied by Databricks Workflows."""
    parser = argparse.ArgumentParser(
        description=("Validate Lakeflow monitoring queries and operational health evaluation."),
    )

    parser.add_argument(
        "--pipeline-id",
        action="append",
        required=True,
        dest="pipeline_ids",
        help=(
            "Lakeflow pipeline UUID to validate. "
            "Specify --pipeline-id multiple times to validate multiple pipelines."
        ),
    )

    arguments = parser.parse_args()

    return MonitoringValidationArguments(
        pipeline_ids=tuple(arguments.pipeline_ids),
    )


def get_spark_session() -> SparkSession:
    """Return the active Spark session provided by Databricks."""
    spark = SparkSession.getActiveSession()

    if spark is None:
        raise RuntimeError(
            "No active Spark session is available for monitoring validation.",
        )

    return spark


def _collect_pipeline_updates(
    dataframe: DataFrame,
) -> tuple[PipelineUpdate, ...]:
    """Convert Spark update rows into monitoring domain models."""
    return tuple(
        PipelineUpdate.model_validate(
            row.asDict(
                recursive=True,
            ),
        )
        for row in dataframe.collect()
    )


def _collect_expectation_metrics(
    dataframe: DataFrame,
) -> tuple[ExpectationMetric, ...]:
    """Convert Spark expectation rows into monitoring domain models."""
    return tuple(
        ExpectationMetric.model_validate(
            row.asDict(
                recursive=True,
            ),
        )
        for row in dataframe.collect()
    )


def _validate_pipeline(
    *,
    repository: MonitoringRepository,
    pipeline_id: str,
) -> None:
    """Validate monitoring and health evaluation for one Lakeflow pipeline."""
    observed_at = datetime.now(UTC)

    print("=" * 80)
    print(f"PIPELINE: {pipeline_id}")
    print("=" * 80)

    print("PIPELINE UPDATES")
    pipeline_updates_dataframe = repository.pipeline_updates(
        pipeline_id=pipeline_id,
    )

    pipeline_updates_dataframe.show(
        truncate=False,
    )

    pipeline_updates = _collect_pipeline_updates(
        pipeline_updates_dataframe,
    )

    print("FLOW METRICS")
    repository.flow_metrics(
        pipeline_id=pipeline_id,
    ).show(
        truncate=False,
    )

    print("EXPECTATION METRICS")
    expectation_metrics_dataframe = repository.expectation_metrics(
        pipeline_id=pipeline_id,
    )

    expectation_metrics_dataframe.show(
        truncate=False,
    )

    expectation_metrics = _collect_expectation_metrics(
        expectation_metrics_dataframe,
    )

    print("PIPELINE HEALTH")

    if pipeline_updates:
        pipeline_health = PipelineHealthEvaluator().evaluate(
            updates=pipeline_updates,
            observed_at=observed_at,
            sla_minutes=DEFAULT_SLA_MINUTES,
        )

        print(
            pipeline_health.model_dump_json(
                indent=2,
            ),
        )
    else:
        print(
            "No pipeline update history is available; "
            "pipeline health cannot be evaluated from runtime evidence.",
        )

    print("DATA QUALITY HEALTH")

    data_quality_health = DataQualityHealthEvaluator().evaluate(
        metrics=expectation_metrics,
        degraded_failure_rate=DEFAULT_DEGRADED_FAILURE_RATE,
        unhealthy_failure_rate=DEFAULT_UNHEALTHY_FAILURE_RATE,
    )

    print(
        data_quality_health.model_dump_json(
            indent=2,
        ),
    )


def validate_pipelines(
    *,
    repository: MonitoringRepository,
    pipeline_ids: tuple[str, ...],
) -> None:
    """Validate one or more Lakeflow pipelines."""
    for pipeline_id in pipeline_ids:
        _validate_pipeline(
            repository=repository,
            pipeline_id=pipeline_id,
        )


def main() -> None:
    """Execute monitoring validation for configured pipelines."""
    arguments = parse_arguments()
    spark = get_spark_session()

    repository = MonitoringRepository(
        spark=spark,
    )

    validate_pipelines(
        repository=repository,
        pipeline_ids=arguments.pipeline_ids,
    )


if __name__ == "__main__":
    main()
