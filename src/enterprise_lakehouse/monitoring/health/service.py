"""Orchestrate pipeline health evaluation from monitoring evidence."""

from datetime import datetime

from enterprise_lakehouse.monitoring.health.evaluator import (
    PipelineHealthEvaluator,
)
from enterprise_lakehouse.monitoring.health.models import PipelineHealth
from enterprise_lakehouse.monitoring.models import PipelineUpdate
from enterprise_lakehouse.monitoring.repository import MonitoringRepository


class PipelineHealthService:
    """Connect monitoring telemetry retrieval with health evaluation."""

    def __init__(
        self,
        *,
        repository: MonitoringRepository,
        evaluator: PipelineHealthEvaluator,
    ) -> None:
        """Initialize the health service dependencies."""
        self._repository = repository
        self._evaluator = evaluator

    def evaluate(
        self,
        *,
        pipeline_id: str,
        pipeline_name: str,
        observed_at: datetime,
        sla_minutes: int,
    ) -> PipelineHealth:
        """Evaluate health for one Lakeflow pipeline."""
        dataframe = self._repository.pipeline_updates(
            pipeline_id=pipeline_id,
        )

        updates = tuple(
            PipelineUpdate.model_validate(
                row.asDict(
                    recursive=True,
                ),
            )
            for row in dataframe.collect()
        )

        return self._evaluator.evaluate(
            updates=updates,
            observed_at=observed_at,
            sla_minutes=sla_minutes,
            pipeline_id=pipeline_id,
            pipeline_name=pipeline_name,
        )
