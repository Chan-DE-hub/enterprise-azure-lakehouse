"""Tests for cached metadata repository."""

from enterprise_lakehouse.common.metadata import (
    CachedMetadataRepository,
    MetadataRepository,
)


class FakeRepository(MetadataRepository):
    """Fake repository used for testing."""

    def __init__(self) -> None:
        self.calls = 0

    def load(self):
        self.calls += 1
        return []


def test_repository_is_called_only_once() -> None:
    repository = FakeRepository()

    cached = CachedMetadataRepository(repository)

    cached.load()
    cached.load()
    cached.load()

    assert repository.calls == 1


def test_clear_cache_forces_reload() -> None:
    repository = FakeRepository()

    cached = CachedMetadataRepository(repository)

    cached.load()

    cached.clear_cache()

    cached.load()

    assert repository.calls == 2
