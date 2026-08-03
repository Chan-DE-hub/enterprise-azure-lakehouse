"""Tests for the Bronze reader contract."""

from datetime import UTC, datetime
from inspect import signature
from typing import Any
from uuid import uuid4

import pytest

from enterprise_lakehouse.bronze.models import PipelineContext
from enterprise_lakehouse.bronze.readers import BaseReader
from enterprise_lakehouse.common.metadata.models import (
    DataClassification,
    FileFormat,
    GovernanceMetadata,
    LoadType,
    SourceLocation,
    SourceMetadata,
    SourceType,
    TargetMetadata,
)


class IncompleteReader(BaseReader):
    """Reader intentionally missing required abstract members."""


class FakeReader(BaseReader):
    """Minimal concrete reader used to test the contract."""

    @property
    def source_type(self) -> str:
        """Return the source type handled by this reader."""
        return "fake"

    def read(
        self,
        *,
        context: PipelineContext,
        metadata: SourceMetadata,
    ) -> Any:
        """Return the supplied context and metadata."""
        return {
            "context": context,
            "metadata": metadata,
        }


def create_metadata() -> SourceMetadata:
    """Create canonical source metadata for reader tests."""
    return SourceMetadata(
        source_id="orders",
        source_system="erp",
        source_type=SourceType.FILE,
        load_type=LoadType.FULL,
        location=SourceLocation(
            object_name="orders",
            path="/Volumes/raw/orders",
        ),
        target=TargetMetadata(
            catalog_name="dev_sales_lakehouse",
            bronze_table="orders",
        ),
        governance=GovernanceMetadata(
            business_domain="sales",
            owner="data_engineering",
            data_classification=DataClassification.INTERNAL,
        ),
        primary_keys=("order_id",),
        event_timestamp_column="event_timestamp",
        file_format=FileFormat.PARQUET,
    )


def test_base_reader_cannot_be_instantiated() -> None:
    """The abstract base contract must not be directly instantiated."""
    with pytest.raises(TypeError):
        BaseReader()  # type: ignore[abstract]


def test_incomplete_reader_cannot_be_instantiated() -> None:
    """A subclass missing required members must remain abstract."""
    with pytest.raises(TypeError):
        IncompleteReader()  # type: ignore[abstract]


def test_concrete_reader_exposes_source_type() -> None:
    """A valid reader must expose its source type."""
    reader = FakeReader()

    assert reader.source_type == "fake"


def test_read_contract_accepts_context_and_metadata() -> None:
    """The reader contract must accept context and canonical metadata."""
    parameters = signature(BaseReader.read).parameters

    assert list(parameters) == [
        "self",
        "context",
        "metadata",
    ]


def test_concrete_reader_returns_source_data() -> None:
    """A valid reader must implement the read operation."""
    reader = FakeReader()

    context = PipelineContext(
        pipeline_name="bronze_ingestion",
        run_id=uuid4(),
        environment="test",
        started_at=datetime.now(UTC),
    )
    metadata = create_metadata()

    result = reader.read(
        context=context,
        metadata=metadata,
    )

    assert result == {
        "context": context,
        "metadata": metadata,
    }
