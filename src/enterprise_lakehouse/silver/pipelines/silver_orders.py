"""Lakeflow declarative Silver orders dataset."""

from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession

from enterprise_lakehouse.common.metadata.yaml_repository import (
    YamlMetadataRepository,
)
from enterprise_lakehouse.silver.metadata import StandardizationRuleFactory
from enterprise_lakehouse.silver.pipelines import SilverPipeline
from enterprise_lakehouse.silver.processors import StandardizationProcessor

SOURCE_ID = "sales_orders"
METADATA_PATH = "/Volumes/workspace/landing/source_files/config/sources.yaml"


def get_spark_session() -> SparkSession:
    """Return the active Spark session for the Silver pipeline."""
    spark = SparkSession.getActiveSession()

    if spark is None:
        raise RuntimeError(
            "No active Spark session is available for the Silver pipeline.",
        )

    return spark


@dp.table(
    name="silver_orders",
    comment="Typed and standardized sales orders from the Bronze layer.",
)
def silver_orders() -> DataFrame:
    """Define the metadata-driven Silver orders streaming table."""
    spark = get_spark_session()

    repository = YamlMetadataRepository(METADATA_PATH)
    metadata = repository.get(SOURCE_ID)

    source_table = (
        f"{metadata.target.catalog_name}."
        f"{metadata.target.bronze_schema}."
        f"{metadata.target.bronze_table}"
    )

    rules = StandardizationRuleFactory().build(
        metadata.standardization,
    )

    source_dataframe = spark.readStream.table(source_table)

    pipeline = SilverPipeline(
        processors=(StandardizationProcessor(rules=rules),),
    )

    return pipeline.run(source_dataframe)
