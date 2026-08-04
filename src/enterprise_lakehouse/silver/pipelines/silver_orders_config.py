"""Configuration for Silver orders processing."""

from enterprise_lakehouse.silver.models import StandardizationRule


def build_standardization_rules() -> tuple[StandardizationRule, ...]:
    """Return ordered standardization rules for Silver orders."""
    return (
        StandardizationRule(
            column_name="order_id",
            data_type="long",
        ),
        StandardizationRule(
            column_name="customer_id",
            data_type="long",
        ),
        StandardizationRule(
            column_name="order_total",
            data_type="decimal(18,2)",
        ),
        StandardizationRule(
            column_name="modified_at",
            data_type="timestamp",
        ),
        StandardizationRule(
            column_name="order_status",
            data_type="string",
            trim=True,
            lowercase=True,
        ),
    )
