"""Tests for configuration loading and validation."""

from pathlib import Path

import pytest

from enterprise_lakehouse.common.config import (
    ConfigurationFileNotFoundError,
    ConfigurationParseError,
    ConfigurationValidationError,
    load_settings,
)


def test_load_settings_returns_valid_application_settings(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "dev.yaml"
    config_file.write_text(
        """
environment: dev
application_name: enterprise-azure-lakehouse

storage:
  landing_path: abfss://landing@example.dfs.core.windows.net/
  bronze_path: abfss://bronze@example.dfs.core.windows.net/
  silver_path: abfss://silver@example.dfs.core.windows.net/
  gold_path: abfss://gold@example.dfs.core.windows.net/
  quarantine_path: abfss://quarantine@example.dfs.core.windows.net/
  checkpoint_path: abfss://checkpoints@example.dfs.core.windows.net/
  schema_location_path: abfss://schemas@example.dfs.core.windows.net/

catalog:
  catalog_name: dev_sales_lakehouse
""".strip(),
        encoding="utf-8",
    )

    settings = load_settings(config_file)

    assert settings.environment == "dev"
    assert settings.application_name == "enterprise-azure-lakehouse"
    assert settings.catalog.catalog_name == "dev_sales_lakehouse"
    assert settings.catalog.bronze_schema == "bronze"
    assert settings.logging.level == "INFO"


def test_load_settings_raises_for_missing_file(
    tmp_path: Path,
) -> None:
    missing_file = tmp_path / "missing.yaml"

    with pytest.raises(
        ConfigurationFileNotFoundError,
        match="does not exist",
    ):
        load_settings(missing_file)


def test_load_settings_raises_for_empty_file(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "empty.yaml"
    config_file.write_text("", encoding="utf-8")

    with pytest.raises(
        ConfigurationParseError,
        match="empty",
    ):
        load_settings(config_file)


def test_load_settings_raises_for_non_mapping_root(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "list.yaml"
    config_file.write_text(
        "- dev\n- prod\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigurationParseError,
        match="root must be a mapping",
    ):
        load_settings(config_file)


def test_load_settings_raises_for_invalid_environment(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "invalid-environment.yaml"
    config_file.write_text(
        """
environment: staging
application_name: enterprise-azure-lakehouse

storage:
  landing_path: landing
  bronze_path: bronze
  silver_path: silver
  gold_path: gold
  quarantine_path: quarantine
  checkpoint_path: checkpoints
  schema_location_path: schemas

catalog:
  catalog_name: staging_sales_lakehouse
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationValidationError):
        load_settings(config_file)


def test_load_settings_rejects_unknown_fields(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "unknown-field.yaml"
    config_file.write_text(
        """
environment: dev
application_name: enterprise-azure-lakehouse
unexpected_setting: should-fail

storage:
  landing_path: landing
  bronze_path: bronze
  silver_path: silver
  gold_path: gold
  quarantine_path: quarantine
  checkpoint_path: checkpoints
  schema_location_path: schemas

catalog:
  catalog_name: dev_sales_lakehouse
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationValidationError):
        load_settings(config_file)
