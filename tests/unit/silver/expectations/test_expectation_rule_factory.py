"""Tests for the Silver expectation rule factory."""

from enterprise_lakehouse.common.metadata.models import (
    DataQualityMetadata,
    ExpectationAction,
)
from enterprise_lakehouse.silver.expectations.expectation_rule_factory import (
    ExpectationRuleFactory,
)


def test_factory_groups_expectations_by_action() -> None:
    """The factory should group expectation rules by Lakeflow action."""
    metadata = DataQualityMetadata(
        expectations=(
            {
                "name": "valid_order_id",
                "constraint": "order_id IS NOT NULL",
                "action": "drop",
            },
            {
                "name": "valid_customer_id",
                "constraint": "customer_id IS NOT NULL",
                "action": "drop",
            },
            {
                "name": "known_order_status",
                "constraint": "order_status IS NOT NULL",
                "action": "retain",
            },
        )
    )

    rules = ExpectationRuleFactory().build(metadata)

    assert rules.drop == {
        "valid_order_id": "order_id IS NOT NULL",
        "valid_customer_id": "customer_id IS NOT NULL",
    }
    assert rules.retain == {
        "known_order_status": "order_status IS NOT NULL",
    }


def test_factory_returns_empty_groups_when_no_expectations_exist() -> None:
    """The factory should return empty groups when no rules exist."""
    rules = ExpectationRuleFactory().build(DataQualityMetadata())

    assert rules.drop == {}
    assert rules.retain == {}


def test_expectation_action_supports_only_pr28_policies() -> None:
    """PR28 should support only retain and drop policies."""
    assert ExpectationAction.RETAIN.value == "retain"
    assert ExpectationAction.DROP.value == "drop"
