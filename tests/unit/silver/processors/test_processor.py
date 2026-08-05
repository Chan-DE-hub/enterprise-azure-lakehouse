"""Tests for the Silver processor contract."""

from inspect import signature

from enterprise_lakehouse.silver.models import StandardizationRule
from enterprise_lakehouse.silver.processors.processor import Processor
from enterprise_lakehouse.silver.processors.standardization_processor import (
    StandardizationProcessor,
)


def test_processor_contract_exposes_process_signature() -> None:
    """The processor contract must expose a standard process operation."""
    parameters = signature(Processor.process).parameters

    assert list(parameters) == [
        "self",
        "dataframe",
    ]


def test_standardization_processor_satisfies_contract() -> None:
    """The generic standardization processor must satisfy the protocol."""
    processor: Processor = StandardizationProcessor(
        rules=(
            StandardizationRule(
                source_column="order_id",
                data_type="long",
            ),
        )
    )

    assert isinstance(
        processor,
        StandardizationProcessor,
    )
