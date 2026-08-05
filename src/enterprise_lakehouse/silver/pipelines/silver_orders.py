"""Lakeflow declarative Silver orders datasets."""

from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from enterprise_lakehouse.common.metadata.yaml_repository import (
    YamlMetadataRepository,
)
from enterprise_lakehouse.silver.expectations import ExpectationRuleFactory
from enterprise_lakehouse.silver.metadata import (
    DeduplicationRuleFactory,
    StandardizationRuleFactory,
)
from enterprise_lakehouse.silver.pipelines import SilverPipeline
from enterprise_lakehouse.silver.processors import (
    DeduplicationProcessor,
    StandardizationProcessor,
)
from enterprise_lakehouse.silver.quarantine import (
    QuarantineRuleFactory,
    build_quarantine_table_name,
)

SOURCE_ID = "sales_orders"
METADATA_PATH = "/Volumes/workspace/landing/source_files/config/sources.yaml"
STANDARDIZED_VIEW = "_silver_orders_standardized"

repository = YamlMetadataRepository(METADATA_PATH)
metadata = repository.get(SOURCE_ID)

standardization_rules = StandardizationRuleFactory().build(
    metadata.standardization,
)

deduplication_rule = DeduplicationRuleFactory(
    watermark_delay="10 minutes",
).build(metadata)

expectation_rules = ExpectationRuleFactory().build(
    metadata.data_quality,
)

all_expectation_rules = {
    **expectation_rules.retain,
    **expectation_rules.drop,
}

quarantine_predicate = QuarantineRuleFactory().build(
    expectation_rules.drop,
)

if metadata.target.silver_table is None:
    raise ValueError(
        "silver_table is required for the Silver orders pipeline.",
    )

silver_table_name = metadata.target.silver_table

quarantine_table_name = build_quarantine_table_name(
    silver_table_name,
)

quarantine_table_identifier = (
    f"{metadata.target.catalog_name}.{metadata.target.quarantine_schema}.{quarantine_table_name}"
)


def get_spark_session() -> SparkSession:
    """Return the active Spark session for the Silver pipeline."""
    spark = SparkSession.getActiveSession()

    if spark is None:
        raise RuntimeError(
            "No active Spark session is available for the Silver pipeline.",
        )

    return spark


@dp.temporary_view(
    name=STANDARDIZED_VIEW,
)
@dp.expect_all(  # type: ignore[attr-defined]
    all_expectation_rules,
)
def standardized_orders() -> DataFrame:
    """Standardize, deduplicate, and classify orders for routing."""
    spark = get_spark_session()

    source_table = (
        f"{metadata.target.catalog_name}."
        f"{metadata.target.bronze_schema}."
        f"{metadata.target.bronze_table}"
    )

    source_dataframe = spark.readStream.table(source_table)

    pipeline = SilverPipeline(
        processors=(
            StandardizationProcessor(
                rules=standardization_rules,
            ),
            DeduplicationProcessor(
                rule=deduplication_rule,
            ),
        ),
    )

    standardized_dataframe = pipeline.run(source_dataframe)

    return standardized_dataframe.withColumn(
        "_is_quarantined",
        F.coalesce(
            F.expr(quarantine_predicate),
            F.lit(True),
        ),
    )


@dp.table(
    name=silver_table_name,
    comment="Typed, standardized, deduplicated, and validated sales orders.",
)
def silver_orders() -> DataFrame:
    """Publish trusted Silver orders."""
    spark = get_spark_session()

    return (
        spark.readStream.table(STANDARDIZED_VIEW)
        .filter(~F.col("_is_quarantined"))
        .drop("_is_quarantined")
    )


@dp.table(
    name=quarantine_table_identifier,
    comment="Invalid Silver orders preserved for investigation and recovery.",
)
def silver_orders_quarantine() -> DataFrame:
    """Publish orders failing enforced data-quality rules."""
    spark = get_spark_session()

    return (
        spark.readStream.table(STANDARDIZED_VIEW)
        .filter(F.col("_is_quarantined"))
        .withColumn(
            "_quarantine_reason",
            F.lit("failed_enforced_data_quality_rule"),
        )
        .withColumn(
            "_quarantine_source_id",
            F.lit(metadata.source_id),
        )
        .withColumn(
            "_quarantined_at",
            F.current_timestamp(),
        )
    )
