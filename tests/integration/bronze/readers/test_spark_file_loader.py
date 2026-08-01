"""Integration tests for the Spark file loader."""

from pathlib import Path

from pyspark.sql import SparkSession

from enterprise_lakehouse.bronze.readers import SparkFileLoader


def write_csv_fixture(path: Path) -> None:
    """Write a small CSV source file for the integration test."""
    path.write_text(
        "order_id,customer_name,amount\n1,Ana,125.50\n2,Carlo,250.00\n",
        encoding="utf-8",
    )


def test_spark_file_loader_reads_real_csv_file(
    tmp_path: Path,
    spark: SparkSession,
) -> None:
    """The loader should read a CSV file into a real Spark DataFrame."""
    source_path = tmp_path / "sales_orders.csv"
    write_csv_fixture(source_path)

    loader = SparkFileLoader(spark=spark)

    dataframe = loader(
        path=source_path.as_uri(),
        file_format="csv",
        options={
            "header": "true",
            "inferSchema": "true",
        },
    )

    rows = dataframe.orderBy("order_id").collect()

    assert dataframe.columns == [
        "order_id",
        "customer_name",
        "amount",
    ]
    assert len(rows) == 2
    assert rows[0]["order_id"] == 1
    assert rows[0]["customer_name"] == "Ana"
    assert rows[0]["amount"] == 125.5
    assert rows[1]["order_id"] == 2
