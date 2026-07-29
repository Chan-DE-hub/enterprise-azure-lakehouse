"""Business validation rules for metadata."""

from __future__ import annotations

from collections import Counter

from enterprise_lakehouse.common.metadata.models import SourceMetadata


class MetadataRules:
    """Enterprise metadata validation rules."""

    @staticmethod
    def validate_unique_source_ids(
        metadata: list[SourceMetadata],
    ) -> None:
        """Ensure every source_id is unique."""

        counts = Counter(item.source_id for item in metadata)

        duplicates = [source_id for source_id, count in counts.items() if count > 1]

        if duplicates:
            raise ValueError(
                f"Duplicate source_id values found: {duplicates}",
            )

    @staticmethod
    def validate_unique_bronze_tables(
        metadata: list[SourceMetadata],
    ) -> None:
        """Ensure bronze table names are unique."""

        counts = Counter(item.target.bronze_table for item in metadata)

        duplicates = [table for table, count in counts.items() if count > 1]

        if duplicates:
            raise ValueError(
                f"Duplicate bronze tables found: {duplicates}",
            )
