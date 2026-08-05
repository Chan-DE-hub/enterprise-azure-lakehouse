"""Models for Silver standardization rules."""

from pydantic import BaseModel, ConfigDict, Field

from enterprise_lakehouse.common.metadata.models import TextCase


class StandardizationRule(BaseModel):
    """Reusable technical standardization rule."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    source_column: str = Field(min_length=1)
    target_column: str | None = None
    data_type: str = Field(min_length=1)

    trim: bool = False
    text_case: TextCase = TextCase.NONE
    parse_format: str | None = None

    @property
    def resolved_target_column(self) -> str:
        """Return the configured target name or preserve the source name."""
        return self.target_column or self.source_column
