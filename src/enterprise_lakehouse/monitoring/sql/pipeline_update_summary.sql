WITH update_status_events AS (
    SELECT
        origin.pipeline_id AS pipeline_id,
        origin.pipeline_name AS pipeline_name,
        origin.update_id AS update_id,
        FROM_JSON(
            details,
            'STRUCT<update_progress: STRUCT<state: STRING>>'
        ).update_progress.state AS update_status,
        timestamp AS event_timestamp,
        TO_JSON(error) AS error_message,
        ROW_NUMBER() OVER (
            PARTITION BY origin.pipeline_id, origin.update_id
            ORDER BY timestamp DESC
        ) AS status_rank
    FROM __EVENT_LOG_SOURCE__
    WHERE event_type = 'update_progress'
      AND origin.update_id IS NOT NULL
),

latest_update_status AS (
    SELECT
        pipeline_id,
        pipeline_name,
        update_id,
        update_status AS final_status,
        error_message
    FROM update_status_events
    WHERE status_rank = 1
),

update_timing AS (
    SELECT
        origin.pipeline_id AS pipeline_id,
        origin.pipeline_name AS pipeline_name,
        origin.update_id AS update_id,
        MIN(
            CASE
                WHEN event_type = 'create_update'
                THEN timestamp
            END
        ) AS started_at,
        MAX(
            CASE
                WHEN event_type = 'update_progress'
                 AND FROM_JSON(
                     details,
                     'STRUCT<update_progress: STRUCT<state: STRING>>'
                 ).update_progress.state IN (
                     'COMPLETED',
                     'FAILED',
                     'CANCELED',
                     'CANCELLED'
                 )
                THEN timestamp
            END
        ) AS completed_at
    FROM __EVENT_LOG_SOURCE__
    WHERE event_type IN (
        'create_update',
        'update_progress'
    )
      AND origin.update_id IS NOT NULL
    GROUP BY
        origin.pipeline_id,
        origin.pipeline_name,
        origin.update_id
)

SELECT
    status.pipeline_id,
    status.pipeline_name,
    status.update_id,
    timing.started_at,
    timing.completed_at,
    status.final_status,
    CASE
        WHEN timing.started_at IS NOT NULL
         AND timing.completed_at IS NOT NULL
        THEN ROUND(
            TIMESTAMPDIFF(
                MILLISECOND,
                timing.started_at,
                timing.completed_at
            ) / 1000.0,
            3
        )
        ELSE NULL
    END AS duration_seconds,
    status.error_message
FROM latest_update_status AS status
INNER JOIN update_timing AS timing
    ON status.pipeline_id = timing.pipeline_id
   AND status.update_id = timing.update_id
WHERE timing.started_at IS NOT NULL
ORDER BY timing.started_at DESC
