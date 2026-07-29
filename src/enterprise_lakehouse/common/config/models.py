"""Typed configuration models for the enterprise lakehouse platform."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EnvironmentName = Literal["dev", "uat", "prod"]


class StorageSettings(BaseModel):
    """Storage locations used by lakehouse pipelines."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    landing_path: str = Field(min_length=1)
    bronze_path: str = Field(min_length=1)
    silver_path: str = Field(min_length=1)
    gold_path: str = Field(min_length=1)
    quarantine_path: str = Field(min_length=1)
    checkpoint_path: str = Field(min_length=1)
    schema_location_path: str = Field(min_length=1)


class CatalogSettings(BaseModel):
    """Unity Catalog names used by the platform."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    catalog_name: str = Field(min_length=1)
    bronze_schema: str = Field(default="bronze", min_length=1)
    silver_schema: str = Field(default="silver", min_length=1)
    gold_schema: str = Field(default="gold", min_length=1)
    config_schema: str = Field(default="config", min_length=1)
    audit_schema: str = Field(default="audit", min_length=1)
    quarantine_schema: str = Field(default="quarantine", min_length=1)


class LoggingSettings(BaseModel):
    """Application logging configuration."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    level: str = Field(default="INFO", min_length=1)


class ApplicationSettings(BaseModel):
    """Root configuration object for the lakehouse platform."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    environment: EnvironmentName
    application_name: str = Field(min_length=1)
    storage: StorageSettings
    catalog: CatalogSettings
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
