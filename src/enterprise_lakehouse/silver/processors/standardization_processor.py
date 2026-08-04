"""Generic Silver standardization processor."""

from collections.abc import Iterable

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F

from enterprise_lakehouse.silver.models import StandardizationRule


class StandardizationProcessor:
    """Apply ordered column-standardization rules."""

    def __init__(
        self,
        *,
        rules: Iterable[StandardizationRule],
    ) -> None:
        """Initialize the processor with immutable ordered rules."""
        self._rules = tuple(rules)

    def process(self, dataframe: DataFrame) -> DataFrame:
        """Apply configured standardization rules sequentially."""
        result = dataframe

        for rule in self._rules:
            result = result.withColumn(
                rule.column_name,
                self.build_expression(rule),
            )

        return result

    def build_expression(
        self,
        rule: StandardizationRule,
    ) -> Column:
        """Build the Spark expression for one standardization rule."""
        expression = F.col(rule.column_name)

        if rule.trim:
            expression = F.trim(expression)

        if rule.lowercase:
            expression = F.lower(expression)

        return expression.cast(rule.data_type)
