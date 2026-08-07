WITH expectation_events AS (
    SELECT
        origin.pipeline_id AS pipeline_id,
        origin.pipeline_name AS pipeline_name,
        origin.update_id AS update_id,
        origin.flow_name AS flow_name,
        timestamp AS event_timestamp,
        expectation.dataset AS dataset,
        expectation.name AS expectation_name,
        TRY_CAST(
            expectation.passed_records
            AS BIGINT
        ) AS passed_records,
        TRY_CAST(
            expectation.failed_records
            AS BIGINT
        ) AS failed_records
    FROM __EVENT_LOG_SOURCE__
    LATERAL VIEW EXPLODE(
        FROM_JSON(
            details:flow_progress:data_quality:expectations,
            'ARRAY<STRUCT<
                name: STRING,
                dataset: STRING,
                passed_records: BIGINT,
                failed_records: BIGINT
            >>'
        )
    ) exploded_expectations AS expectation
    WHERE event_type = 'flow_progress'
      AND origin.update_id IS NOT NULL
      AND origin.flow_name IS NOT NULL
),

aggregated_expectations AS (
    SELECT
        pipeline_id,
        pipeline_name,
        update_id,
        flow_name,
        dataset,
        expectation_name,
        MIN(event_timestamp) AS first_recorded_at,
        MAX(event_timestamp) AS last_recorded_at,
        SUM(
            COALESCE(
                passed_records,
                0
            )
        ) AS passed_records,
        SUM(
            COALESCE(
                failed_records,
                0
            )
        ) AS failed_records
    FROM expectation_events
    GROUP BY
        pipeline_id,
        pipeline_name,
        update_id,
        flow_name,
        dataset,
        expectation_name
)

SELECT
    pipeline_id,
    pipeline_name,
    update_id,
    flow_name,
    dataset,
    expectation_name,
    first_recorded_at,
    last_recorded_at,
    passed_records,
    failed_records
FROM aggregated_expectations
ORDER BY
    last_recorded_at DESC,
    pipeline_name,
    flow_name,
    dataset,
    expectation_name
