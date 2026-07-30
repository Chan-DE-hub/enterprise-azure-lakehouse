"""Tests for the Bronze reader contract."""

from typing import Any

import pytest

from enterprise_lakehouse.bronze.readers import BaseReader


class IncompleteReader(BaseReader):
    """Reader intentionally missing required abstract members."""


class FakeReader(BaseReader):
    """Minimal concrete reader used to test the contract."""

    @property
    def source_type(self) -> str:
        return "fake"

    def read(self, *, options: dict[str, Any]) -> Any:
        return options


def test_base_reader_cannot_be_instantiated() -> None:
    """The abstract base contract must not be directly instantiated."""
    with pytest.raises(TypeError):
        BaseReader()  # type: ignore[abstract]


def test_incomplete_reader_cannot_be_instantiated() -> None:
    """A subclass missing required members must remain abstract."""
    with pytest.raises(TypeError):
        IncompleteReader()  # type: ignore[abstract]


def test_concrete_reader_exposes_source_type() -> None:
    """A valid reader must expose its source type."""
    reader = FakeReader()

    assert reader.source_type == "fake"


def test_concrete_reader_returns_source_data() -> None:
    """A valid reader must implement the read operation."""
    reader = FakeReader()
    options = {"path": "/Volumes/raw/orders"}

    result = reader.read(options=options)

    assert result == options
