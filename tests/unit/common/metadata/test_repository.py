"""Tests for metadata repository abstractions."""

import pytest

from enterprise_lakehouse.common.metadata.repository import MetadataRepository


def test_metadata_repository_is_abstract() -> None:
    with pytest.raises(TypeError):
        MetadataRepository()
