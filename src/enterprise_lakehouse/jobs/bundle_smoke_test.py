"""Databricks bundle deployment smoke test."""

from datetime import UTC, datetime


def main() -> None:
    """Print basic runtime information to verify job execution."""
    executed_at = datetime.now(UTC).isoformat()

    print("Databricks bundle smoke test succeeded.")
    print(f"Executed at: {executed_at}")


if __name__ == "__main__":
    main()
