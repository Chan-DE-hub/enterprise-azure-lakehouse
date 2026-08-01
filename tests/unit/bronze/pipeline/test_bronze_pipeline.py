"""Tests for the Bronze pipeline."""

from datetime import UTC, datetime
from typing import Any
from unittest.mock import Mock
from uuid import uuid4

from enterprise_lakehouse.bronze.models import (
    BronzeWriteConfig,
    PipelineContext,
)
from enterprise_lakehouse.bronze.pipeline.bronze_pipeline import BronzePipeline


def create_context() -> PipelineContext:
    """Create a reusable pipeline execution context."""
    return PipelineContext(
        pipeline_name="bronze_sales_orders",
        run_id=uuid4(),
        environment="dev",
        started_at=datetime.now(UTC),
    )


def test_pipeline_reads_source_then_writes_dataframe() -> None:
    """The pipeline should pass ingestion output to the Bronze writer."""
    dataframe: Any = object()
    context = create_context()

    write_config = BronzeWriteConfig(
        table_name="dev_sales_lakehouse.bronze.sales_orders",
        mode="append",
        options={"mergeSchema": "true"},
    )

    ingestion_engine = Mock()
    ingestion_engine.run.return_value = dataframe

    writer = Mock()

    pipeline = BronzePipeline(
        ingestion_engine=ingestion_engine,
        writer=writer,
    )

    pipeline.run(
        context=context,
        source_name="sales_orders",
        write_config=write_config,
    )

    ingestion_engine.run.assert_called_once_with(
        context=context,
        source_name="sales_orders",
    )

    writer.write.assert_called_once_with(
        dataframe=dataframe,
        table_name="dev_sales_lakehouse.bronze.sales_orders",
        mode="append",
        options={"mergeSchema": "true"},
    )
