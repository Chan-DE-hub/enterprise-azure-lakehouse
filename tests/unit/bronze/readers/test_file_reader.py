"""Tests for the Bronze file reader."""

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from enterprise_lakehouse.bronze.models import PipelineContext, SourceMetadata
from enterprise_lakehouse.bronze.readers.file_reader import FileReader


class FakeFileLoader:
    """Test double that records file-loading requests."""

    def __init__(self) -> None:
        """Initialize an empty collection of recorded calls."""
        self.calls: list[dict[str, Any]] = []

    def __call__(
        self,
        *,
        path: str,
        file_format: str,
        options: Mapping[str, Any],
    ) -> Any:
        """Record a file-loading request and return fake source data."""
        call = {
            "path": path,
            "file_format": file_format,
            "options": dict(options),
        }
        self.calls.append(call)

        return {"rows": 10}


def create_pipeline_context() -> PipelineContext:
    """Create a pipeline context for reader tests."""
    return PipelineContext(
        pipeline_name="bronze_ingestion",
        run_id=uuid4(),
        environment="test",
        started_at=datetime.now(UTC),
    )


def create_source_metadata(
    *,
    options: Mapping[str, Any],
) -> SourceMetadata:
    """Create file-source metadata for reader tests."""
    return SourceMetadata(
        source_name="orders",
        source_type="file",
        load_mode="incremental",
        primary_keys=("order_id",),
        watermark_column="updated_at",
        event_timestamp_column="event_timestamp",
        options=options,
    )


def test_file_reader_exposes_file_source_type() -> None:
    """The reader must identify itself as a file reader."""
    reader = FileReader(loader=FakeFileLoader())

    assert reader.source_type == "file"


def test_file_reader_delegates_to_file_loader() -> None:
    """The reader must delegate source loading using metadata options."""
    loader = FakeFileLoader()
    reader = FileReader(loader=loader)

    metadata = create_source_metadata(
        options={
            "path": "/Volumes/raw/orders",
            "format": "parquet",
            "mergeSchema": "true",
        }
    )

    result = reader.read(
        context=create_pipeline_context(),
        metadata=metadata,
    )

    assert result == {"rows": 10}
    assert loader.calls == [
        {
            "path": "/Volumes/raw/orders",
            "file_format": "parquet",
            "options": {"mergeSchema": "true"},
        }
    ]


def test_file_reader_requires_path_option() -> None:
    """The reader must require a configured file path."""
    loader = FakeFileLoader()
    reader = FileReader(loader=loader)

    metadata = create_source_metadata(
        options={
            "format": "parquet",
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required metadata option: path",
    ):
        reader.read(
            context=create_pipeline_context(),
            metadata=metadata,
        )

    assert loader.calls == []


def test_file_reader_requires_format_option() -> None:
    """The reader must require a configured file format."""
    loader = FakeFileLoader()
    reader = FileReader(loader=loader)

    metadata = create_source_metadata(
        options={
            "path": "/Volumes/raw/orders",
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required metadata option: format",
    ):
        reader.read(
            context=create_pipeline_context(),
            metadata=metadata,
        )

    assert loader.calls == []
