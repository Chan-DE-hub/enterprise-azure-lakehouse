# Project Roadmap

## Purpose

This document defines the planned evolution of the Enterprise Azure Lakehouse repository.

The roadmap is intentionally incremental. Each milestone should introduce a focused set of capabilities together with tests, documentation, and implementation evidence.

---

## Roadmap Principles

The project roadmap follows these principles:

- Implement foundations before platform complexity
- Keep milestones small and reviewable
- Distinguish implemented capabilities from planned capabilities
- Add tests and documentation alongside code
- Avoid claiming production readiness before evidence exists
- Prefer maintainable patterns over unnecessary complexity

---

## Milestone Status

| Status | Meaning |
|---|---|
| ✅ Completed | Implemented, reviewed, and available in the repository |
| 🚧 In Progress | Currently being developed |
| ⏳ Planned | Approved for a future milestone |
| 🔍 Under Review | Scope or design is still being evaluated |

---

## v0.1.0 — Engineering Foundation

**Status:** 🚧 In Progress

### Objective

Establish the Python engineering, metadata, testing, and documentation foundation required by later Lakehouse features.

### Completed Capabilities

- Structured logging
- Typed configuration framework
- Enterprise exception hierarchy
- Metadata models
- Repository abstraction
- YAML metadata repository
- Metadata validation
- Business validation rules
- Cached repository using the Decorator Pattern
- Unit testing with pytest
- Linting and formatting with Ruff
- Static type checking with mypy
- Local quality gates with pre-commit
- Feature-branch and pull-request workflow

### Remaining Scope

- Architecture documentation foundation
- Coding standards
- Development workflow
- Branching strategy
- Architecture decision record structure
- README alignment
- Documentation review
- Release notes for v0.1.0

### Exit Criteria

The milestone is complete when:

- Foundation tests pass
- Ruff checks pass
- mypy checks pass
- pre-commit checks pass
- Documentation accurately reflects the repository
- The documentation pull request is reviewed and merged
- The repository can be tagged as `v0.1.0`

---

## v0.2.0 — Databricks Platform Foundation

**Status:** ⏳ Planned

### Objective

Introduce the initial Databricks project structure and deployment foundation without implementing complete business pipelines.

### Planned Capabilities

- Databricks project package
- Databricks Asset Bundles
- Environment-specific configuration
- Dev, test, and production deployment targets
- Unity Catalog naming conventions
- Catalog and schema bootstrap definitions
- External location and volume conventions
- Databricks Workflows foundation
- Basic deployment validation
- Platform documentation

### Exit Criteria

- Bundle validation succeeds
- Deployment configuration is environment-aware
- Unity Catalog conventions are documented
- No credentials are committed to the repository
- Automated tests remain passing

---

## v0.3.0 — Bronze Ingestion Foundation

**Status:** ⏳ Planned

### Objective

Implement a reusable, metadata-driven Bronze ingestion framework for file-based data.

### Planned Capabilities

- Landing-zone conventions
- Auto Loader foundation
- Schema inference and schema evolution strategy
- Append-only Bronze tables
- Ingestion metadata columns
- Checkpoint management
- Quarantine handling
- Replay support
- Audit events
- Sample retail source data
- Unit and integration-style tests

### Exit Criteria

- At least one sample domain is ingested end to end
- Bronze data remains traceable to the source
- Failed records are isolated
- Replay does not create unintended duplicates
- Documentation explains operational behavior

---

## v0.4.0 — Silver Processing Foundation

**Status:** ⏳ Planned

### Objective

Transform Bronze records into validated, deduplicated, and conformed Silver datasets.

### Planned Capabilities

- Schema enforcement
- Data cleansing
- Deduplication
- Standardization
- Business-key validation
- CDC processing
- Delete propagation
- Late-arriving data handling
- Data-quality expectations
- Silver quarantine rules
- Conformed customer, product, and order datasets

### Exit Criteria

- Silver transformations are incremental
- Duplicate handling is deterministic
- CDC behavior is tested
- Data-quality failures are observable
- Business rules are documented

---

## v0.5.0 — Gold Data Products

**Status:** ⏳ Planned

### Objective

Build analytics-ready data products for reporting and business consumption.

### Planned Capabilities

- Dimensional models
- Fact and dimension tables
- Surrogate keys
- Slowly Changing Dimension patterns
- Business aggregates
- Data marts
- Semantic reporting datasets
- Gold quality checks
- Consumption documentation

### Exit Criteria

- Gold outputs serve defined business questions
- Grain is documented for every model
- Measures and dimensions are traceable
- Incremental refresh behavior is validated

---

## v0.6.0 — Observability and Operations

**Status:** ⏳ Planned

### Objective

Add centralized monitoring, auditability, operational controls, and failure-management patterns.

### Planned Capabilities

- Pipeline-run history
- Dataset-level audit records
- Structured operational events
- SLA monitoring
- Failure classification
- Retry strategy
- Alerting design
- Backfill controls
- Replay runbooks
- Operational dashboards
- Troubleshooting documentation

### Exit Criteria

- Pipeline success and failure are traceable
- Operational metadata supports troubleshooting
- Replay and backfill procedures are documented
- Critical failure scenarios are tested

---

## v0.7.0 — CI/CD and Infrastructure Automation

**Status:** ⏳ Planned

### Objective

Automate validation, deployment, and infrastructure provisioning.

### Planned Capabilities

- GitHub Actions
- Automated pytest execution
- Automated Ruff checks
- Automated mypy checks
- Databricks bundle validation
- Environment deployment workflows
- Terraform foundation
- Pull-request quality gates
- Release workflow
- Versioning strategy

### Exit Criteria

- Pull requests run automated checks
- Deployment is repeatable
- Environment differences are configuration-driven
- Infrastructure changes are reviewed as code

---

## v0.8.0 — Streaming and Event Processing

**Status:** ⏳ Planned

### Objective

Introduce production-inspired event-streaming patterns.

### Planned Capabilities

- Azure Event Hubs integration
- Kafka-compatible ingestion
- Streaming Bronze tables
- Event parsing
- Watermarks
- Late-event handling
- Stateful deduplication
- Streaming Silver transformations
- Operational monitoring
- Failure and replay strategy

### Exit Criteria

- Streaming data is processed incrementally
- Checkpoints are managed safely
- Late and duplicate events are handled deterministically
- Recovery behavior is documented and tested

---

## Future Candidates

The following capabilities may be introduced after the core roadmap is stable:

- REST API ingestion
- Database CDC integration
- Azure Data Factory metadata-driven ingestion
- dbt transformation examples
- Snowflake interoperability
- Apache Airflow orchestration examples
- Microsoft Purview integration
- Cost monitoring
- Disaster-recovery design
- Performance benchmarking
- Synthetic scale testing
- Data-contract validation
- Generative AI insights

These items are exploratory and should not be treated as committed scope until moved into a defined milestone.

---

## Scope Management

A roadmap item should be moved into active development only when:

- Its purpose is clearly defined
- Dependencies are available
- Acceptance criteria are documented
- The implementation can be delivered in a focused pull request or small pull-request series
- The repository is ready to support the added complexity

Unrelated features should not be added to an active milestone solely because they appear useful.

---

## Roadmap Maintenance

This document should be updated when:

- A milestone is completed
- Scope changes materially
- A capability moves from planned to active development
- A design decision changes the delivery sequence
- A new dependency affects the roadmap

The roadmap should reflect actual repository progress rather than aspirational claims.
