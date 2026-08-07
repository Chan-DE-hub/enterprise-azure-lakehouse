# Lakeflow Event Log Monitoring

## Purpose

The monitoring framework uses native Databricks Lakeflow event logs as the operational source of truth for pipeline health, flow metrics, and data-quality evidence.

Custom operational tables are not introduced when the same information is already available from native Lakeflow state.

## Architecture

Lakeflow Pipeline
    ↓
Native Event Log
    ↓
Packaged Monitoring SQL
    ↓
MonitoringRepository
    ↓
Runtime Validation / Future Views / Dashboards

## Monitoring Capabilities

### Pipeline Updates

Captures:

- pipeline ID
- pipeline name
- update ID
- start timestamp
- completion timestamp
- final status
- duration
- error details

### Flow Metrics

Captures available native flow metrics such as:

- output rows
- AUTO CDC upserts
- deletes
- expectation-dropped rows
- flow duration
- final flow status

Native metrics are nullable because different Lakeflow flow types emit different operational fields.

### Expectation Metrics

Captures per-expectation:

- dataset
- expectation name
- passed records
- failed records

Expectation failure counts must not be treated as unique invalid-row counts because one row may fail multiple expectations.

## Design Principles

- Prefer native platform telemetry over duplicate custom audit writes.
- Use structured event-log fields instead of human-readable messages.
- Keep monitoring queries reusable and packaged with the Python monitoring module.
- Keep SQL execution behind `MonitoringRepository`.
- Keep monitoring models immutable.
- Treat presentation concerns such as dashboards and alerts as a separate observability layer.

## Runtime Validation

The monitoring framework is validated through a Databricks Asset Bundle job that queries real Lakeflow event logs for the Silver Orders and Silver Customers pipelines.

The validation covers:

- successful and failed pipeline updates
- flow-level execution metrics
- AUTO CDC metrics
- expectation metrics

## Future Extensions

Later observability work may add:

- governed monitoring views
- dashboards
- SLA tracking
- alerts
- cost monitoring
- cross-pipeline reconciliation

These extensions should reuse the monitoring foundation instead of duplicating native Lakeflow operational state.
