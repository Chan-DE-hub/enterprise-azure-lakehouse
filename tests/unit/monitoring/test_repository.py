"""Tests for the operational monitoring repository."""

from unittest.mock import Mock, call, patch

from enterprise_lakehouse.monitoring import MonitoringRepository

PIPELINE_ID = "9b1fffe2-cdfb-4ce5-934f-de9474f51131"


def test_repository_executes_pipeline_update_query() -> None:
    """Pipeline update retrieval should execute the rendered summary query."""
    spark = Mock(name="spark")
    expected_dataframe = Mock(name="pipeline_updates_dataframe")
    spark.sql.return_value = expected_dataframe

    repository = MonitoringRepository(spark=spark)

    with patch(
        "enterprise_lakehouse.monitoring.repository.render_pipeline_event_log_query",
        return_value="SELECT pipeline_updates",
    ) as render_query:
        result = repository.pipeline_updates(
            pipeline_id=PIPELINE_ID,
        )

    assert result is expected_dataframe

    render_query.assert_called_once_with(
        resource_name="pipeline_update_summary.sql",
        pipeline_id=PIPELINE_ID,
    )
    spark.sql.assert_called_once_with(
        "SELECT pipeline_updates",
    )


def test_repository_executes_flow_metrics_query() -> None:
    """Flow metric retrieval should execute the packaged flow query."""
    spark = Mock(name="spark")
    expected_dataframe = Mock(name="flow_metrics_dataframe")
    spark.sql.return_value = expected_dataframe

    repository = MonitoringRepository(spark=spark)

    with patch(
        "enterprise_lakehouse.monitoring.repository.render_pipeline_event_log_query",
        return_value="SELECT flow_metrics",
    ) as render_query:
        result = repository.flow_metrics(
            pipeline_id=PIPELINE_ID,
        )

    assert result is expected_dataframe

    render_query.assert_called_once_with(
        resource_name="flow_metrics.sql",
        pipeline_id=PIPELINE_ID,
    )
    spark.sql.assert_called_once_with(
        "SELECT flow_metrics",
    )


def test_repository_executes_expectation_metrics_query() -> None:
    """Expectation retrieval should execute the packaged quality query."""
    spark = Mock(name="spark")
    expected_dataframe = Mock(name="expectation_metrics_dataframe")
    spark.sql.return_value = expected_dataframe

    repository = MonitoringRepository(spark=spark)

    with patch(
        "enterprise_lakehouse.monitoring.repository.render_pipeline_event_log_query",
        return_value="SELECT expectation_metrics",
    ) as render_query:
        result = repository.expectation_metrics(
            pipeline_id=PIPELINE_ID,
        )

    assert result is expected_dataframe

    render_query.assert_called_once_with(
        resource_name="expectation_metrics.sql",
        pipeline_id=PIPELINE_ID,
    )
    spark.sql.assert_called_once_with(
        "SELECT expectation_metrics",
    )


def test_repository_methods_use_independent_queries() -> None:
    """Each monitoring operation should resolve its own SQL resource."""
    spark = Mock(name="spark")
    repository = MonitoringRepository(spark=spark)

    with patch(
        "enterprise_lakehouse.monitoring.repository.render_pipeline_event_log_query",
        side_effect=[
            "SELECT pipeline_updates",
            "SELECT flow_metrics",
            "SELECT expectation_metrics",
        ],
    ) as render_query:
        repository.pipeline_updates(pipeline_id=PIPELINE_ID)
        repository.flow_metrics(pipeline_id=PIPELINE_ID)
        repository.expectation_metrics(pipeline_id=PIPELINE_ID)

    assert render_query.call_args_list == [
        call(
            resource_name="pipeline_update_summary.sql",
            pipeline_id=PIPELINE_ID,
        ),
        call(
            resource_name="flow_metrics.sql",
            pipeline_id=PIPELINE_ID,
        ),
        call(
            resource_name="expectation_metrics.sql",
            pipeline_id=PIPELINE_ID,
        ),
    ]
