"""Bronze pipeline orchestration."""

from enterprise_lakehouse.bronze.engine import IngestionEngine
from enterprise_lakehouse.bronze.models import (
    BronzeWriteConfig,
    PipelineContext,
)
from enterprise_lakehouse.bronze.writers import BronzeDeltaWriter


class BronzePipeline:
    """Coordinate an end-to-end Bronze ingestion run."""

    def __init__(
        self,
        *,
        ingestion_engine: IngestionEngine,
        writer: BronzeDeltaWriter,
    ) -> None:
        """Initialize the pipeline."""
        self._ingestion_engine = ingestion_engine
        self._writer = writer

    def run(
        self,
        *,
        context: PipelineContext,
        source_name: str,
        write_config: BronzeWriteConfig,
    ) -> None:
        """Execute one Bronze ingestion pipeline."""

        dataframe = self._ingestion_engine.run(
            context=context,
            source_name=source_name,
        )

        self._writer.write(
            dataframe=dataframe,
            table_name=write_config.table_name,
            mode=write_config.mode,
            options=write_config.options,
        )
