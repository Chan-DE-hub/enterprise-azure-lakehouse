# ADR-0004: Separate Landing, Bronze, and Quarantine Responsibilities

- **Status:** Accepted
- **Date:** 2026-07-24
- **Decision owners:** Data Engineering
- **Related documents:** [Architecture Overview](../architecture-overview.md)

## Context

The terms Landing, Raw, and Bronze are often used inconsistently.

Combining source-delivered files, parsed Delta records, and rejected records into one location creates unclear retention rules, ownership boundaries, replay behavior, and data-quality semantics.

The architecture requires explicit responsibilities for source preservation, queryable ingestion history, and invalid-record handling.

## Decision

Landing, Bronze, and Quarantine will be treated as separate architectural responsibilities.

### Landing

Landing preserves source-delivered files or extracts with minimal modification.

Landing responsibilities include:

- preserving the received payload
- retaining source filenames and delivery structure
- supporting replay
- supporting source-to-target reconciliation
- isolating partially delivered files
- applying retention and archival policies

Landing is not a business transformation layer.

### Bronze

Bronze stores queryable, append-oriented source history in Delta format together with technical ingestion metadata.

Bronze responsibilities include:

- parsing source records sufficiently for durable storage
- retaining raw payload when useful
- recording ingestion timestamps
- recording source identifiers
- recording file, topic, partition, or offset metadata
- recording schema version
- supporting deduplication and replay
- preserving source fidelity

Bronze does not perform complex business transformations.

### Quarantine

Quarantine stores records that cannot safely continue through the trusted path.

Quarantine responsibilities include:

- retaining failed records or payloads
- recording failed rule identifiers
- recording error details
- recording source and run context
- supporting investigation
- supporting controlled correction and reprocessing

Invalid records must not be silently discarded.

## Decision Drivers

- Source fidelity
- Replayability
- Clear retention boundaries
- Explicit data-quality handling
- Operational troubleshooting
- Reconciliation
- Separation of concerns
- Auditability

## Alternatives Considered

### Combine Landing and Bronze

**Advantages**

- Fewer layers
- Simpler visual architecture

**Disadvantages**

- Blurs file preservation and parsed-table responsibilities
- Makes replay semantics unclear
- Complicates retention
- Weakens separation between physical delivery and logical ingestion

### Write Only Valid Records to Bronze

**Advantages**

- Cleaner Bronze tables
- Fewer invalid records in the primary path

**Disadvantages**

- Bronze no longer reflects source history accurately
- Failed records may be lost
- Reconciliation becomes unreliable
- Troubleshooting becomes difficult

### Drop Invalid Records

**Advantages**

- Simplest pipeline behavior
- Lower storage use

**Disadvantages**

- Silent data loss
- Poor auditability
- No correction or replay path
- Unacceptable for production-inspired engineering

## Consequences

### Positive Consequences

- Source delivery and parsed history have distinct ownership.
- Replay boundaries are clearer.
- Invalid records remain recoverable.
- Reconciliation can distinguish delivered, ingested, accepted, and rejected records.
- Data quality becomes operationally visible.
- Retention policies can differ by responsibility.

### Negative Consequences and Trade-offs

- Additional storage objects and schemas are required.
- More lifecycle policies must be managed.
- Quarantine reprocessing requires explicit controls.
- Duplicate storage may exist between original payloads and parsed Bronze records.

## Implementation Implications

The standard flow will be:

```text
Source
    ↓
Landing
    ↓
Bronze
    ├── Valid path
    └── Quarantine path
            ↓
    Controlled reprocessing

_ingestion_timestamp
_source_system
_source_object
_source_file
_source_file_modification_time
_source_event_timestamp
_source_partition
_source_offset
_schema_version
_pipeline_run_id
_record_hash
_raw_payload

Quarantine records will include applicable fields such as:

_quarantine_timestamp
_failed_rule_id
_error_code
_error_message
_reprocessing_status
_original_run_id
