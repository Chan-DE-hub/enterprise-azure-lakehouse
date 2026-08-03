"""Tests for the Bronze writer contract."""

from inspect import signature

from enterprise_lakehouse.bronze.writers.bronze_delta_writer import (
    BronzeDeltaWriter,
)
from enterprise_lakehouse.bronze.writers.bronze_writer import BronzeWriter


def test_bronze_writer_contract_exposes_write_signature() -> None:
    """The writer contract must define the standard Bronze write operation."""
    parameters = signature(BronzeWriter.write).parameters

    assert list(parameters) == [
        "self",
        "dataframe",
        "table_name",
        "mode",
        "options",
    ]


def test_bronze_delta_writer_satisfies_writer_contract() -> None:
    """The batch Delta writer must satisfy the Bronze writer protocol."""
    writer: BronzeWriter = BronzeDeltaWriter()

    assert isinstance(writer, BronzeDeltaWriter)
