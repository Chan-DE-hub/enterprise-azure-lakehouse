"""Tests for the Bronze Databricks job entry point."""

import sys
from unittest.mock import Mock, patch

import pytest

from enterprise_lakehouse.common.metadata.models import LoadType
from enterprise_lakehouse.jobs.bronze_job import (
    BronzeJobArguments,
    build_pipeline,
    parse_arguments,
)


def test_parse_arguments_returns_bronze_job_configuration(
    monkeypatch,
) -> None:
    """The job should parse source, metadata, and environment arguments."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "bronze_job.py",
            "--source-id",
            "sales_orders",
            "--metadata-path",
            "/Volumes/dev/config/sources.yml",
            "--environment",
            "dev",
        ],
    )

    arguments = parse_arguments()

    assert arguments == BronzeJobArguments(
        source_id="sales_orders",
        metadata_path="/Volumes/dev/config/sources.yml",
        environment="dev",
    )


def test_parse_arguments_defaults_environment_to_dev(
    monkeypatch,
) -> None:
    """The job should default to the development environment."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "bronze_job.py",
            "--source-id",
            "sales_orders",
            "--metadata-path",
            "/Volumes/dev/config/sources.yml",
        ],
    )

    arguments = parse_arguments()

    assert arguments.environment == "dev"


def test_get_spark_session_returns_active_session() -> None:
    """The job should return the active Databricks Spark session."""
    active_session = object()

    with patch(
        "enterprise_lakehouse.jobs.bronze_job.SparkSession.getActiveSession",
        return_value=active_session,
    ):
        from enterprise_lakehouse.jobs.bronze_job import get_spark_session

        result = get_spark_session()

    assert result is active_session


def test_get_spark_session_requires_active_session() -> None:
    """The job should fail clearly when no Spark session is available."""
    with (
        patch(
            "enterprise_lakehouse.jobs.bronze_job.SparkSession.getActiveSession",
            return_value=None,
        ),
        pytest.raises(
            RuntimeError,
            match="No active Spark session is available for the Bronze job",
        ),
    ):
        from enterprise_lakehouse.jobs.bronze_job import get_spark_session

        get_spark_session()


def test_build_pipeline_composes_batch_writer() -> None:
    """Batch metadata should compose the batch Delta writer."""
    spark = Mock()
    repository = Mock()
    metadata = Mock()
    metadata.load_type = LoadType.FULL

    composer = Mock()
    reader = Mock()
    ingestion_engine = Mock()
    writer = Mock()
    pipeline = Mock()

    with (
        patch(
            "enterprise_lakehouse.jobs.bronze_job.LoaderComposer",
            return_value=composer,
        ) as composer_class,
        patch(
            "enterprise_lakehouse.jobs.bronze_job.MetadataFileReader",
            return_value=reader,
        ) as reader_class,
        patch(
            "enterprise_lakehouse.jobs.bronze_job.IngestionEngine",
            return_value=ingestion_engine,
        ) as engine_class,
        patch(
            "enterprise_lakehouse.jobs.bronze_job.BronzeDeltaWriter",
            return_value=writer,
        ) as writer_class,
        patch(
            "enterprise_lakehouse.jobs.bronze_job.BronzePipeline",
            return_value=pipeline,
        ) as pipeline_class,
    ):
        result = build_pipeline(
            spark=spark,
            repository=repository,
            metadata=metadata,
        )

    composer_class.assert_called_once_with(spark=spark)
    reader_class.assert_called_once_with(composer=composer)
    engine_class.assert_called_once_with(
        reader=reader,
        repository=repository,
    )
    writer_class.assert_called_once_with()
    pipeline_class.assert_called_once_with(
        ingestion_engine=ingestion_engine,
        writer=writer,
    )

    assert result is pipeline


def test_build_pipeline_composes_streaming_writer() -> None:
    """Streaming metadata should compose the streaming Delta writer."""
    spark = Mock()
    repository = Mock()
    metadata = Mock()
    metadata.load_type = LoadType.STREAMING

    composer = Mock()
    reader = Mock()
    ingestion_engine = Mock()
    writer = Mock()
    pipeline = Mock()

    with (
        patch(
            "enterprise_lakehouse.jobs.bronze_job.LoaderComposer",
            return_value=composer,
        ) as composer_class,
        patch(
            "enterprise_lakehouse.jobs.bronze_job.MetadataFileReader",
            return_value=reader,
        ) as reader_class,
        patch(
            "enterprise_lakehouse.jobs.bronze_job.IngestionEngine",
            return_value=ingestion_engine,
        ) as engine_class,
        patch(
            "enterprise_lakehouse.jobs.bronze_job.BronzeStreamingWriter",
            return_value=writer,
        ) as writer_class,
        patch(
            "enterprise_lakehouse.jobs.bronze_job.BronzePipeline",
            return_value=pipeline,
        ) as pipeline_class,
    ):
        result = build_pipeline(
            spark=spark,
            repository=repository,
            metadata=metadata,
        )

    composer_class.assert_called_once_with(spark=spark)
    reader_class.assert_called_once_with(composer=composer)
    engine_class.assert_called_once_with(
        reader=reader,
        repository=repository,
    )
    writer_class.assert_called_once_with()
    pipeline_class.assert_called_once_with(
        ingestion_engine=ingestion_engine,
        writer=writer,
    )

    assert result is pipeline


def test_main_runs_bronze_pipeline() -> None:
    """The job should build and run the Bronze pipeline."""
    arguments = BronzeJobArguments(
        source_id="sales_orders",
        metadata_path="/Volumes/dev/config/sources.yml",
        environment="dev",
    )

    spark = Mock()
    metadata = Mock()
    metadata.load_type = LoadType.FULL
    metadata.target.catalog_name = "dev_sales_lakehouse"
    metadata.target.bronze_schema = "bronze"
    metadata.target.bronze_table = "sales_orders"

    repository = Mock()
    repository.get.return_value = metadata

    pipeline = Mock()

    with (
        patch(
            "enterprise_lakehouse.jobs.bronze_job.parse_arguments",
            return_value=arguments,
        ),
        patch(
            "enterprise_lakehouse.jobs.bronze_job.get_spark_session",
            return_value=spark,
        ),
        patch(
            "enterprise_lakehouse.jobs.bronze_job.YamlMetadataRepository",
            return_value=repository,
        ) as repository_class,
        patch(
            "enterprise_lakehouse.jobs.bronze_job.build_pipeline",
            return_value=pipeline,
        ) as build_pipeline_mock,
    ):
        from enterprise_lakehouse.jobs.bronze_job import main

        main()

    repository_class.assert_called_once_with(
        "/Volumes/dev/config/sources.yml",
    )
    repository.get.assert_called_once_with("sales_orders")
    build_pipeline_mock.assert_called_once_with(
        spark=spark,
        repository=repository,
        metadata=metadata,
    )

    pipeline.run.assert_called_once()

    _, keyword_arguments = pipeline.run.call_args

    assert keyword_arguments["source_name"] == "sales_orders"
    assert keyword_arguments["context"].environment == "dev"
    assert keyword_arguments["write_config"].table_name == "dev_sales_lakehouse.bronze.sales_orders"
    assert keyword_arguments["write_config"].mode == "append"
    assert keyword_arguments["write_config"].options == {
        "mergeSchema": "true",
    }
