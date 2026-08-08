"""Operational health domain models."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class HealthStatus(StrEnum):
    """Supported operational health states."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class PipelineHealth(BaseModel):
    """Immutable operational health state for one pipeline."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    pipeline_id: str = Field(min_length=1)
    pipeline_name: str = Field(min_length=1)

    status: HealthStatus

    observed_at: datetime
    last_success_at: datetime | None = None
    minutes_since_success: float | None = Field(
        default=None,
        ge=0,
    )

    sla_minutes: int = Field(
        gt=0,
    )
