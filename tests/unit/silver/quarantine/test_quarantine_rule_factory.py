"""Tests for the Silver quarantine rule factory."""

from enterprise_lakehouse.silver.quarantine.quarantine_rule_factory import (
    QuarantineRuleFactory,
)


def test_factory_builds_invalid_record_predicate() -> None:
    """The factory should quarantine rows failing any enforced rule."""
    drop_rules = {
        "valid_order_id": "order_id IS NOT NULL",
        "valid_customer_id": "customer_id IS NOT NULL",
        "positive_order_total": "order_total >= 0",
    }

    predicate = QuarantineRuleFactory().build(drop_rules)

    assert predicate == (
        "NOT((order_id IS NOT NULL) AND (customer_id IS NOT NULL) AND (order_total >= 0))"
    )


def test_factory_returns_false_when_no_drop_rules_exist() -> None:
    """No rows should be quarantined when no enforced rules exist."""
    predicate = QuarantineRuleFactory().build({})

    assert predicate == "FALSE"
