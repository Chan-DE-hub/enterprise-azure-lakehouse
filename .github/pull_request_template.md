## Summary

Provide a concise explanation of what this pull request changes and why the change is required.

## Change Type

Select all that apply.

- [ ] Architecture or design
- [ ] Documentation
- [ ] Feature
- [ ] Bug fix
- [ ] Refactoring
- [ ] Data contract or schema change
- [ ] Data quality rule
- [ ] Infrastructure
- [ ] Databricks resource configuration
- [ ] CI/CD
- [ ] Security
- [ ] Testing
- [ ] Operational or maintenance change
- [ ] Breaking change

## Scope

Identify the components affected by this change.

- [ ] Configuration
- [ ] Data contracts
- [ ] Ingestion
- [ ] Bronze
- [ ] Quarantine
- [ ] Silver
- [ ] Gold
- [ ] Data quality
- [ ] Reconciliation
- [ ] Monitoring
- [ ] Unity Catalog
- [ ] Databricks Workflows or pipelines
- [ ] Terraform
- [ ] GitHub Actions
- [ ] Documentation

## Implementation

Describe the implementation clearly.

Include, where applicable:

- processing logic
- source and target objects
- configuration changes
- schema changes
- incremental-processing behavior
- idempotency behavior
- retry and recovery behavior
- security implications
- deployment implications

## Architecture and Design Decisions

Explain any important technical decisions made in this pull request.

State whether the change:

- follows an existing Architecture Decision Record
- requires a new Architecture Decision Record
- changes an existing architectural boundary
- introduces a new dependency or platform capability

Related ADR or architecture document:

<!-- Add a relative repository link when applicable. -->

## Data Impact

Complete this section for changes affecting data processing.

### Data Grain

Describe the grain of the affected dataset or data product.

### Keys

List the applicable:

- business keys
- primary keys
- deduplication keys
- CDC sequence columns
- partitioning or clustering columns

### Incremental Behavior

Describe how new, changed, deleted, late, duplicate, or replayed records are handled.

### Schema Compatibility

- [ ] No schema change
- [ ] Backward-compatible schema change
- [ ] Breaking schema change
- [ ] Schema migration is included
- [ ] Data contract is updated
- [ ] Downstream consumers are documented

### Data Quality

Describe:

- validation rules
- rule severity
- quarantine behavior
- accepted and rejected record handling
- expected quality metrics

## Security and Privacy

Confirm that this pull request:

- [ ] Contains no credentials, tokens, keys, or connection strings
- [ ] Contains no production or customer data
- [ ] Contains no sensitive personal information
- [ ] Uses identity or secret references instead of embedded secret values
- [ ] Preserves least-privilege access
- [ ] Does not expose private infrastructure identifiers
- [ ] Uses synthetic or approved non-sensitive test data

Describe any security impact:

<!-- Write "None" when there is no security impact. -->

## Cost Impact

- [ ] No expected cloud cost impact
- [ ] Expected cost impact is documented
- [ ] Temporary resources include cleanup instructions
- [ ] Triggered or bounded execution is used where appropriate
- [ ] No continuously running resource is introduced without justification

Cost notes:

<!-- Write "None" when there is no expected cost impact. -->

## Testing and Validation

List the validation performed.

- [ ] Markdown preview reviewed
- [ ] Unit tests passed
- [ ] Integration tests passed
- [ ] Contract tests passed
- [ ] Data-quality scenarios validated
- [ ] Reconciliation validated
- [ ] Ruff checks passed
- [ ] Formatting checks passed
- [ ] mypy checks passed
- [ ] Databricks bundle validation passed
- [ ] Terraform formatting passed
- [ ] Terraform validation passed
- [ ] SQL validation passed
- [ ] Security or secret scan passed
- [ ] Manual smoke test completed

Provide commands, results, or evidence:

<!-- Include concise and reproducible evidence. -->

## Failure and Recovery

Describe applicable failure scenarios and recovery behavior.

Include, where relevant:

- retryable failures
- non-retryable failures
- checkpoint behavior
- watermark behavior
- replay procedure
- backfill procedure
- quarantine reprocessing
- rollback procedure

Write `Not applicable` when the change does not affect runtime behavior.

## Observability

Describe how the change can be monitored.

Include, where applicable:

- pipeline status
- audit fields
- data freshness
- record counts
- rejected records
- reconciliation results
- schema drift
- latency
- alerting
- relevant log fields

Write `Not applicable` when the change does not affect runtime behavior.

## Deployment and Rollback

### Deployment

Describe the required deployment steps, sequencing, configuration, and dependencies.

### Rollback

Describe how the change can be reversed safely.

For breaking data changes, include the data restoration or forward-fix strategy.

## Documentation

- [ ] README updated when required
- [ ] Architecture documentation updated when required
- [ ] ADR added or updated when required
- [ ] Data contract updated when required
- [ ] Deployment documentation updated when required
- [ ] Operational runbook updated when required
- [ ] Testing documentation updated when required
- [ ] Changelog updated when required
- [ ] No documentation change is required

## Reviewer Checklist

- [ ] The change has one clear responsibility
- [ ] The implementation matches the documented architecture
- [ ] Business logic remains explicit and reviewable
- [ ] Configuration controls only appropriate technical behavior
- [ ] Incremental logic is deterministic
- [ ] Reprocessing is idempotent
- [ ] Invalid records are not silently discarded
- [ ] Security-sensitive values are excluded
- [ ] Tests cover the important success and failure paths
- [ ] Operational behavior is documented
- [ ] Cost implications are acceptable
- [ ] Portfolio claims remain accurate and evidence-based

## Related Work

Link related issues, pull requests, commits, documents, or external references.

<!-- Example: Closes #123 -->
