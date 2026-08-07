"""Repository for querying native Lakeflow operational metrics."""

from pyspark.sql import DataFrame, SparkSession

from enterprise_lakehouse.monitoring.query_loader import (
    render_pipeline_event_log_query,
)


class MonitoringRepository:
    """Execute packaged monitoring queries against pipeline event logs."""

    def __init__(
        self,
        *,
        spark: SparkSession,
    ) -> None:
        """Initialize the repository with an active Spark session."""
        self._spark = spark

    def pipeline_updates(
        self,
        *,
        pipeline_id: str,
    ) -> DataFrame:
        """Return pipeline update health and duration metrics."""
        return self._execute(
            resource_name="pipeline_update_summary.sql",
            pipeline_id=pipeline_id,
        )

    def flow_metrics(
        self,
        *,
        pipeline_id: str,
    ) -> DataFrame:
        """Return flow-level operational metrics."""
        return self._execute(
            resource_name="flow_metrics.sql",
            pipeline_id=pipeline_id,
        )

    def expectation_metrics(
        self,
        *,
        pipeline_id: str,
    ) -> DataFrame:
        """Return per-expectation data-quality metrics."""
        return self._execute(
            resource_name="expectation_metrics.sql",
            pipeline_id=pipeline_id,
        )

    def _execute(
        self,
        *,
        resource_name: str,
        pipeline_id: str,
    ) -> DataFrame:
        """Render and execute one packaged monitoring query."""
        query = render_pipeline_event_log_query(
            resource_name=resource_name,
            pipeline_id=pipeline_id,
        )

        return self._spark.sql(query)
