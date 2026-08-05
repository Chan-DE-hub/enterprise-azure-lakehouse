"""Factory for Silver standardization rules."""

from enterprise_lakehouse.common.metadata.models import (
    StandardizationMetadata,
)
from enterprise_lakehouse.silver.models import StandardizationRule


class StandardizationRuleFactory:
    """Create immutable standardization rules from typed metadata."""

    def build(
        self,
        metadata: StandardizationMetadata,
    ) -> tuple[StandardizationRule, ...]:
        """Convert typed metadata into reusable standardization rules."""
        return tuple(
            StandardizationRule(
                source_column=column.source_column,
                target_column=column.target_column,
                data_type=column.data_type,
                trim=column.trim,
                text_case=column.text_case,
                parse_format=column.parse_format,
            )
            for column in metadata.columns
        )
