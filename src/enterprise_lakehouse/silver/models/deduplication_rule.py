"""Models for Silver deduplication rules."""

from pydantic import BaseModel, ConfigDict, Field


class DeduplicationRule(BaseModel):
    """Reusable streaming deduplication rule."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    keys: tuple[str, ...] = Field(min_length=1)
    event_time_column: str = Field(min_length=1)
    watermark_delay: str = Field(min_length=1)
