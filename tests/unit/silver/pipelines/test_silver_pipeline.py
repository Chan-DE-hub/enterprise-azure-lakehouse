"""Tests for Silver pipeline orchestration."""

from unittest.mock import Mock, call

from enterprise_lakehouse.silver.pipelines.silver_pipeline import SilverPipeline


def test_pipeline_applies_processors_in_order() -> None:
    """The pipeline should apply each processor sequentially."""
    source_dataframe = Mock(name="source_dataframe")
    standardized_dataframe = Mock(name="standardized_dataframe")
    final_dataframe = Mock(name="final_dataframe")

    first_processor = Mock()
    first_processor.process.return_value = standardized_dataframe

    second_processor = Mock()
    second_processor.process.return_value = final_dataframe

    pipeline = SilverPipeline(
        processors=(
            first_processor,
            second_processor,
        ),
    )

    result = pipeline.run(source_dataframe)

    assert result is final_dataframe

    assert first_processor.process.call_args_list == [
        call(source_dataframe),
    ]
    assert second_processor.process.call_args_list == [
        call(standardized_dataframe),
    ]


def test_pipeline_returns_source_when_no_processors_are_configured() -> None:
    """The pipeline should preserve the source when no processors exist."""
    source_dataframe = Mock(name="source_dataframe")

    pipeline = SilverPipeline(processors=())

    result = pipeline.run(source_dataframe)

    assert result is source_dataframe
