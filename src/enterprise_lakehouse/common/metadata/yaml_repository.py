"""YAML implementation of the metadata repository."""

from __future__ import annotations

from pathlib import Path

import yaml

from enterprise_lakehouse.common.metadata.models import SourceMetadata
from enterprise_lakehouse.common.metadata.repository import MetadataRepository


class YamlMetadataRepository(MetadataRepository):
    """Loads metadata definitions from a YAML file."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def load(self) -> list[SourceMetadata]:
        """Load metadata definitions from YAML."""

        with self._path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = yaml.safe_load(file)

        sources = data.get("sources", [])

        return [SourceMetadata.model_validate(source) for source in sources]
