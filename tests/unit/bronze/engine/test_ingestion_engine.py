"""Tests for the Bronze ingestion engine."""

from datetime import UTC, datetime
from typing import Any, override
from uuid import uuid4

from enterprise_lakehouse.bronze.engine import IngestionEngine
from enterprise_lakehouse.bronze.models import (
    PipelineContext,
    SourceMetadata,
)
from enterprise_lakehouse.bronze.readers import BaseReader
from enterprise_lakehouse.bronze.repositories import MetadataRepository


class FakeReader(BaseReader):
    """Minimal reader used to test engine dependency wiring."""

    @property
    def source_type(self) -> str:
        """Return the source type handled by the reader."""
        return "fake"

    def read(
        self,
        *,
        context: PipelineContext,
        metadata: SourceMetadata,
    ) -> Any:
        """Return metadata options as fake source data."""
        del context

        return metadata.options


def create_metadata() -> SourceMetadata:
    """Create reusable source metadata for engine tests."""
    return SourceMetadata(
        source_name="sales_orders",
        source_type="file",
        ingestion_mode="batch",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column="event_timestamp",
        options={"format": "parquet"},
    )


class FakeMetadataRepository(MetadataRepository):
    """Repository used to test metadata loading."""

    def __init__(
        self,
        metadata: SourceMetadata | None = None,
    ) -> None:
        self.metadata = metadata or create_metadata()
        self.loaded_source_name: str | None = None

    @override
    def load(self, source_name: str) -> SourceMetadata:
        """Return metadata for the requested source."""
        self.loaded_source_name = source_name
        return self.metadata


def create_context() -> PipelineContext:
    """Create a reusable pipeline context for engine tests."""
    return PipelineContext(
        pipeline_name="bronze_orders",
        run_id=uuid4(),
        environment="dev",
        started_at=datetime.now(UTC),
    )


def test_engine_stores_reader_dependency() -> None:
    """The engine should preserve its injected reader dependency."""
    reader = FakeReader()
    repository = FakeMetadataRepository()

    engine = IngestionEngine(
        reader=reader,
        repository=repository,
    )

    assert engine.reader is reader


def test_run_accepts_pipeline_context() -> None:
    """The engine should delegate execution using the supplied context."""
    engine = IngestionEngine(
        reader=FakeReader(),
        repository=FakeMetadataRepository(),
    )

    context = create_context()

    result = engine.run(
        context=context,
        source_name="sales_orders",
    )

    assert result == {"format": "parquet"}


def test_engine_loads_metadata_for_requested_source() -> None:
    """The engine should load metadata for the requested source."""
    repository = FakeMetadataRepository()

    engine = IngestionEngine(
        reader=FakeReader(),
        repository=repository,
    )

    context = create_context()

    engine.run(
        context=context,
        source_name="sales_orders",
    )

    assert repository.loaded_source_name == "sales_orders"
