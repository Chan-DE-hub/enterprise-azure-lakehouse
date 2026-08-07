"""Factory for composing reusable Silver definitions."""

from collections.abc import Iterable

from enterprise_lakehouse.common.metadata.models import SourceMetadata
from enterprise_lakehouse.silver.definition import SilverDefinition
from enterprise_lakehouse.silver.expectations import ExpectationRuleFactory
from enterprise_lakehouse.silver.metadata import (
    ProcessingStrategyFactory,
    StandardizationRuleFactory,
)
from enterprise_lakehouse.silver.processors import StandardizationProcessor
from enterprise_lakehouse.silver.quarantine import (
    QuarantineRuleFactory,
    build_quarantine_table_name,
)


class SilverDefinitionFactory:
    """Compose reusable Silver pipeline definitions from source metadata."""

    def __init__(
        self,
        *,
        standardization_factory: StandardizationRuleFactory,
        expectation_factory: ExpectationRuleFactory,
        quarantine_factory: QuarantineRuleFactory,
        processing_strategy_factory: ProcessingStrategyFactory,
    ) -> None:
        """Initialize the definition factory."""
        self._standardization_factory = standardization_factory
        self._expectation_factory = expectation_factory
        self._quarantine_factory = quarantine_factory
        self._processing_strategy_factory = processing_strategy_factory

    def build(
        self,
        *,
        metadata: SourceMetadata,
        additional_processors: Iterable[object] = (),
    ) -> SilverDefinition:
        """Build one reusable Silver definition."""
        if metadata.target.silver_table is None:
            raise ValueError(
                "silver_table is required for Silver processing.",
            )

        standardization_rules = self._standardization_factory.build(
            metadata.standardization,
        )

        expectation_rules = self._expectation_factory.build(
            metadata.data_quality,
        )

        all_expectation_rules = {
            **expectation_rules.retain,
            **expectation_rules.drop,
        }

        quarantine_predicate = self._quarantine_factory.build(
            expectation_rules.drop,
        )

        processing_strategy = self._processing_strategy_factory.build(
            metadata.processing,
        )

        source_table = (
            f"{metadata.target.catalog_name}."
            f"{metadata.target.bronze_schema}."
            f"{metadata.target.bronze_table}"
        )

        quarantine_table_name = build_quarantine_table_name(
            metadata.target.silver_table,
        )

        quarantine_table = (
            f"{metadata.target.catalog_name}."
            f"{metadata.target.quarantine_schema}."
            f"{quarantine_table_name}"
        )

        processors = (
            StandardizationProcessor(
                rules=standardization_rules,
            ),
            *tuple(additional_processors),
        )

        return SilverDefinition(
            source_table=source_table,
            silver_table=metadata.target.silver_table,
            quarantine_table=quarantine_table,
            processors=processors,
            expectation_rules=all_expectation_rules,
            quarantine_predicate=quarantine_predicate,
            processing_strategy=processing_strategy,
        )
