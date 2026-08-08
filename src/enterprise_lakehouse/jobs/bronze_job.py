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
from enterprise_lakehouse.bronze.writers import (
    BronzeDeltaWriter,
    BronzeStreamingWriter,
)
from enterprise_lakehouse.common.config import load_settings
from enterprise_lakehouse.common.metadata.models import LoadType, SourceMetadata
from enterprise_lakehouse.common.metadata.repository import MetadataRepository
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
    repository: MetadataRepository,
    metadata: SourceMetadata,
) -> BronzePipeline:
    """Compose the Bronze pipeline from production dependencies."""
    composer = LoaderComposer(spark=spark)
    reader = MetadataFileReader(composer=composer)

    ingestion_engine = IngestionEngine(
        reader=reader,
        repository=repository,
    )

    writer = (
        BronzeStreamingWriter() if metadata.load_type is LoadType.STREAMING else BronzeDeltaWriter()
    )

    return BronzePipeline(
        ingestion_engine=ingestion_engine,
        writer=writer,
    )


@dataclass(frozen=True, slots=True)
class BronzeJobArguments:
    """Runtime arguments required by the Bronze ingestion job."""

    source_id: str
    metadata_path: str
    config_path: str | None = None
    environment: str = "dev"
    catalog_name: str | None = None
    bronze_schema: str | None = None


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
        "--config-path",
        default=None,
        help="Path to the environment-specific application configuration.",
    )
    parser.add_argument(
        "--environment",
        default="dev",
        help="Deployment environment such as dev, uat, or prod.",
    )
    parser.add_argument(
        "--catalog-name",
        default=None,
        help="Resolved Unity Catalog name supplied by the deployment target.",
    )

    parser.add_argument(
        "--bronze-schema",
        default=None,
        help="Resolved Bronze schema supplied by the deployment target.",
    )

    arguments = parser.parse_args()

    return BronzeJobArguments(
        source_id=arguments.source_id,
        metadata_path=arguments.metadata_path,
        config_path=arguments.config_path,
        environment=arguments.environment,
        catalog_name=arguments.catalog_name,
        bronze_schema=arguments.bronze_schema,
    )


def main() -> None:
    """Run one metadata-driven Bronze ingestion job."""
    arguments = parse_arguments()
    spark = get_spark_session()

    config_path = arguments.config_path or f"configs/{arguments.environment}.yaml"

    settings = load_settings(
        config_path,
    )

    repository = YamlMetadataRepository(arguments.metadata_path)
    metadata = repository.get(arguments.source_id)

    pipeline = build_pipeline(
        spark=spark,
        repository=repository,
        metadata=metadata,
    )

    context = PipelineContext(
        pipeline_name="bronze_ingestion",
        run_id=uuid4(),
        environment=arguments.environment,
        started_at=datetime.now(UTC),
    )

    write_options: dict[str, str | bool] = {
        "mergeSchema": "true",
    }

    if metadata.load_type is LoadType.STREAMING:
        checkpoint_path = f"{settings.storage.checkpoint_path.rstrip('/')}/{metadata.source_id}"

        write_options = {
            "checkpointLocation": checkpoint_path,
            "trigger": "availableNow",
        }

    catalog_name = arguments.catalog_name or settings.catalog.catalog_name

    bronze_schema = arguments.bronze_schema or settings.catalog.bronze_schema

    write_config = BronzeWriteConfig(
        table_name=(f"{catalog_name}.{bronze_schema}.{metadata.target.bronze_table}"),
        mode="append",
        options=write_options,
    )

    pipeline.run(
        context=context,
        source_name=arguments.source_id,
        write_config=write_config,
    )


if __name__ == "__main__":
    main()
