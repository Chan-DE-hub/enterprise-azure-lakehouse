"""Generic Silver standardization processor."""

from collections.abc import Iterable

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F

from enterprise_lakehouse.silver.models import (
    StandardizationRule,
    TextCase,
)


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
            expression = self.build_expression(rule)

            result = result.withColumn(
                rule.resolved_target_column,
                expression,
            )

            if rule.resolved_target_column != rule.source_column:
                result = result.drop(rule.source_column)

        return result

    def build_expression(
        self,
        rule: StandardizationRule,
    ) -> Column:
        """Build the Spark expression for one standardization rule."""
        expression = F.col(rule.source_column)

        if rule.trim:
            expression = F.trim(expression)

        if rule.text_case is TextCase.LOWER:
            expression = F.lower(expression)
        elif rule.text_case is TextCase.UPPER:
            expression = F.upper(expression)

        if rule.parse_format is not None:
            if rule.data_type == "timestamp":
                return F.to_timestamp(
                    expression,
                    rule.parse_format,
                )

            if rule.data_type == "date":
                return F.to_date(
                    expression,
                    rule.parse_format,
                )

        return expression.cast(rule.data_type)
