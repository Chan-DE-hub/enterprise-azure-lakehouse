"""Factory for building Silver quarantine predicates."""

from collections.abc import Mapping


class QuarantineRuleFactory:
    """Build SQL predicates used to identify invalid Silver records."""

    def build(self, drop_rules: Mapping[str, str]) -> str:
        """Return a predicate that matches rows failing any enforced rule.

        Args:
            drop_rules: Mapping of rule names to valid-record SQL expressions.

        Returns:
            A SQL predicate identifying invalid records. When no enforced rules
            exist, returns ``FALSE`` so that no rows are quarantined.
        """
        if not drop_rules:
            return "FALSE"

        valid_record_predicate = " AND ".join(
            f"({expression})" for expression in drop_rules.values()
        )

        return f"NOT({valid_record_predicate})"
