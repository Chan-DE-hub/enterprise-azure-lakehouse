"""Tests for metadata repository decorators."""

from enterprise_lakehouse.common.metadata import (
    MetadataRepository,
)
from enterprise_lakehouse.common.metadata.decorators import (
    MetadataRepositoryDecorator,
)


class FakeRepository(MetadataRepository):
    def load(self):
        return []


def test_base_decorator_delegates_to_repository() -> None:
    repository = FakeRepository()

    decorator = MetadataRepositoryDecorator(
        repository,
    )

    assert decorator.load() == []
