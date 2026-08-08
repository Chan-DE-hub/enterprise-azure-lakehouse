"""Operational monitoring domain models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MonitoringModel(BaseModel):
    """Base model for immutable operational monitoring evidence."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )


class PipelineUpdate(MonitoringModel):
    """Run-level health and timing metrics for one pipeline update."""

    pipeline_id: str = Field(min_length=1)
    pipeline_name: str = Field(min_length=1)
    update_id: str = Field(min_length=1)

    started_at: datetime | None = None
    completed_at: datetime | None = None
    final_status: str = Field(min_length=1)
    duration_seconds: float | None = Field(default=None, ge=0)
    error_message: str | None = None


class FlowMetric(MonitoringModel):
    """Operational metrics for one Lakeflow flow within an update."""

    pipeline_id: str = Field(min_length=1)
    update_id: str = Field(min_length=1)
    flow_name: str = Field(min_length=1)
    final_status: str = Field(min_length=1)

    output_rows: int | None = Field(default=None, ge=0)
    upserted_rows: int | None = Field(default=None, ge=0)
    deleted_rows: int | None = Field(default=None, ge=0)
    expectation_dropped_rows: int | None = Field(default=None, ge=0)


class ExpectationMetric(MonitoringModel):
    """Per-expectation data-quality results for one Lakeflow flow."""

    pipeline_id: str = Field(min_length=1)
    pipeline_name: str | None = Field(
        default=None,
        min_length=1,
    )
    update_id: str = Field(min_length=1)
    flow_name: str = Field(min_length=1)
    dataset: str = Field(min_length=1)
    expectation_name: str = Field(min_length=1)

    passed_records: int = Field(ge=0)
    failed_records: int = Field(ge=0)

    first_recorded_at: datetime | None = None
    last_recorded_at: datetime | None = None
