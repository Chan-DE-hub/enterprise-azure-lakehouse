"""Bronze file reader implementation."""

from typing import Any

from enterprise_lakehouse.bronze.models import PipelineContext
from enterprise_lakehouse.bronze.readers.base_reader import BaseReader
from enterprise_lakehouse.bronze.readers.file_loader import FileLoader
from enterprise_lakehouse.common.metadata.models import SourceMetadata


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
        """Load a file using canonical source metadata."""
        # Reserved for future run-scoped logging, tracing, and metrics.
        del context

        path = metadata.location.path

        if path is None:
            raise ValueError(
                f"Missing source path for file source: {metadata.source_id}",
            )

        file_format = metadata.file_format

        if file_format is None:
            raise ValueError(
                f"Missing file format for file source: {metadata.source_id}",
            )

        return self._loader(
            path=path,
            file_format=file_format.value,
            options=dict(metadata.reader_options),
        )
