# Package Architecture

## 1. Purpose

This document defines the internal application architecture for the Enterprise Azure Lakehouse project.

Rather than organizing code by technology or file type, the application is organized by engineering responsibility. Each package has one clearly defined purpose, explicit ownership boundaries, and controlled dependencies.

The architecture is designed to support:

- Azure Databricks
- Lakeflow Declarative Pipelines
- Unity Catalog
- Incremental batch ingestion
- Streaming ingestion
- Metadata-driven processing
- CDC
- Data quality
- Reconciliation
- Operational support

---

# 2. High-Level Package Structure

```text
src/
└── enterprise_lakehouse/
    ├── common/
    ├── ingestion/
    ├── pipelines/
    │   ├── bronze/
    │   ├── silver/
    │   └── gold/
    ├── quality/
    ├── reconciliation/
    └── operations/
```

Each package owns a single engineering responsibility.

Packages communicate through documented interfaces rather than direct implementation coupling.

---

# 3. Dependency Direction

Dependencies always flow downward.

```text
Gold
    ↓
Silver
    ↓
Bronze
    ↓
Ingestion
    ↓
Common
```

The opposite direction is prohibited.

For example:

- Bronze must never import Gold.
- Common must never import pipeline modules.
- Ingestion adapters must not depend on Silver transformations.
- Reconciliation must never contain Bronze ingestion logic.

This keeps the architecture maintainable as the platform grows.

---

# 4. Package Responsibilities

## common/

Provides reusable technical capabilities shared across the platform.

Examples:

- configuration loading
- structured logging
- schema validation
- custom exceptions
- contracts
- helper abstractions with well-defined scope

This package must never contain business rules.

---

## ingestion/

Responsible only for acquiring data from external systems.

Examples:

- Auto Loader
- Event Hubs
- Kafka
- JDBC
- REST APIs

Responsibilities include:

- authentication
- retries
- pagination
- watermark predicates
- schema hints
- file metadata
- event envelope parsing

The ingestion package does not perform business transformations.

---

## pipelines/

Owns Medallion processing.

### Bronze

Responsible for:

- source fidelity
- append-only ingestion
- technical metadata
- schema evolution
- quarantine routing

No business transformations.

---

### Silver

Responsible for:

- parsing
- standardization
- CDC application
- deduplication
- conformance
- trusted business rules

---

### Gold

Responsible for:

- facts
- dimensions
- KPIs
- aggregates
- semantic models
- consumer-ready datasets

---

## quality/

Responsible for reusable data quality execution.

Examples:

- expectation evaluation
- rule execution
- validation metrics
- rejected record handling

---

## reconciliation/

Responsible for business reconciliation.

Examples:

- row counts
- control totals
- checksums
- financial balancing
- tolerance evaluation

A pipeline may succeed technically while failing reconciliation.

---

## operations/

Supports controlled operational activities.

Examples:

- replay
- backfill
- checkpoint reset
- repair
- operational diagnostics

Operational utilities must be explicit and auditable.

---

# 5. Communication Rules

Packages communicate only through documented interfaces.

For example:

```text
Bronze
      ↓
configuration
      ↓
logging
      ↓
schema validation
```

Instead of directly importing unrelated implementation.

---

# 6. Design Principles

Every package should satisfy:

- Single responsibility
- Explicit ownership
- Testability
- Low coupling
- High cohesion
- Deterministic behavior
- Idempotent processing
- Observable execution

---

# 7. Forbidden Patterns

The following are prohibited:

- giant utils.py
- giant helpers.py
- circular imports
- business logic inside ingestion adapters
- business logic inside configuration
- duplicated transformations
- hidden global state
- hardcoded storage accounts
- hardcoded catalogs
- hardcoded credentials

---

# 8. Engineering Philosophy

The application is designed so that every package answers one question:

"What engineering capability does this package own?"

If that answer is unclear, the package boundary is likely incorrect.

Every new module added to the repository should strengthen this responsibility model rather than weaken it.

Well-defined ownership boundaries reduce maintenance cost, simplify testing, and make the platform easier to extend as new data sources, pipelines, and consumers are introduced.
