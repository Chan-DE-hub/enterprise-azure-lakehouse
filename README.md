# Enterprise Azure Lakehouse

> Production-inspired Azure Databricks Lakehouse portfolio demonstrating
> metadata-driven data engineering, Medallion Architecture, software
> engineering practices, automated quality gates, and environment-aware
> deployment using Databricks Asset Bundles.

## Portfolio Status

**Core Lakehouse Implementation Complete — Production Readiness Finalization**

This repository demonstrates how a maintainable Azure Databricks data
platform can be designed incrementally using production-inspired engineering
patterns.

The project includes working implementations across Bronze, Silver, Gold,
monitoring, testing, and Databricks deployment configuration.

The repository intentionally distinguishes between:

- implemented and tested capabilities;
- production-inspired patterns demonstrated in a portfolio environment; and
- future capabilities that would require additional Azure infrastructure,
  enterprise integrations, or production workloads.

It does not claim to represent a live enterprise production environment.

---

## Project Overview

The Enterprise Azure Lakehouse models a fictional retail organization that
processes operational data such as customers and orders through a governed
Medallion Architecture.

The project demonstrates an engineering progression from raw ingestion to
analytics-ready data products:

```text
Source Systems
      |
      v
Landing / Source Files
      |
      v
Metadata-Driven Bronze Ingestion
      |
      v
Bronze Delta Tables
      |
      v
Silver Processing
  |-- Standardization
  |-- Expectations
  |-- Quarantine
  |-- Deduplication
  |-- Processing Strategies
      |
      v
Trusted Silver Tables
      |
      v
Gold Data Products
  |-- Dimensions
  |-- Facts
  |-- Aggregates
      |
      v
Analytics / Reporting
```

Supporting the data path are:

```text
Configuration
Metadata
Unity Catalog
Databricks Asset Bundles
Structured Logging
Monitoring
Data Quality
Automated Tests
CI Quality Gates
Architecture Documentation
```

---

## Business Scenario

The repository models a retail data platform receiving operational data from
multiple source domains.

Representative datasets include:

- customers;
- orders; and
- CDC-style customer events.

The objective is to transform source data into governed and analytics-ready
datasets while demonstrating:

- metadata-driven ingestion;
- incremental processing;
- data-quality enforcement;
- deterministic deduplication;
- quarantine handling;
- environment isolation;
- monitoring and operational visibility; and
- maintainable software engineering practices.

Synthetic data and portfolio-scale workloads are used so that the architecture
can be demonstrated without depending on proprietary enterprise datasets.

---

## Architecture

### High-Level Data Flow

```text
Operational Sources
        |
        v
Landing Zone
        |
        v
+---------------------------+
| Bronze Ingestion          |
|                           |
| Metadata Repository       |
| Loader Composition        |
| Auto Loader / File Reader |
| Ingestion Engine          |
| Delta Writers             |
+---------------------------+
        |
        v
Bronze
        |
        v
+---------------------------+
| Silver Processing         |
|                           |
| Standardization           |
| Expectations              |
| Quarantine                |
| Deduplication             |
| Processing Strategies     |
+---------------------------+
        |
        v
Silver
        |
        v
+---------------------------+
| Gold Data Products        |
|                           |
| Customer Dimension        |
| Order Fact                |
| Customer Order Summary    |
+---------------------------+
        |
        v
Analytics-Ready Data
```

### Cross-Cutting Capabilities

```text
                  +----------------------+
                  | Configuration        |
                  | Metadata             |
                  | Structured Logging   |
                  | Monitoring           |
                  | Data Quality         |
                  | Testing              |
                  | CI/CD                |
                  +----------------------+
                            |
       +--------------------+--------------------+
       |                    |                    |
       v                    v                    v
     Bronze               Silver               Gold
```

Detailed architecture documentation is available under
`docs/architecture/`.

---

## Implemented Capabilities

### Engineering Foundation

Implemented:

- typed Python package structure;
- structured logging;
- centralized exception hierarchy;
- typed application configuration;
- environment-specific configuration;
- metadata models and validation;
- repository abstractions;
- YAML-backed metadata repository;
- metadata caching;
- reusable business-rule patterns;
- pytest unit and integration testing;
- Ruff linting and formatting;
- MyPy static type checking; and
- pre-commit quality gates.

### Bronze Layer

Implemented:

- metadata-driven ingestion framework;
- reusable ingestion engine;
- loader composition;
- file-based ingestion;
- Spark file loading;
- Databricks Auto Loader abstraction;
- batch Delta writer;
- streaming Delta writer;
- Bronze write configuration;
- pipeline execution context;
- environment-aware target resolution;
- environment-specific checkpoint paths; and
- Databricks job entry point.

Bronze is designed to preserve source traceability while keeping ingestion
concerns separate from downstream business transformations.

### Silver Layer

Implemented:

- declarative Silver definitions;
- reusable Silver pipeline composition;
- metadata-driven standardization rules;
- standardization processor;
- expectation rule framework;
- quarantine rule generation;
- quarantine table naming;
- deterministic deduplication rules;
- deduplication processor; and
- metadata-driven processing strategy selection.

The Silver layer is responsible for producing typed, standardized, validated,
and trusted datasets from Bronze data.

### Gold Layer

Implemented:

- reusable Gold definitions;
- Gold definition factory;
- customer dimension;
- order fact;
- customer-order aggregate; and
- Gold pipeline definitions.

Gold models demonstrate analytics-oriented dimensional and aggregate data
products rather than acting as another generic transformation layer.

### Monitoring and Data Quality

Implemented:

- monitoring models;
- monitoring repository;
- reusable SQL query loader;
- pipeline update summaries;
- flow metrics;
- expectation metrics;
- data-quality health evaluation;
- health service abstraction; and
- runtime monitoring validation.

Monitoring is designed as a separate operational capability rather than being
embedded directly into transformation logic.

### Databricks Deployment

Implemented:

- Databricks Asset Bundle configuration;
- Databricks job resources;
- declarative pipeline resources;
- schema resources;
- development target;
- production target;
- environment-aware resource configuration;
- environment-specific application configuration;
- Bronze ingestion job;
- monitoring validation job; and
- bundle deployment smoke-test job.

The deployment configuration separates development and production resource
resolution while keeping environment-specific values outside core processing
logic.

---

## Environment Strategy

The repository contains explicit development and production configuration.

```text
configs/
|-- dev.yaml
`-- prod.yaml
```

Databricks Asset Bundle targets provide deployment-level environment
resolution.

```text
Databricks Bundle
        |
        +-- dev
        |    `-- development resources
        |
        `-- prod
             `-- production resource overrides
```

Environment-sensitive values include:

- Unity Catalog and schema resolution;
- Bronze target schema;
- storage locations;
- checkpoint roots; and
- application configuration.

This reduces environment-specific hardcoding inside pipeline code.

---

## Metadata-Driven Design

Metadata is used where configuration varies between datasets and processing
strategies.

Representative flow:

```text
Source Metadata
      |
      v
Metadata Repository
      |
      v
Validation
      |
      v
Loader / Processing Strategy
      |
      v
Pipeline Execution
```

The design deliberately avoids turning every behavior into metadata.

Stable engineering behavior remains in typed Python components, while
dataset-specific configuration is represented through metadata.

This keeps the framework reusable without creating unnecessary abstraction.

---

## Repository Structure

```text
enterprise-azure-lakehouse/
|
|-- .github/
|   |-- workflows/
|   |   `-- ci.yml
|   |-- CODEOWNERS
|   |-- dependabot.yml
|   `-- pull_request_template.md
|
|-- configs/
|   |-- metadata/
|   |   `-- sources.yaml
|   |-- dev.yaml
|   `-- prod.yaml
|
|-- docs/
|   |-- architecture/
|   |   |-- decisions/
|   |   |-- monitoring/
|   |   `-- silver/
|   |-- engineering/
|   `-- roadmap/
|
|-- resources/
|   |-- jobs/
|   |-- pipelines/
|   `-- schemas/
|
|-- src/
|   `-- enterprise_lakehouse/
|       |-- bronze/
|       |-- common/
|       |-- gold/
|       |-- jobs/
|       |-- monitoring/
|       `-- silver/
|
|-- tests/
|   |-- integration/
|   `-- unit/
|
|-- databricks.yml
|-- pyproject.toml
|-- uv.lock
`-- README.md
```

---

## Technology Stack

| Category | Technology | Usage |
| --- | --- | --- |
| Language | Python | Core framework and pipeline implementation |
| Distributed Processing | PySpark | Spark-based data processing and testing |
| Lakehouse Platform | Azure Databricks | Target execution platform |
| Storage Architecture | Delta Lake | Bronze, Silver, and Gold table patterns |
| Governance | Unity Catalog | Catalog and schema organization |
| Ingestion | Databricks Auto Loader | Incremental file-ingestion pattern |
| Deployment | Databricks Asset Bundles | Jobs, pipelines, schemas, and environments |
| Configuration | Pydantic / YAML | Typed environment and metadata configuration |
| Testing | pytest | Unit and integration tests |
| Linting | Ruff | Static linting and import checks |
| Formatting | Ruff | Python formatting |
| Type Checking | MyPy | Static type validation |
| Dependency Management | uv | Locked Python dependency management |
| Local Quality Gates | pre-commit | Automated repository checks |
| CI | GitHub Actions | Automated repository and Python quality validation |
| Version Control | Git / GitHub | Branching, pull requests, and review workflow |

---

## Testing Strategy

The project uses multiple levels of validation.

### Unit Tests

Unit tests cover components across:

- Bronze;
- configuration;
- metadata;
- logging;
- Silver;
- Gold;
- monitoring; and
- Databricks job orchestration.

### Integration Tests

Integration tests validate Spark-dependent behavior separately from isolated
unit tests.

Representative coverage includes:

- Spark session behavior; and
- Spark file loading.

### Static Quality Gates

Local and CI quality gates include:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest -v
uv run pre-commit run --all-files
```

---

## Continuous Integration

GitHub Actions validates changes targeting the main branch.

The CI workflow performs:

```text
Repository Validation
        |
        v
Python 3.12
        |
        v
Locked Dependency Installation
        |
        v
Ruff Lint
        |
        v
Ruff Format Check
        |
        v
MyPy
        |
        v
pytest
        |
        v
pre-commit
```

Dependencies are resolved from the committed `uv.lock` to improve
reproducibility between developer and CI environments.

Databricks deployment validation remains separated from unauthenticated
repository CI because deployment commands require a securely configured
Databricks identity.

---

## Databricks Validation

The repository supports Databricks Asset Bundle validation for both deployment
targets:

```bash
databricks bundle validate --target dev
```

```bash
databricks bundle validate --target prod
```

A dedicated bundle smoke-test job is also included to verify that a deployed
Python task can execute successfully in the Databricks runtime.

The smoke test verifies runtime execution only; it is not presented as a full
end-to-end production health check.

---

## Engineering Principles

The project follows these engineering principles:

1. **Configuration over hardcoding**
   Environment and dataset differences belong in configuration or metadata.

2. **Metadata where variability exists**
   Metadata drives variable behavior without replacing ordinary software
   engineering.

3. **Strong typing**
   Typed models and interfaces make contracts explicit.

4. **Separation of concerns**
   Reading, processing, writing, metadata, monitoring, and deployment remain
   separate responsibilities.

5. **Small reusable components**
   Components are designed to be understandable and independently testable.

6. **Idempotent and deterministic processing**
   Pipeline behavior should remain predictable during retries and repeated
   execution.

7. **Observability as architecture**
   Monitoring and data quality are treated as platform capabilities rather
   than afterthoughts.

8. **Environment isolation**
   Development and production configuration are resolved explicitly.

9. **Automated quality gates**
   Tests, linting, formatting, typing, and repository validation protect the
   main branch.

10. **Incremental delivery**
    Capabilities are introduced through focused pull requests instead of a
    single large implementation.

---

## Development Workflow

The repository follows a feature-branch workflow:

```text
main
 |
 +-- feature/<capability>
          |
          +-- implementation
          +-- tests
          +-- documentation
          +-- local quality gates
          |
          v
      Pull Request
          |
          v
        CI
          |
          v
      Code Review
          |
          v
        main
```

Changes are expected to pass automated quality gates before merge.

---

## Architecture Decisions

Architecture decisions are documented as ADRs under:

```text
docs/architecture/decisions/
```

Current decisions cover topics including:

- Unity Catalog governance;
- Unity Catalog Volumes;
- metadata-driven design boundaries;
- separation of Landing, Bronze, and Quarantine;
- Databricks-native orchestration; and
- the project's free-first operating model.

The purpose of the ADRs is to document not only what was implemented, but why
specific engineering trade-offs were chosen.

---

## Production-Inspired vs Production

This repository intentionally uses the term **production-inspired**.

It demonstrates patterns expected in maintainable production data platforms,
including:

- modular architecture;
- environment isolation;
- automated testing;
- static analysis;
- metadata-driven processing;
- data-quality handling;
- monitoring;
- deployment configuration; and
- CI quality gates.

However, this portfolio does not claim:

- live enterprise production traffic;
- enterprise-scale workload benchmarks;
- production SLAs;
- organization-wide security administration;
- live Azure Event Hubs or Kafka infrastructure;
- complete disaster-recovery implementation;
- production alerting integrations; or
- fully automated authenticated production deployment.

Those capabilities require infrastructure, operational ownership, credentials,
scale, and organizational controls beyond the scope of a standalone portfolio.

---

## Current Limitations

- Uses synthetic or portfolio sample data.
- Workloads demonstrate engineering patterns rather than enterprise-scale
  throughput.
- Cloud deployment requires a configured Databricks workspace and
  authentication.
- CI validates repository and Python engineering quality but does not
  automatically deploy production infrastructure.
- External enterprise source-system integrations are represented
  architecturally unless explicitly implemented in the repository.

---

## Future Enhancements

Potential future extensions include:

- Azure Data Factory metadata-driven source ingestion;
- Azure Event Hubs or Kafka integration;
- database CDC integration;
- REST API ingestion;
- secure workload-identity-based deployment automation;
- infrastructure as code;
- operational alerting integrations;
- replay and backfill runbooks;
- performance benchmarking;
- synthetic scale testing;
- Microsoft Purview integration;
- disaster-recovery design; and
- additional domain-oriented data products.

Future enhancements are intentionally separated from implemented capabilities.

---

## Local Development

### Requirements

- Python 3.12 or newer;
- `uv`;
- Git; and
- Databricks CLI when validating or deploying bundle resources.

### Install Dependencies

```bash
uv sync --frozen --extra dev
```

### Run Tests

```bash
uv run pytest -v
```

### Run Static Analysis

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

### Run All Pre-Commit Checks

```bash
uv run pre-commit run --all-files
```

### Validate Databricks Bundle

Development:

```bash
databricks bundle validate --target dev
```

Production:

```bash
databricks bundle validate --target prod
```

---

## Documentation

Additional documentation is available under `docs/`.

Key areas include:

```text
docs/
|-- architecture/
|   |-- decisions/
|   |-- monitoring/
|   `-- silver/
|
|-- engineering/
|   |-- branching-strategy.md
|   |-- coding-standards.md
|   `-- development-workflow.md
|
`-- roadmap/
    `-- roadmap.md
```

---

## Portfolio Purpose

This project demonstrates the ability to reason about a data platform beyond
individual notebooks or SQL transformations.

The focus is on:

- designing maintainable data-engineering frameworks;
- separating infrastructure, orchestration, and processing concerns;
- building reusable Python components;
- applying metadata-driven architecture deliberately;
- implementing Medallion Architecture with clear layer responsibilities;
- treating testing and observability as first-class concerns;
- using disciplined Git and pull-request workflows; and
- documenting engineering decisions and trade-offs.

The implementation is intentionally incremental so that the repository history
shows how the architecture evolved rather than presenting a generated
monolithic solution.

---

## Contributing

This repository is primarily a personal portfolio and learning project.

Suggestions, engineering feedback, and constructive review are welcome.

---

## License

Released under the MIT License.

---

## Author

**Christian Evangelista**

Business Intelligence Analyst with Data Engineering responsibilities,
building production-inspired cloud data engineering solutions with Python,
SQL, Azure, and Databricks.
