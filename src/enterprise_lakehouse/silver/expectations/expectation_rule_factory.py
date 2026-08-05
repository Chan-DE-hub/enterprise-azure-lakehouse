"""Factory for grouped Silver expectation rules."""

from enterprise_lakehouse.common.metadata.models import (
    DataQualityMetadata,
    ExpectationAction,
)
from enterprise_lakehouse.silver.expectations.expectation_rules import (
    ExpectationRules,
)


class ExpectationRuleFactory:
    """Convert typed data-quality metadata into Lakeflow rule groups."""

    def build(
        self,
        metadata: DataQualityMetadata,
    ) -> ExpectationRules:
        """Group expectations according to their configured action."""
        retain: dict[str, str] = {}
        drop: dict[str, str] = {}

        for expectation in metadata.expectations:
            if expectation.action is ExpectationAction.RETAIN:
                retain[expectation.name] = expectation.constraint
            elif expectation.action is ExpectationAction.DROP:
                drop[expectation.name] = expectation.constraint

        return ExpectationRules(
            retain=retain,
            drop=drop,
        )
