"""Lakeflow declarative Silver customers AUTO CDC SCD Type 1 datasets."""

from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from enterprise_lakehouse.common.metadata.yaml_repository import (
    YamlMetadataRepository,
)
from enterprise_lakehouse.silver.expectations import ExpectationRuleFactory
from enterprise_lakehouse.silver.metadata import StandardizationRuleFactory
from enterprise_lakehouse.silver.pipelines import SilverPipeline
from enterprise_lakehouse.silver.processors import StandardizationProcessor
from enterprise_lakehouse.silver.quarantine import (
    QuarantineRuleFactory,
    build_quarantine_table_name,
)

SOURCE_ID = "customers_cdc"
METADATA_PATH = "/Volumes/workspace/landing/source_files/config/sources.yaml"

STAGED_VIEW = "_silver_customers_cdc_staged"
VALID_VIEW = "_silver_customers_cdc_valid"

repository = YamlMetadataRepository(METADATA_PATH)
metadata = repository.get(SOURCE_ID)

standardization_rules = StandardizationRuleFactory().build(
    metadata.standardization,
)

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
        "silver_table is required for the Customers AUTO CDC pipeline.",
    )

if metadata.sequence_column is None:
    raise ValueError(
        "sequence_column is required for the Customers AUTO CDC pipeline.",
    )

if metadata.operation_column is None:
    raise ValueError(
        "operation_column is required for the Customers AUTO CDC pipeline.",
    )

silver_table_name = metadata.target.silver_table
sequence_column = metadata.sequence_column
operation_column = metadata.operation_column

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
    name=STAGED_VIEW,
)
@dp.expect_all(  # type: ignore[attr-defined]
    all_expectation_rules,
)
def staged_customers_cdc() -> DataFrame:
    """Standardize CDC events and classify invalid records."""
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


@dp.temporary_view(
    name=VALID_VIEW,
)
def valid_customers_cdc() -> DataFrame:
    """Expose valid CDC events for the AUTO CDC flow."""
    spark = get_spark_session()

    return (
        spark.readStream.table(STAGED_VIEW)
        .filter(~F.col("_is_quarantined"))
        .drop("_is_quarantined")
    )


@dp.table(
    name=quarantine_table_identifier,
    comment="Invalid customer CDC events preserved for investigation and recovery.",
)
def silver_customers_quarantine() -> DataFrame:
    """Publish customer CDC events failing enforced quality rules."""
    spark = get_spark_session()

    return (
        spark.readStream.table(STAGED_VIEW)
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


dp.create_streaming_table(
    name=silver_table_name,
    comment="Current-state customers maintained using AUTO CDC SCD Type 1.",
)

dp.create_auto_cdc_flow(
    target=silver_table_name,
    source=VALID_VIEW,
    keys=list(metadata.primary_keys),
    sequence_by=sequence_column,
    apply_as_deletes=f"{operation_column} = 'DELETE'",
    except_column_list=[
        operation_column,
        "_rescued_data",
    ],
    stored_as_scd_type="1",
    name="customers_auto_cdc_scd1",
)
