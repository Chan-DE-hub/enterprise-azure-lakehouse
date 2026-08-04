"""Tests for the Silver processor contract."""

from inspect import signature

from enterprise_lakehouse.silver.processors.orders_standardization_processor import (
    OrdersStandardizationProcessor,
)
from enterprise_lakehouse.silver.processors.processor import Processor


def test_processor_contract_exposes_process_signature() -> None:
    """The processor contract must expose a standard process operation."""
    parameters = signature(Processor.process).parameters

    assert list(parameters) == [
        "self",
        "dataframe",
    ]


def test_orders_standardization_processor_satisfies_contract() -> None:
    """The orders standardization processor must satisfy the protocol."""
    processor: Processor = OrdersStandardizationProcessor()

    assert isinstance(
        processor,
        OrdersStandardizationProcessor,
    )
