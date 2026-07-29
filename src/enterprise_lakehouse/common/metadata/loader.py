"""Metadata loaders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class MetadataLoader:
    """Loads raw metadata from YAML files."""

    def load_yaml(
        self,
        path: str | Path,
    ) -> dict[str, Any]:
        """Load and return a YAML document as a dictionary."""

        yaml_path = Path(path)

        with yaml_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            raw_document: Any = yaml.safe_load(file)

        if raw_document is None:
            return {}

        if not isinstance(raw_document, dict):
            raise ValueError(
                "Metadata YAML root must be a mapping.",
            )

        return raw_document
