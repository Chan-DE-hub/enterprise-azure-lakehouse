"""Metadata validation."""

from __future__ import annotations

from typing import Any

from enterprise_lakehouse.common.metadata.models import SourceMetadata
from enterprise_lakehouse.common.metadata.rules import MetadataRules


class MetadataValidator:
    """Converts raw metadata into validated models."""

    def validate(
        self,
        document: dict[str, Any],
    ) -> list[SourceMetadata]:
        """Validate raw metadata and apply business rules."""

        sources = document.get(
            "sources",
            [],
        )

        validated_metadata = [SourceMetadata.model_validate(source) for source in sources]

        MetadataRules.validate_unique_source_ids(validated_metadata)
        MetadataRules.validate_unique_bronze_tables(validated_metadata)

        return validated_metadata
