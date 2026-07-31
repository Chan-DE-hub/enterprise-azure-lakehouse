"""Bronze file reader implementation."""

from typing import Any

from enterprise_lakehouse.bronze.models import (
    PipelineContext,
    SourceMetadata,
)
from enterprise_lakehouse.bronze.readers.base_reader import BaseReader
from enterprise_lakehouse.bronze.readers.file_loader import FileLoader


class FileReader(BaseReader):
    """Reader responsible for loading file-based sources."""

    def __init__(
        self,
        *,
        loader: FileLoader,
    ) -> None:
        """Initialize the file reader."""
        self._loader = loader

    @property
    def source_type(self) -> str:
        """Return the source type handled by this reader."""
        return "file"

    def read(
        self,
        *,
        context: PipelineContext,
        metadata: SourceMetadata,
    ) -> Any:
        """Load a file using the configured loader."""
        # Reserved for future run-scoped logging, tracing, and metrics.
        del context

        options = dict(metadata.options)

        if "path" not in options:
            raise ValueError("Missing required metadata option: path")

        if "format" not in options:
            raise ValueError("Missing required metadata option: format")

        path = options.pop("path")
        file_format = options.pop("format")

        return self._loader(
            path=path,
            file_format=file_format,
            options=options,
        )
