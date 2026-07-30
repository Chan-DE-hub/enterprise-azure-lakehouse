"""Execution context shared across the Bronze ingestion pipeline."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class PipelineContext:
    """Immutable execution context for a single pipeline run.

    This object contains execution-level information that remains constant
    throughout the lifetime of a pipeline execution.
    """

    pipeline_name: str
    run_id: UUID
    environment: str
    started_at: datetime
