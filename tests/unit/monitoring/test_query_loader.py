"""Tests for packaged monitoring SQL resources."""

import pytest

from enterprise_lakehouse.monitoring import (
    load_monitoring_query,
    render_monitoring_query,
    render_pipeline_event_log_query,
)


def test_loader_reads_pipeline_update_summary_query() -> None:
    """The loader should return the packaged update-summary query."""
    query = load_monitoring_query("pipeline_update_summary.sql")

    assert "__EVENT_LOG_SOURCE__" in query
    assert "update_progress" in query
    assert "pipeline_id" in query
    assert "pipeline_name" in query
    assert "update_id" in query
    assert "final_status" in query
    assert "duration_seconds" in query


def test_loader_rejects_unknown_query() -> None:
    """Unknown monitoring resources should fail clearly."""
    with pytest.raises(
        FileNotFoundError,
        match="unknown.sql",
    ):
        load_monitoring_query("unknown.sql")


def test_renderer_injects_pipeline_event_log_source() -> None:
    """The renderer should use the native Lakeflow event-log table function."""
    query = render_pipeline_event_log_query(
        resource_name="pipeline_update_summary.sql",
        pipeline_id="9b1fffe2-cdfb-4ce5-934f-de9474f51131",
    )

    assert "__EVENT_LOG_SOURCE__" not in query
    assert "FROM event_log('9b1fffe2-cdfb-4ce5-934f-de9474f51131')" in query


@pytest.mark.parametrize(
    "pipeline_id",
    [
        "",
        "pipeline'; DROP TABLE audit; --",
        "pipeline id with spaces",
    ],
)
def test_renderer_rejects_invalid_pipeline_id(
    pipeline_id: str,
) -> None:
    """Pipeline identifiers must not allow arbitrary SQL injection."""
    with pytest.raises(
        ValueError,
        match="Invalid pipeline_id",
    ):
        render_pipeline_event_log_query(
            resource_name="pipeline_update_summary.sql",
            pipeline_id=pipeline_id,
        )


def test_renderer_requires_event_log_source_token(
    monkeypatch,
) -> None:
    """The renderer should reject templates without the source token."""
    monkeypatch.setattr(
        "enterprise_lakehouse.monitoring.query_loader.load_monitoring_query",
        lambda resource_name: "SELECT 1",
    )

    with pytest.raises(
        ValueError,
        match="Template token not found: __EVENT_LOG_SOURCE__",
    ):
        render_pipeline_event_log_query(
            resource_name="pipeline_update_summary.sql",
            pipeline_id="9b1fffe2-cdfb-4ce5-934f-de9474f51131",
        )


def test_generic_renderer_replaces_configured_tokens(
    monkeypatch,
) -> None:
    """The generic renderer should replace all configured template tokens."""
    monkeypatch.setattr(
        "enterprise_lakehouse.monitoring.query_loader.load_monitoring_query",
        lambda resource_name: (
            "SELECT * FROM __EVENT_LOG_SOURCE__ WHERE pipeline_name = __PIPELINE_NAME__"
        ),
    )

    query = render_monitoring_query(
        resource_name="pipeline_update_summary.sql",
        replacements={
            "__EVENT_LOG_SOURCE__": "event_log('pipeline-id')",
            "__PIPELINE_NAME__": "'silver_orders'",
        },
    )

    assert query == ("SELECT * FROM event_log('pipeline-id') WHERE pipeline_name = 'silver_orders'")


def test_generic_renderer_rejects_missing_template_token(
    monkeypatch,
) -> None:
    """Configured replacements must exist in the SQL template."""
    monkeypatch.setattr(
        "enterprise_lakehouse.monitoring.query_loader.load_monitoring_query",
        lambda resource_name: "SELECT 1",
    )

    with pytest.raises(
        ValueError,
        match="Template token not found",
    ):
        render_monitoring_query(
            resource_name="pipeline_update_summary.sql",
            replacements={
                "__EVENT_LOG_SOURCE__": "event_log('pipeline-id')",
            },
        )


def test_generic_renderer_rejects_unresolved_tokens(
    monkeypatch,
) -> None:
    """Rendered monitoring SQL must not contain unresolved template tokens."""
    monkeypatch.setattr(
        "enterprise_lakehouse.monitoring.query_loader.load_monitoring_query",
        lambda resource_name: "SELECT * FROM __EVENT_LOG_SOURCE__ WHERE flow_name = __FLOW_NAME__",
    )

    with pytest.raises(
        ValueError,
        match="Unresolved monitoring template tokens",
    ):
        render_monitoring_query(
            resource_name="flow_metrics.sql",
            replacements={
                "__EVENT_LOG_SOURCE__": "event_log('pipeline-id')",
            },
        )


def test_loader_reads_flow_metrics_query() -> None:
    """The loader should return the packaged flow-metrics query."""
    query = load_monitoring_query("flow_metrics.sql")

    assert "__EVENT_LOG_SOURCE__" in query
    assert "flow_progress" in query
    assert "num_output_rows" in query
    assert "num_upserted_rows" in query
    assert "num_deleted_rows" in query
    assert "dropped_records" in query
    assert "duration_seconds" in query


def test_loader_reads_expectation_metrics_query() -> None:
    """The loader should return the packaged expectation-metrics query."""
    query = load_monitoring_query("expectation_metrics.sql")

    assert "__EVENT_LOG_SOURCE__" in query
    assert "flow_progress" in query
    assert "expectations" in query
    assert "passed_records" in query
    assert "failed_records" in query
    assert "expectation_name" in query


def test_pipeline_update_query_serializes_structured_errors() -> None:
    """Pipeline update monitoring should normalize structured errors to text."""
    query = load_monitoring_query(
        "pipeline_update_summary.sql",
    )

    assert "TO_JSON(error) AS error_message" in query
