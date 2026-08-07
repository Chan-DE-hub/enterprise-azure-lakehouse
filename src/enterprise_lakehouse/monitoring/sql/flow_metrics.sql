WITH flow_progress_events AS (
    SELECT
        origin.pipeline_id AS pipeline_id,
        origin.pipeline_name AS pipeline_name,
        origin.update_id AS update_id,
        origin.flow_name AS flow_name,
        timestamp AS event_timestamp,
        details:flow_progress.status::STRING AS flow_status,
        TRY_CAST(
            details:flow_progress.metrics.num_output_rows
            AS BIGINT
        ) AS output_rows,
        TRY_CAST(
            details:flow_progress.metrics.num_upserted_rows
            AS BIGINT
        ) AS upserted_rows,
        TRY_CAST(
            details:flow_progress.metrics.num_deleted_rows
            AS BIGINT
        ) AS deleted_rows,
        TRY_CAST(
            details:flow_progress.data_quality.dropped_records
            AS BIGINT
        ) AS expectation_dropped_rows
    FROM __EVENT_LOG_SOURCE__
    WHERE event_type = 'flow_progress'
      AND origin.update_id IS NOT NULL
      AND origin.flow_name IS NOT NULL
      AND origin.flow_name
          != 'pipelines.flowTimeMetrics.missingFlowName'
),

aggregated_flows AS (
    SELECT
        pipeline_id,
        pipeline_name,
        update_id,
        flow_name,

        MIN(
            CASE
                WHEN flow_status IN (
                    'STARTING',
                    'RUNNING',
                    'COMPLETED'
                )
                THEN event_timestamp
            END
        ) AS started_at,

        MAX(
            CASE
                WHEN flow_status IN (
                    'STARTING',
                    'RUNNING',
                    'COMPLETED'
                )
                THEN event_timestamp
            END
        ) AS completed_at,

        MAX_BY(
            flow_status,
            event_timestamp
        ) FILTER (
            WHERE flow_status IN (
                'COMPLETED',
                'FAILED',
                'CANCELED',
                'CANCELLED',
                'EXCLUDED',
                'SKIPPED',
                'STOPPED',
                'IDLE'
            )
        ) AS final_status,

        SUM(output_rows) AS output_rows,
        SUM(upserted_rows) AS upserted_rows,
        SUM(deleted_rows) AS deleted_rows,
        MAX(expectation_dropped_rows) AS expectation_dropped_rows

    FROM flow_progress_events
    GROUP BY
        pipeline_id,
        pipeline_name,
        update_id,
        flow_name
)

SELECT
    pipeline_id,
    pipeline_name,
    update_id,
    flow_name,
    started_at,
    completed_at,
    final_status,

    CASE
        WHEN started_at IS NOT NULL
         AND completed_at IS NOT NULL
        THEN ROUND(
            TIMESTAMPDIFF(
                MILLISECOND,
                started_at,
                completed_at
            ) / 1000.0,
            3
        )
        ELSE NULL
    END AS duration_seconds,

    output_rows,
    upserted_rows,
    deleted_rows,
    expectation_dropped_rows

FROM aggregated_flows
ORDER BY
    started_at DESC,
    pipeline_name,
    flow_name
