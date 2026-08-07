"""Lakeflow declarative Gold sales datasets."""

from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession

from enterprise_lakehouse.common.metadata.yaml_repository import (
    YamlMetadataRepository,
)
from enterprise_lakehouse.gold import (
    GoldDatasetType,
    GoldDefinitionFactory,
)
from enterprise_lakehouse.gold.aggregates import (
    CustomerOrderSummaryTransformer,
)
from enterprise_lakehouse.gold.dimensions import (
    CustomerDimensionTransformer,
)
from enterprise_lakehouse.gold.facts import (
    OrderFactTransformer,
)

ORDERS_SOURCE_ID = "sales_orders"
CUSTOMERS_SOURCE_ID = "customers_cdc"

METADATA_PATH = "/Volumes/workspace/landing/source_files/config/sources.yaml"

SILVER_CATALOG_CONF = "enterprise_lakehouse.silver_catalog"
SILVER_SCHEMA_CONF = "enterprise_lakehouse.silver_schema"

repository = YamlMetadataRepository(
    METADATA_PATH,
)

orders_metadata = repository.get(
    ORDERS_SOURCE_ID,
)

customers_metadata = repository.get(
    CUSTOMERS_SOURCE_ID,
)

gold_definition_factory = GoldDefinitionFactory()

order_fact_definition = gold_definition_factory.build(
    metadata=orders_metadata,
    dataset_name="fact_order",
    dataset_type=GoldDatasetType.FACT,
    grain="one row per order",
)

customer_dimension_definition = gold_definition_factory.build(
    metadata=customers_metadata,
    dataset_name="dim_customer",
    dataset_type=GoldDatasetType.DIMENSION,
    grain="one row per current customer",
)


def get_spark_session() -> SparkSession:
    """Return the active Spark session for the Gold pipeline."""
    spark = SparkSession.getActiveSession()

    if spark is None:
        raise RuntimeError(
            "No active Spark session is available for the Gold pipeline.",
        )

    return spark


def get_silver_table(
    *,
    spark: SparkSession,
    table_name: str,
) -> str:
    """Resolve one deployed Silver table from pipeline configuration."""
    silver_catalog = spark.conf.get(
        SILVER_CATALOG_CONF,
    )

    silver_schema = spark.conf.get(
        SILVER_SCHEMA_CONF,
    )

    return f"{silver_catalog}.{silver_schema}.{table_name}"


@dp.materialized_view(
    name=order_fact_definition.dataset_name,
    comment="Gold order fact at one-row-per-order grain.",
)
def fact_order() -> DataFrame:
    """Publish the business-ready Gold order fact."""
    spark = get_spark_session()

    if orders_metadata.target.silver_table is None:
        raise ValueError(
            "silver_table is required for the order fact.",
        )

    source_table = get_silver_table(
        spark=spark,
        table_name=orders_metadata.target.silver_table,
    )

    source_dataframe = spark.read.table(
        source_table,
    )

    transformer = OrderFactTransformer()

    return transformer.transform(
        source_dataframe,
    )


@dp.materialized_view(
    name=customer_dimension_definition.dataset_name,
    comment="Current-state Gold customer dimension at one-row-per-customer grain.",
)
def dim_customer() -> DataFrame:
    """Publish the current-state Gold customer dimension."""
    spark = get_spark_session()

    if customers_metadata.target.silver_table is None:
        raise ValueError(
            "silver_table is required for the customer dimension.",
        )

    source_table = get_silver_table(
        spark=spark,
        table_name=customers_metadata.target.silver_table,
    )

    source_dataframe = spark.read.table(
        source_table,
    )

    transformer = CustomerDimensionTransformer()

    return transformer.transform(
        source_dataframe,
    )


@dp.materialized_view(
    name="customer_order_summary",
    comment="Customer-level Gold order metrics derived from the canonical order fact.",
)
def customer_order_summary() -> DataFrame:
    """Publish customer-level order metrics."""
    spark = get_spark_session()

    order_fact_dataframe = spark.read.table(
        order_fact_definition.dataset_name,
    )

    transformer = CustomerOrderSummaryTransformer()

    return transformer.transform(
        order_fact_dataframe,
    )
