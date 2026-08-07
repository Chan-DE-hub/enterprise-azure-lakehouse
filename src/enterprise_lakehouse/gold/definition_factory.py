"""Factory for composing reusable Gold dataset definitions."""

from enterprise_lakehouse.common.metadata.models import SourceMetadata
from enterprise_lakehouse.gold.definition import (
    GoldDatasetType,
    GoldDefinition,
)


class GoldDefinitionFactory:
    """Compose Gold dataset definitions from trusted Silver metadata."""

    def build(
        self,
        *,
        metadata: SourceMetadata,
        dataset_name: str,
        dataset_type: GoldDatasetType,
        grain: str,
    ) -> GoldDefinition:
        """Build one Gold dataset definition."""
        if metadata.target.silver_table is None:
            raise ValueError(
                "silver_table is required for Gold processing.",
            )

        source_table = (
            f"{metadata.target.catalog_name}."
            f"{metadata.target.silver_schema}."
            f"{metadata.target.silver_table}"
        )

        target_table_name = metadata.target.gold_table or dataset_name

        target_table = (
            f"{metadata.target.catalog_name}.{metadata.target.gold_schema}.{target_table_name}"
        )

        return GoldDefinition(
            dataset_name=dataset_name,
            dataset_type=dataset_type,
            source_tables=(source_table,),
            target_table=target_table,
            grain=grain,
            business_domain=metadata.governance.business_domain,
        )
