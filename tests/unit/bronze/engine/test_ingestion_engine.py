"""Tests for the Bronze ingestion engine."""

from datetime import UTC, datetime
from typing import Any, override
from uuid import uuid4

from enterprise_lakehouse.bronze.engine import IngestionEngine
from enterprise_lakehouse.bronze.models import PipelineContext
from enterprise_lakehouse.bronze.readers import BaseReader
from enterprise_lakehouse.common.metadata.models import (
    FileFormat,
    GovernanceMetadata,
    LoadType,
    SourceLocation,
    SourceMetadata,
    SourceType,
    TargetMetadata,
)
from enterprise_lakehouse.common.metadata.repository import MetadataRepository


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
        """Return metadata reader options as fake source data."""
        del context

        return dict(metadata.reader_options)


def create_metadata() -> SourceMetadata:
    """Create reusable canonical source metadata for engine tests."""
    return SourceMetadata(
        source_id="sales_orders",
        source_system="erp",
        source_type=SourceType.FILE,
        load_type=LoadType.INCREMENTAL,
        location=SourceLocation(
            object_name="sales_orders",
            path="/Volumes/raw/sales_orders",
        ),
        target=TargetMetadata(
            catalog_name="dev_sales_lakehouse",
            bronze_table="sales_orders",
        ),
        governance=GovernanceMetadata(
            business_domain="sales",
            owner="data_engineering",
        ),
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column="event_timestamp",
        file_format=FileFormat.PARQUET,
        reader_options={
            "mergeSchema": "true",
        },
    )


class FakeMetadataRepository(MetadataRepository):
    """Repository used to test canonical metadata lookup."""

    def __init__(
        self,
        metadata: SourceMetadata | None = None,
    ) -> None:
        """Initialize the repository with reusable source metadata."""
        self.metadata = metadata or create_metadata()
        self.requested_source_id: str | None = None

    @override
    def load(self) -> list[SourceMetadata]:
        """Return all configured metadata definitions."""
        return [self.metadata]

    @override
    def get(self, source_id: str) -> SourceMetadata:
        """Record and return the requested source metadata."""
        self.requested_source_id = source_id
        return super().get(source_id)


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

    result = engine.run(
        context=create_context(),
        source_name="sales_orders",
    )

    assert result == {
        "mergeSchema": "true",
    }


def test_engine_loads_metadata_for_requested_source() -> None:
    """The engine should request metadata using the supplied source ID."""
    repository = FakeMetadataRepository()

    engine = IngestionEngine(
        reader=FakeReader(),
        repository=repository,
    )

    engine.run(
        context=create_context(),
        source_name="sales_orders",
    )

    assert repository.requested_source_id == "sales_orders"
