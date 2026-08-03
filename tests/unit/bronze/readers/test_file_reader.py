"""Tests for the Bronze file reader."""

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from enterprise_lakehouse.bronze.models import PipelineContext
from enterprise_lakehouse.bronze.readers.file_reader import FileReader
from enterprise_lakehouse.common.metadata.models import (
    FileFormat,
    GovernanceMetadata,
    LoadType,
    SourceLocation,
    SourceMetadata,
    SourceType,
    TargetMetadata,
)


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
    path: str | None = "/Volumes/raw/orders",
    file_format: FileFormat | None = FileFormat.PARQUET,
    reader_options: dict[str, str | int | float | bool] | None = None,
) -> SourceMetadata:
    """Create canonical file-source metadata for reader tests."""
    values = {
        "source_id": "orders",
        "source_system": "erp",
        "source_type": SourceType.FILE,
        "load_type": LoadType.FULL,
        "location": SourceLocation(
            object_name="orders",
            path=path,
        ),
        "target": TargetMetadata(
            catalog_name="dev_sales_lakehouse",
            bronze_table="orders",
        ),
        "governance": GovernanceMetadata(
            business_domain="sales",
            owner="data_engineering",
        ),
        "primary_keys": ("order_id",),
        "event_timestamp_column": "event_timestamp",
        "file_format": file_format,
        "reader_options": reader_options or {},
        "enabled": True,
        "priority": 100,
    }

    if path is None or file_format is None:
        # Deliberately bypass model validation to verify the reader's
        # defensive checks independently of metadata validation.
        return SourceMetadata.model_construct(**values)

    return SourceMetadata(**values)


def test_file_reader_exposes_file_source_type() -> None:
    """The reader must identify itself as a file reader."""
    reader = FileReader(loader=FakeFileLoader())

    assert reader.source_type == "file"


def test_file_reader_delegates_to_file_loader() -> None:
    """The reader must delegate using canonical metadata fields."""
    loader = FakeFileLoader()
    reader = FileReader(loader=loader)

    metadata = create_source_metadata(
        reader_options={
            "mergeSchema": "true",
        },
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
            "options": {
                "mergeSchema": "true",
            },
        }
    ]


def test_file_reader_requires_source_path() -> None:
    """The reader must reject metadata without a source path."""
    loader = FakeFileLoader()
    reader = FileReader(loader=loader)

    metadata = create_source_metadata(path=None)

    with pytest.raises(
        ValueError,
        match="Missing source path for file source: orders",
    ):
        reader.read(
            context=create_pipeline_context(),
            metadata=metadata,
        )

    assert loader.calls == []


def test_file_reader_requires_file_format() -> None:
    """The reader must reject metadata without a file format."""
    loader = FakeFileLoader()
    reader = FileReader(loader=loader)

    metadata = create_source_metadata(file_format=None)

    with pytest.raises(
        ValueError,
        match="Missing file format for file source: orders",
    ):
        reader.read(
            context=create_pipeline_context(),
            metadata=metadata,
        )

    assert loader.calls == []
