"""Models for Silver standardization rules."""

from pydantic import BaseModel, ConfigDict, Field


class StandardizationRule(BaseModel):
    """Reusable column-standardization configuration."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    column_name: str = Field(min_length=1)
    data_type: str = Field(min_length=1)

    trim: bool = False
    lowercase: bool = False
