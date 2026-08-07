"""Reusable Gold dataset definitions."""

from dataclasses import dataclass
from enum import StrEnum


class GoldDatasetType(StrEnum):
    """Supported Gold dataset categories."""

    FACT = "fact"
    DIMENSION = "dimension"


@dataclass(frozen=True, slots=True)
class GoldDefinition:
    """Immutable business contract for one Gold dataset."""

    dataset_name: str
    dataset_type: GoldDatasetType
    source_tables: tuple[str, ...]
    target_table: str
    grain: str
    business_domain: str

    def __post_init__(self) -> None:
        """Validate required Gold business-contract fields."""
        if not self.dataset_name.strip():
            raise ValueError(
                "dataset_name must not be empty",
            )

        if not self.source_tables:
            raise ValueError(
                "source_tables must contain at least one source",
            )

        if any(not source_table.strip() for source_table in self.source_tables):
            raise ValueError(
                "source_tables must not contain empty values",
            )

        if not self.target_table.strip():
            raise ValueError(
                "target_table must not be empty",
            )

        if not self.grain.strip():
            raise ValueError(
                "grain must not be empty",
            )

        if not self.business_domain.strip():
            raise ValueError(
                "business_domain must not be empty",
            )
