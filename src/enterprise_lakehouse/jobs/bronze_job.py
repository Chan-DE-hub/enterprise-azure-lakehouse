"""Databricks Bronze ingestion job entry point."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from pyspark.sql import SparkSession

from enterprise_lakehouse.bronze.engine import IngestionEngine
from enterprise_lakehouse.bronze.models import (
    BronzeWriteConfig,
    PipelineContext,
)
from enterprise_lakehouse.bronze.pipeline import BronzePipeline
from enterprise_lakehouse.bronze.readers import LoaderComposer, MetadataFileReader
from enterprise_lakehouse.bronze.writers import BronzeDeltaWriter
from enterprise_lakehouse.common.metadata.yaml_repository import (
    YamlMetadataRepository,
)


def get_spark_session() -> SparkSession:
    """Return the active Spark session provided by Databricks."""
    spark = SparkSession.getActiveSession()

    if spark is None:
        raise RuntimeError(
            "No active Spark session is available for the Bronze job.",
        )

    return spark


def build_pipeline(
    *,
    spark: SparkSession,
    metadata_path: str,
) -> BronzePipeline:
    """Compose the Bronze pipeline from production dependencies."""
    repository = YamlMetadataRepository(metadata_path)

    composer = LoaderComposer(spark=spark)
    reader = MetadataFileReader(composer=composer)

    ingestion_engine = IngestionEngine(
        reader=reader,
        repository=repository,
    )

    writer = BronzeDeltaWriter()

    return BronzePipeline(
        ingestion_engine=ingestion_engine,
        writer=writer,
    )


@dataclass(frozen=True, slots=True)
class BronzeJobArguments:
    """Runtime arguments required by the Bronze ingestion job."""

    source_id: str
    metadata_path: str
    environment: str


def parse_arguments() -> BronzeJobArguments:
    """Parse Bronze job arguments supplied by Databricks Workflows."""
    parser = argparse.ArgumentParser(
        description="Run one metadata-driven Bronze ingestion source.",
    )

    parser.add_argument(
        "--source-id",
        required=True,
        help="Unique source identifier defined in metadata.",
    )
    parser.add_argument(
        "--metadata-path",
        required=True,
        help="Workspace or volume path to the metadata YAML file.",
    )
    parser.add_argument(
        "--environment",
        default="dev",
        help="Deployment environment such as dev, uat, or prod.",
    )

    arguments = parser.parse_args()

    return BronzeJobArguments(
        source_id=arguments.source_id,
        metadata_path=arguments.metadata_path,
        environment=arguments.environment,
    )


def main() -> None:
    """Run one metadata-driven Bronze ingestion job."""
    arguments = parse_arguments()
    spark = get_spark_session()

    repository = YamlMetadataRepository(arguments.metadata_path)
    metadata = repository.get(arguments.source_id)

    pipeline = build_pipeline(
        spark=spark,
        metadata_path=arguments.metadata_path,
    )

    context = PipelineContext(
        pipeline_name="bronze_ingestion",
        run_id=uuid4(),
        environment=arguments.environment,
        started_at=datetime.now(UTC),
    )

    write_config = BronzeWriteConfig(
        table_name=(
            f"{metadata.target.catalog_name}."
            f"{metadata.target.bronze_schema}."
            f"{metadata.target.bronze_table}"
        ),
        mode="append",
        options={
            "mergeSchema": "true",
        },
    )

    pipeline.run(
        context=context,
        source_name=arguments.source_id,
        write_config=write_config,
    )


if __name__ == "__main__":
    main()
