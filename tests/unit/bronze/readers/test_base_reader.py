"""Tests for the Bronze reader contract."""

from datetime import UTC, datetime
from inspect import signature
from typing import Any
from uuid import uuid4

import pytest

from enterprise_lakehouse.bronze.models import PipelineContext, SourceMetadata
from enterprise_lakehouse.bronze.readers import BaseReader


class IncompleteReader(BaseReader):
    """Reader intentionally missing required abstract members."""


class FakeReader(BaseReader):
    """Minimal concrete reader used to test the contract."""

    @property
    def source_type(self) -> str:
        return "fake"

    def read(
        self,
        *,
        context: PipelineContext,
        metadata: SourceMetadata,
    ) -> Any:
        return {
            "context": context,
            "metadata": metadata,
        }


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
    """The reader contract must use Bronze domain models."""
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
    metadata = SourceMetadata(
        source_name="orders",
        source_type="fake",
        ingestion_mode="batch",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column="event_timestamp",
        options={"path": "/Volumes/raw/orders"},
    )

    result = reader.read(
        context=context,
        metadata=metadata,
    )

    assert result == {
        "context": context,
        "metadata": metadata,
    }
