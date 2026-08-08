"""Evaluate actionable pipeline operational health."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime

from enterprise_lakehouse.monitoring.health.models import (
    HealthStatus,
    PipelineHealth,
)
from enterprise_lakehouse.monitoring.models import PipelineUpdate


class PipelineHealthEvaluator:
    """Evaluate operational health from pipeline update evidence."""

    def evaluate(
        self,
        *,
        updates: Iterable[PipelineUpdate],
        observed_at: datetime,
        sla_minutes: int,
        pipeline_id: str | None = None,
        pipeline_name: str | None = None,
    ) -> PipelineHealth:
        """Return actionable pipeline health for the observed point in time."""
        normalized_observed_at = self._as_utc(
            observed_at,
        )

        update_list = tuple(updates)

        if not update_list:
            if pipeline_id is None or pipeline_name is None:
                raise ValueError(
                    "pipeline_id and pipeline_name are required when updates are empty.",
                )

            return PipelineHealth(
                pipeline_id=pipeline_id,
                pipeline_name=pipeline_name,
                status=HealthStatus.UNKNOWN,
                observed_at=normalized_observed_at,
                last_success_at=None,
                minutes_since_success=None,
                sla_minutes=sla_minutes,
            )

        latest_update = max(
            update_list,
            key=lambda update: self._latest_timestamp(
                update,
            ),
        )

        successful_updates = tuple(
            update
            for update in update_list
            if (update.final_status.upper() == "COMPLETED" and update.completed_at is not None)
        )

        last_success_at = (
            max(
                self._as_utc(update.completed_at)
                for update in successful_updates
                if update.completed_at is not None
            )
            if successful_updates
            else None
        )

        minutes_since_success = (
            (normalized_observed_at - last_success_at).total_seconds() / 60.0
            if last_success_at is not None
            else None
        )

        if latest_update.final_status.upper() == "FAILED":
            status = HealthStatus.UNHEALTHY
        elif last_success_at is None:
            status = HealthStatus.UNKNOWN
        elif minutes_since_success is not None and minutes_since_success > sla_minutes:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.HEALTHY

        return PipelineHealth(
            pipeline_id=latest_update.pipeline_id,
            pipeline_name=latest_update.pipeline_name,
            status=status,
            observed_at=normalized_observed_at,
            last_success_at=last_success_at,
            minutes_since_success=minutes_since_success,
            sla_minutes=sla_minutes,
        )

    @classmethod
    def _latest_timestamp(
        cls,
        update: PipelineUpdate,
    ) -> datetime:
        """Return a normalized timestamp used to order updates."""
        timestamp = update.completed_at or update.started_at

        if timestamp is None:
            return datetime.min.replace(
                tzinfo=UTC,
            )

        return cls._as_utc(
            timestamp,
        )

    @staticmethod
    def _as_utc(
        value: datetime,
    ) -> datetime:
        """Normalize one datetime to timezone-aware UTC."""
        if value.tzinfo is None:
            return value.replace(
                tzinfo=UTC,
            )

        return value.astimezone(
            UTC,
        )
