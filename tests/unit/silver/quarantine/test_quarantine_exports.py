"""Tests for Silver quarantine package exports."""

from enterprise_lakehouse.silver.quarantine import QuarantineRuleFactory


def test_quarantine_package_exports_rule_factory() -> None:
    """The quarantine package should expose its public rule factory."""
    assert QuarantineRuleFactory.__name__ == "QuarantineRuleFactory"
