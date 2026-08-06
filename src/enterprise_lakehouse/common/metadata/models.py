"""Typed metadata models for lakehouse pipeline definitions."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SourceType(StrEnum):
    """Supported source-system categories."""

    FILE = "file"
    DATABASE = "database"
    REST_API = "rest_api"
    EVENT_HUB = "event_hub"
    KAFKA = "kafka"


class LoadType(StrEnum):
    """Supported source loading patterns."""

    FULL = "full"
    INCREMENTAL = "incremental"
    CDC = "cdc"
    STREAMING = "streaming"


class SilverProcessingStrategy(StrEnum):
    """Supported Silver processing strategies."""

    APPEND = "append"
    AUTO_CDC = "auto_cdc"


class FileFormat(StrEnum):
    """Supported landing-file formats."""

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    AVRO = "avro"


class DataClassification(StrEnum):
    """High-level data sensitivity classification."""

    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class TextCase(StrEnum):
    """Supported text-case normalization strategies."""

    NONE = "none"
    LOWER = "lower"
    UPPER = "upper"


class ExpectationAction(StrEnum):
    """Supported Lakeflow expectation actions."""

    RETAIN = "retain"
    DROP = "drop"


class MetadataModel(BaseModel):
    """Base model for strict metadata validation."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )


class ProcessingMetadata(MetadataModel):
    """Silver processing configuration for one source."""

    strategy: SilverProcessingStrategy = SilverProcessingStrategy.APPEND


class StandardizationColumnMetadata(MetadataModel):
    """Technical standardization configuration for one source column."""

    source_column: str = Field(min_length=1)
    target_column: str | None = None
    data_type: str = Field(min_length=1)

    trim: bool = False
    text_case: TextCase = TextCase.NONE
    parse_format: str | None = None

    @property
    def resolved_target_column(self) -> str:
        """Return the configured target column or preserve the source name."""
        return self.target_column or self.source_column


class StandardizationMetadata(MetadataModel):
    """Silver standardization configuration for one source."""

    columns: tuple[StandardizationColumnMetadata, ...] = ()


class SourceLocation(MetadataModel):
    """Physical or logical location of a source dataset."""

    database: str | None = None
    schema_name: str | None = None
    object_name: str
    path: str | None = None
    topic_name: str | None = None


class TargetMetadata(MetadataModel):
    """Lakehouse target definitions for a source dataset."""

    catalog_name: str
    bronze_schema: str = "bronze"
    silver_schema: str = "silver"
    gold_schema: str = "gold"
    quarantine_schema: str = "quarantine"

    bronze_table: str
    silver_table: str | None = None
    gold_table: str | None = None

    checkpoint_path: str | None = None
    schema_location_path: str | None = None


class GovernanceMetadata(MetadataModel):
    """Ownership, classification, and operational governance metadata."""

    business_domain: str
    owner: str
    data_classification: DataClassification = DataClassification.INTERNAL
    tags: tuple[str, ...] = ()
    sla_minutes: int | None = Field(default=None, gt=0)


class ExpectationMetadata(MetadataModel):
    """Configuration for one Silver data-quality expectation."""

    name: str = Field(min_length=1)
    constraint: str = Field(min_length=1)
    action: ExpectationAction


class DataQualityMetadata(MetadataModel):
    """Data-quality expectations configured for one source."""

    expectations: tuple[ExpectationMetadata, ...] = ()


class SourceMetadata(MetadataModel):
    """Complete metadata contract for one source dataset."""

    source_id: str = Field(min_length=1)
    source_system: str = Field(min_length=1)
    source_type: SourceType
    load_type: LoadType

    location: SourceLocation
    target: TargetMetadata
    governance: GovernanceMetadata

    primary_keys: tuple[str, ...] = ()
    watermark_column: str | None = None
    sequence_column: str | None = None
    operation_column: str | None = None
    event_timestamp_column: str | None = None
    file_format: FileFormat | None = None

    data_quality: DataQualityMetadata = Field(
        default_factory=DataQualityMetadata,
    )

    reader_options: dict[str, str | int | float | bool] = Field(
        default_factory=dict,
    )

    processing: ProcessingMetadata = Field(
        default_factory=ProcessingMetadata,
    )

    standardization: StandardizationMetadata = Field(
        default_factory=StandardizationMetadata,
    )

    enabled: bool = True
    priority: int = Field(default=100, ge=1, le=999)

    @model_validator(mode="after")
    def validate_loading_strategy(self) -> SourceMetadata:
        """Validate fields required by the selected ingestion strategy."""

        if self.source_type is SourceType.FILE and self.file_format is None:
            raise ValueError(
                "file_format is required when source_type is 'file'",
            )

        if self.source_type is SourceType.FILE and self.location.path is None:
            raise ValueError(
                "path is required when source_type is 'file'",
            )

        if self.load_type is LoadType.INCREMENTAL and self.watermark_column is None:
            raise ValueError(
                "watermark_column is required for incremental loading",
            )

        if self.load_type is LoadType.CDC:
            if not self.primary_keys:
                raise ValueError(
                    "primary_keys are required for CDC loading",
                )

            if self.sequence_column is None:
                raise ValueError(
                    "sequence_column is required for CDC loading",
                )

            if self.operation_column is None:
                raise ValueError(
                    "operation_column is required for CDC loading",
                )

        if self.load_type is LoadType.STREAMING and self.target.checkpoint_path is None:
            raise ValueError(
                "checkpoint_path is required for streaming loading",
            )

        if (
            self.source_type
            in {
                SourceType.EVENT_HUB,
                SourceType.KAFKA,
            }
            and self.location.topic_name is None
        ):
            raise ValueError(
                "topic_name is required for Event Hub or Kafka sources",
            )

        if self.processing.strategy is SilverProcessingStrategy.AUTO_CDC:
            if not self.primary_keys:
                raise ValueError(
                    "primary_keys are required for AUTO CDC processing",
                )

            if self.sequence_column is None:
                raise ValueError(
                    "sequence_column is required for AUTO CDC processing",
                )

            if self.operation_column is None:
                raise ValueError(
                    "operation_column is required for AUTO CDC processing",
                )

        return self
