"""Lakeflow declarative Gold order fact dataset."""

from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession

from enterprise_lakehouse.common.metadata.yaml_repository import (
    YamlMetadataRepository,
)
from enterprise_lakehouse.gold import (
    GoldDatasetType,
    GoldDefinitionFactory,
)
from enterprise_lakehouse.gold.facts import OrderFactTransformer

SOURCE_ID = "sales_orders"
METADATA_PATH = "/Volumes/workspace/landing/source_files/config/sources.yaml"

SILVER_CATALOG_CONF = "enterprise_lakehouse.silver_catalog"
SILVER_SCHEMA_CONF = "enterprise_lakehouse.silver_schema"

repository = YamlMetadataRepository(METADATA_PATH)
metadata = repository.get(SOURCE_ID)

definition = GoldDefinitionFactory().build(
    metadata=metadata,
    dataset_name="fact_order",
    dataset_type=GoldDatasetType.FACT,
    grain="one row per order",
)


def get_spark_session() -> SparkSession:
    """Return the active Spark session for the Gold pipeline."""
    spark = SparkSession.getActiveSession()

    if spark is None:
        raise RuntimeError(
            "No active Spark session is available for the Gold pipeline.",
        )

    return spark


def get_silver_source_table(
    *,
    spark: SparkSession,
) -> str:
    """Resolve the deployed Silver source table from pipeline configuration."""
    silver_catalog = spark.conf.get(
        SILVER_CATALOG_CONF,
    )

    silver_schema = spark.conf.get(
        SILVER_SCHEMA_CONF,
    )

    if metadata.target.silver_table is None:
        raise ValueError(
            "silver_table is required for Gold processing.",
        )

    return f"{silver_catalog}.{silver_schema}.{metadata.target.silver_table}"


@dp.materialized_view(
    name=definition.dataset_name,
    comment="Gold order fact at one-row-per-order grain.",
)
def fact_order() -> DataFrame:
    """Publish the business-ready Gold order fact."""
    spark = get_spark_session()

    source_table = get_silver_source_table(
        spark=spark,
    )

    source_dataframe = spark.read.table(
        source_table,
    )

    transformer = OrderFactTransformer()

    return transformer.transform(
        source_dataframe,
    )
