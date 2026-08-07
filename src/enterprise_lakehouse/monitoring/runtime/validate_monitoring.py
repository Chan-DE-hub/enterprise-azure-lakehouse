"""Runtime validation for the monitoring framework."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from pyspark.sql import SparkSession

from enterprise_lakehouse.monitoring import MonitoringRepository


@dataclass(frozen=True, slots=True)
class MonitoringValidationArguments:
    """Runtime arguments for monitoring validation."""

    pipeline_ids: tuple[str, ...]


def parse_arguments() -> MonitoringValidationArguments:
    """Parse pipeline identifiers supplied by Databricks Workflows."""
    parser = argparse.ArgumentParser(
        description="Validate monitoring queries against Lakeflow pipelines.",
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


def _validate_pipeline(
    *,
    repository: MonitoringRepository,
    pipeline_id: str,
) -> None:
    """Validate monitoring queries against one Lakeflow pipeline."""
    print("=" * 80)
    print(f"PIPELINE: {pipeline_id}")
    print("=" * 80)

    print("PIPELINE UPDATES")
    repository.pipeline_updates(
        pipeline_id=pipeline_id,
    ).show(
        truncate=False,
    )

    print("FLOW METRICS")
    repository.flow_metrics(
        pipeline_id=pipeline_id,
    ).show(
        truncate=False,
    )

    print("EXPECTATION METRICS")
    repository.expectation_metrics(
        pipeline_id=pipeline_id,
    ).show(
        truncate=False,
    )


def validate_pipelines(
    *,
    repository: MonitoringRepository,
    pipeline_ids: tuple[str, ...],
) -> None:
    """Validate monitoring queries against one or more Lakeflow pipelines."""
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
