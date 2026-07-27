# Repository Structure and Ownership

## 1. Purpose

This document defines the final repository structure, responsibility boundaries, and ownership model for the Enterprise Azure Lakehouse portfolio.

The repository is organized by engineering responsibility rather than by arbitrary file type. Each directory must have a clear purpose, and new directories must not be introduced without an identified responsibility and concrete content.

The structure supports:

- Azure Databricks development
- Lakeflow Spark Declarative Pipelines
- Databricks Declarative Automation Bundles
- Unity Catalog deployment
- Metadata-driven ingestion
- Bronze, Silver, and Gold processing
- Data quality and quarantine
- Testing
- Infrastructure as Code
- CI/CD
- Observability
- Operational documentation

---

## 2. Final Target Structure

```text
enterprise-azure-lakehouse/
├── .github/
│   ├── workflows/
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   └── pull_request_template.md
│
├── config/
│   ├── base/
│   ├── dev/
│   ├── test/
│   └── prod/
│
├── data/
│   ├── contracts/
│   ├── reference/
│   └── synthetic/
│
├── docs/
│   ├── architecture/
│   │   ├── decisions/
│   │   ├── architecture-overview.md
│   │   └── repository-structure.md
│   ├── deployment/
│   ├── development/
│   ├── operations/
│   ├── security/
│   └── testing/
│
├── infrastructure/
│   ├── modules/
│   ├── environments/
│   └── scripts/
│
├── resources/
│   ├── jobs/
│   ├── pipelines/
│   ├── schemas/
│   └── permissions/
│
├── scripts/
│   ├── bootstrap/
│   ├── deployment/
│   ├── maintenance/
│   └── validation/
│
├── src/
│   └── enterprise_lakehouse/
│       ├── common/
│       │   ├── configuration/
│       │   ├── contracts/
│       │   ├── errors/
│       │   ├── logging/
│       │   └── validation/
│       ├── ingestion/
│       │   ├── files/
│       │   ├── events/
│       │   ├── jdbc/
│       │   └── api/
│       ├── pipelines/
│       │   ├── bronze/
│       │   ├── silver/
│       │   └── gold/
│       ├── quality/
│       ├── reconciliation/
│       └── operations/
│
├── sql/
│   ├── governance/
│   ├── control/
│   ├── audit/
│   ├── monitoring/
│   └── validation/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── fixtures/
│
├── .editorconfig
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
├── databricks.yml
├── pyproject.toml
└── uv.lock
```

This is the final target structure. Directories will be created only when the first real file for that responsibility is introduced.

---

## 3. Root-Level Files

| File | Responsibility |
|---|---|
| `README.md` | Primary project overview, architecture summary, setup instructions, evidence, and navigation |
| `LICENSE` | Repository licensing |
| `CONTRIBUTING.md` | Contribution, branch, commit, review, and engineering standards |
| `SECURITY.md` | Security expectations and responsible disclosure |
| `CODE_OF_CONDUCT.md` | Professional collaboration expectations |
| `CHANGELOG.md` | Notable repository changes |
| `.gitignore` | Prevents generated, local, sensitive, and transient files from entering version control |
| `.editorconfig` | Common text-formatting behavior across editors |
| `.pre-commit-config.yaml` | Local validation hooks |
| `pyproject.toml` | Python package metadata, dependencies, test, lint, format, and type-checking configuration |
| `uv.lock` | Reproducible Python dependency resolution |
| `databricks.yml` | Root configuration for Databricks Declarative Automation Bundles |

The repository will contain only one root `databricks.yml`. Resource definitions may be separated into files under `resources/` and included by the root configuration.

---

## 4. `.github/`

The `.github/` directory owns GitHub-specific repository automation and collaboration controls.

### Responsibilities

- Continuous integration workflows
- Pull request standards
- Code ownership
- Dependency-update configuration
- Repository automation

### Planned Contents

```text
.github/
├── workflows/
│   ├── ci.yml
│   ├── bundle-validation.yml
│   ├── terraform-validation.yml
│   └── security-scan.yml
├── CODEOWNERS
├── dependabot.yml
└── pull_request_template.md
```

### Boundary

Business logic, Databricks pipeline code, and infrastructure definitions must not be implemented inside GitHub workflow files.

Workflow files coordinate validation and deployment commands; they do not replace application scripts or deployment definitions.

---

## 5. `config/`

The `config/` directory owns version-controlled, non-secret configuration.

### Responsibilities

- Environment-independent defaults
- Environment-specific overrides
- Technical ingestion configuration
- Pipeline settings
- Naming and deployment parameters
- References to governed secrets, never secret values

### Structure

```text
config/
├── base/
├── dev/
├── test/
└── prod/
```

### Configuration Resolution

```text
Base configuration
        ↓
Environment override
        ↓
Runtime parameters
        ↓
Secret or identity references
```

### Boundary

Configuration may control repeatable technical behavior, but it must not become a hidden programming language for complex business transformations.

The following must never be committed:

- passwords
- access tokens
- storage keys
- client secrets
- private connection strings
- customer identifiers
- production credentials

---

## 6. `data/`

The `data/` directory owns small, safe, version-controlled data artifacts.

### Structure

```text
data/
├── contracts/
├── reference/
└── synthetic/
```

### Responsibilities

#### `contracts/`

Stores source and target data contracts such as:

- JSON Schema
- Avro schema definitions
- declarative schema specifications
- expected field metadata
- compatibility rules

#### `reference/`

Stores small, non-sensitive reference datasets used by tests or demonstrations.

Examples:

- country codes
- order status mappings
- payment type mappings

#### `synthetic/`

Stores small synthetic datasets used for:

- local tests
- demonstrations
- controlled failure scenarios
- screenshots
- reconciliation tests

### Boundary

This directory must not contain:

- production extracts
- customer data
- personal information
- large generated datasets
- binary runtime outputs
- checkpoints
- Delta transaction logs

Large or runtime-generated data belongs outside Git.

---

## 7. `docs/`

The `docs/` directory owns version-controlled engineering documentation.

### Structure

```text
docs/
├── architecture/
├── deployment/
├── development/
├── operations/
├── security/
└── testing/
```

### Responsibilities

| Directory | Responsibility |
|---|---|
| `architecture/` | Platform architecture, repository structure, data flows, and ADRs |
| `deployment/` | Local, Databricks, Azure, Terraform, and bundle deployment procedures |
| `development/` | Developer setup, coding conventions, and workflow instructions |
| `operations/` | Monitoring, incident response, replay, backfill, and runbooks |
| `security/` | Identity, access, secret handling, and threat considerations |
| `testing/` | Test strategy, fixtures, coverage, and execution guidance |

### Boundary

Documentation must describe actual repository behavior accurately.

Planned or unexecuted capabilities must be labeled clearly and must not be presented as successfully deployed production infrastructure.

---

## 8. `infrastructure/`

The `infrastructure/` directory owns Azure and Databricks infrastructure definitions managed through Terraform.

### Structure

```text
infrastructure/
├── modules/
├── environments/
└── scripts/
```

### Responsibilities

#### `modules/`

Reusable infrastructure components with clear boundaries.

Potential modules include:

- resource group
- storage account
- ADLS Gen2 containers
- Databricks workspace
- access connector
- Key Vault
- monitoring
- budget controls

Modules will be created only when reuse or isolation provides real value.

#### `environments/`

Environment composition and variable definitions.

```text
environments/
├── dev/
├── test/
└── prod/
```

#### `scripts/`

Infrastructure-specific helper scripts for:

- validation
- bounded demonstration deployment
- cleanup
- post-destroy verification

### Boundary

Terraform defines infrastructure. It must not contain data-transformation logic, business SQL, or pipeline processing code.

Infrastructure modules must not embed secret values.

---

## 9. `resources/`

The `resources/` directory owns Databricks resource definitions referenced by `databricks.yml`.

### Structure

```text
resources/
├── jobs/
├── pipelines/
├── schemas/
└── permissions/
```

### Responsibilities

#### `jobs/`

Defines Databricks Workflows, including:

- task graphs
- parameters
- retries
- timeouts
- schedules
- notifications
- compute references

#### `pipelines/`

Defines Lakeflow pipeline resources, including:

- source file references
- catalog and schema targets
- serverless or compute settings
- development mode
- channel and edition settings
- pipeline configuration

#### `schemas/`

Defines deployment-controlled Unity Catalog schemas or related governed objects when bundle-managed definitions are appropriate.

#### `permissions/`

Defines environment-specific resource permissions and workload access.

### Boundary

Resource YAML defines deployed Databricks resources. It must not become the primary location for Python or SQL transformation logic.

---

## 10. `scripts/`

The `scripts/` directory owns executable operational entry points that are not part of the reusable Python package.

### Structure

```text
scripts/
├── bootstrap/
├── deployment/
├── maintenance/
└── validation/
```

### Responsibilities

| Directory | Responsibility |
|---|---|
| `bootstrap/` | Initial developer or environment setup |
| `deployment/` | Controlled deployment and cleanup entry points |
| `maintenance/` | Backfill, replay, repair, and operational maintenance |
| `validation/` | Repository-wide validation and smoke-test commands |

### Boundary

A script should coordinate reusable package functions or external commands.

Complex reusable logic must be implemented under `src/`, not duplicated across scripts.

---

## 11. `src/enterprise_lakehouse/`

The `src/enterprise_lakehouse/` directory owns reusable application and pipeline code.

Using a `src` layout prevents accidental imports from the repository root and encourages the package to be tested as it will be installed or deployed.

### Structure

```text
src/enterprise_lakehouse/
├── common/
├── ingestion/
├── pipelines/
├── quality/
├── reconciliation/
└── operations/
```

---

## 12. `common/`

The `common/` package contains narrowly scoped capabilities shared by multiple engineering components.

```text
common/
├── configuration/
├── contracts/
├── errors/
├── logging/
└── validation/
```

### Responsibilities

#### `configuration/`

- typed configuration models
- environment resolution
- configuration loading
- configuration validation

#### `contracts/`

- schema contract loading
- contract compatibility checks
- field-level contract representations

#### `errors/`

- domain-specific exception types
- retryable versus non-retryable failure classification

#### `logging/`

- structured logging configuration
- correlation and run context
- safe log-field handling

#### `validation/`

- shared technical validation
- identifier validation
- path validation
- configuration invariants

### Boundary

`common/` must not become a dumping ground.

The following generic files are prohibited unless they have a narrowly documented responsibility:

```text
utils.py
helpers.py
misc.py
common.py
```

---

## 13. `ingestion/`

The `ingestion/` package owns source-specific data acquisition behavior.

```text
ingestion/
├── files/
├── events/
├── jdbc/
└── api/
```

### Responsibilities

#### `files/`

- Auto Loader options
- file metadata extraction
- file-format handling
- schema-location behavior
- file-ingestion validation

#### `events/`

- Kafka and Event Hubs input configuration
- event metadata extraction
- offset and partition handling
- event-envelope parsing

#### `jdbc/`

- partitioned source reads
- incremental extraction configuration
- source protection
- watermark predicates
- connection option validation

#### `api/`

- pagination
- rate-limit handling
- retries
- request and response validation
- landing of API payloads

### Boundary

The repository will not build one universal ingestion function containing deeply nested conditions for every source type.

Each adapter owns source-specific operational behavior while reusing shared configuration, validation, and logging capabilities.

---

## 14. `pipelines/`

The `pipelines/` package owns declarative dataset definitions and medallion transformations.

```text
pipelines/
├── bronze/
├── silver/
└── gold/
```

### Bronze Responsibilities

- durable ingestion history
- technical metadata
- source fidelity
- raw payload retention where justified
- ingestion-level validation
- quarantine routing
- no consumer-specific business logic

### Silver Responsibilities

- parsing
- standardization
- deterministic deduplication
- CDC application
- delete handling
- conformance
- trusted business rules
- SCD processing where required

### Gold Responsibilities

- facts
- dimensions
- aggregates
- metrics
- consumer-ready data products
- documented grain and business definitions

### Boundary

Pipeline source files define datasets and transformation logic.

Reusable technical behavior should be delegated to focused modules instead of embedding large procedural frameworks inside dataset definitions.

---

## 15. `quality/`

The `quality/` package owns reusable data-quality behavior.

### Responsibilities

- expectation definitions
- rule loading
- rule severity
- validation results
- quarantine decision support
- data-quality metric generation

### Boundary

Business-specific rules remain close to their domain or pipeline when centralizing them would reduce clarity.

The package may provide the execution model without forcing every rule into one global repository.

---

## 16. `reconciliation/`

The `reconciliation/` package owns source-to-target and layer-to-layer reconciliation.

### Responsibilities

- record-count comparison
- amount or measure comparison
- accepted and rejected record accounting
- hash or checksum validation
- reconciliation status
- tolerance evaluation
- evidence generation

### Boundary

Reconciliation is separate from pipeline execution status.

A technically successful job can still fail business reconciliation.

---

## 17. `operations/`

The `operations/` package owns reusable operational behavior.

### Responsibilities

- replay request handling
- backfill request handling
- run-context creation
- checkpoint-reset safeguards
- repair validation
- operational status transitions

### Boundary

Destructive operations must require explicit scope, validation, and audit context.

Operations code must not silently delete checkpoints, tables, or retained source data.

---

## 18. `sql/`

The `sql/` directory owns deployment and operational SQL that is not best represented as Python pipeline code.

### Structure

```text
sql/
├── governance/
├── control/
├── audit/
├── monitoring/
└── validation/
```

### Responsibilities

| Directory | Responsibility |
|---|---|
| `governance/` | Catalogs, schemas, volumes, grants, views, row filters, and masks |
| `control/` | Control and configuration table definitions |
| `audit/` | Audit and reconciliation table definitions |
| `monitoring/` | Operational views and monitoring queries |
| `validation/` | Post-deployment and smoke-test SQL |

### Boundary

SQL files must be deterministic, reviewable, and environment-aware.

Physical environment identifiers must be supplied through deployment configuration rather than copied into every SQL file.

---

## 19. `tests/`

The `tests/` directory owns automated test code and test fixtures.

### Structure

```text
tests/
├── unit/
├── integration/
├── contract/
└── fixtures/
```

### Responsibilities

#### `unit/`

Tests pure or isolated behavior such as:

- parsers
- configuration validation
- schema conversion
- deduplication rules
- hashing
- reconciliation calculations

#### `integration/`

Tests interactions among multiple components such as:

- file ingestion to Bronze
- Bronze to Silver transformation
- quarantine routing
- local Spark behavior
- deployment smoke tests

#### `contract/`

Tests:

- required fields
- type compatibility
- schema evolution
- breaking changes
- source and target contract compliance

#### `fixtures/`

Stores small test-only input and expected-output artifacts.

### Boundary

Tests must not depend on real customer data or uncontrolled production systems.

Cloud-dependent tests must be clearly marked and excluded from the default free local test suite.

---

## 20. Ownership Model

| Area | Primary owner | Review focus |
|---|---|---|
| Architecture | Data Architect / Principal Data Engineer | Boundaries, trade-offs, scalability, governance |
| Python application code | Data Engineering | Correctness, maintainability, testability |
| Pipeline definitions | Data Engineering | Incrementality, idempotency, quality, recovery |
| SQL models | Data Engineering / Analytics Engineering | Grain, determinism, performance, semantics |
| Infrastructure | Cloud / Platform Engineering | Security, networking, cost, reproducibility |
| Bundle resources | Data Engineering / Platform Engineering | Deployment behavior, permissions, environment isolation |
| CI/CD | Platform / DevOps Engineering | Security, validation, promotion, rollback |
| Security controls | Security / Platform Engineering | Identity, least privilege, secret handling |
| Data contracts | Source owner and Data Engineering | Compatibility, ownership, breaking changes |
| Operations | Data Engineering / Platform Operations | Monitoring, replay, failure recovery |

For this portfolio, one developer may implement all areas, but the repository will preserve these enterprise ownership boundaries.

---

## 21. Dependency Direction

Dependencies must flow toward stable, focused capabilities.

```text
Pipeline definitions
        ↓
Domain and processing modules
        ↓
Ingestion, quality, and reconciliation capabilities
        ↓
Common configuration, contracts, errors, logging, and validation
```

The reverse dependency is prohibited.

Examples:

- `common/` must not import Bronze, Silver, or Gold pipeline modules.
- ingestion adapters must not depend on Gold models.
- infrastructure code must not import application transformation logic.
- GitHub workflows must not contain reusable business logic.

Circular imports and circular ownership must be treated as design defects.

---

## 22. Naming Standards

### Python packages and modules

Use lowercase snake case:

```text
config_loader.py
schema_validator.py
watermark_manager.py
audit_logger.py
```

### Python classes

Use Pascal case:

```text
SourceConfiguration
SchemaContract
ReconciliationResult
```

### Python functions and variables

Use lowercase snake case:

```text
load_source_configuration
validate_schema_contract
pipeline_run_id
```

### YAML files

Use lowercase kebab case:

```text
bronze-file-pipeline.yml
silver-cdc-pipeline.yml
daily-sales-job.yml
```

### SQL files

Use ordered lowercase snake case when execution order matters:

```text
001_create_catalogs.sql
010_create_schemas.sql
020_create_volumes.sql
030_apply_grants.sql
```

### Databricks objects

Use lowercase snake case unless an external naming standard requires otherwise:

```text
dev_sales.bronze.orders
dev_sales.silver.orders
dev_sales.gold.fact_sales
```

---

## 23. Files and Patterns That Are Prohibited

The repository must not introduce:

- DBFS mount scripts
- committed credentials
- production data
- arbitrary `utils.py` dumping grounds
- a single universal ingestion engine
- notebooks containing the entire platform implementation
- hardcoded environment-specific storage names throughout application code
- duplicated business logic across Bronze, Silver, and Gold
- checkpoint deletion without safeguards
- generated Spark or Terraform runtime files
- copied vendor libraries
- empty folders maintained only by placeholder files
- claims of production execution without evidence

---

## 24. Directory-Creation Rule

A directory is created only when:

1. Its responsibility is defined in this document.
2. At least one real implementation or documentation file is ready.
3. The file belongs to that responsibility.
4. The directory does not duplicate an existing ownership boundary.

Empty folders and placeholder `.gitkeep` files will not be used merely to display the target structure.

---

## 25. Validation Rules

Repository structure compliance will be validated through:

- code review
- naming checks
- import-boundary review
- Python linting and type checking
- test discovery
- bundle validation
- Terraform formatting and validation
- secret scanning
- documentation review
- GitHub Actions

Future automated checks may verify:

- prohibited filenames
- forbidden DBFS mount usage
- hardcoded secret patterns
- package import boundaries
- expected configuration structure
- required documentation for new architectural components

---

## 26. Implementation Sequence

The repository will be implemented in this order:

```text
1. Repository controls and developer configuration
2. Python project and dependency foundation
3. Configuration and contract models
4. Synthetic data and test fixtures
5. Unity Catalog and governance SQL
6. File-based Bronze ingestion
7. Data quality and quarantine
8. Silver standardization and CDC
9. Gold data products
10. Reconciliation and operational controls
11. Databricks bundle resources
12. CI/CD validation
13. Terraform infrastructure
14. Monitoring, replay, backfill, and runbooks
15. Final evidence and interview documentation
```

This sequence builds executable foundations before adding higher-level data products.

---

## 27. Definition of Done

The repository structure is considered successfully implemented when:

- every created directory has concrete content
- every file has one clear responsibility
- source code is importable as a package
- configuration is validated and secret-free
- pipeline definitions are separated by layer
- ingestion adapters reflect source-specific behavior
- automated tests mirror the package structure
- Databricks resources are defined through bundle configuration
- infrastructure is separated from application code
- CI/CD validates the repository
- operational procedures are documented
- the repository can be navigated and explained without guesswork
