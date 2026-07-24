# ADR-0006: Adopt a Free-First and Cost-Conscious Portfolio Operating Model

- **Status:** Accepted
- **Date:** 2026-07-24
- **Decision owners:** Data Engineering
- **Related documents:** [Architecture Overview](../architecture-overview.md)

## Context

The repository is a personal portfolio project designed to demonstrate enterprise-oriented engineering practices.

A complete Azure implementation could require paid services such as Azure Databricks, Azure Data Lake Storage, Azure Data Factory, Event Hubs, Key Vault, Azure Monitor, networking components, and hosted databases.

Leaving cloud services running solely for portfolio appearance creates unnecessary financial risk.

The project must distinguish architectural completeness from continuous paid infrastructure usage.

## Decision

The portfolio will follow a free-first operating model.

Free and open-source tools will be used for:

- source control
- documentation
- architecture diagrams
- local development
- dependency management
- linting
- formatting
- type checking
- unit testing
- local Spark testing
- Infrastructure as Code authoring
- deployment-definition validation
- CI/CD validation where free allowances permit

Paid cloud resources will be created only for bounded demonstrations that require live-cloud evidence.

Before any paid deployment, the project must define:

- expected resources
- expected duration
- estimated cost exposure
- budget or spending controls
- resource tags
- cleanup commands
- verification that cleanup succeeded

Unsupported enterprise capabilities may be represented through code, Terraform, deployment definitions, tests, diagrams, and operational documentation.

The repository must never claim that unexecuted infrastructure was deployed successfully.

## Decision Drivers

- Financial safety
- Honest representation
- Reproducibility
- Local testability
- Avoidance of idle infrastructure
- Portfolio accessibility
- Demonstration of cost engineering
- Separation between architectural design and runtime proof

## Alternatives Considered

### Maintain a Permanent Azure Environment

**Advantages**

- Continuous live demonstration
- Real cloud screenshots and runtime evidence

**Disadvantages**

- Ongoing cost
- Security and maintenance burden
- Resource drift
- Risk of forgotten services
- Unnecessary for most code and architecture validation

### Use Only Documentation Without Executable Code

**Advantages**

- No infrastructure cost
- Simple maintenance

**Disadvantages**

- Weak engineering evidence
- No testing
- No executable implementation
- Limited value during technical interviews

### Use Simulated Claims Without Disclosure

**Advantages**

- Appears more complete

**Disadvantages**

- Misleading
- Damages credibility
- Cannot withstand technical questioning
- Violates the portfolio's truthfulness principle

## Consequences

### Positive Consequences

- The project remains financially sustainable.
- Most engineering behavior can be tested locally.
- Cloud demonstrations remain intentional and bounded.
- Cost controls become part of the architecture.
- Portfolio claims remain truthful.
- Reviewers can reproduce many validations without paid accounts.

### Negative Consequences and Trade-offs

- Some Azure-managed capabilities cannot be demonstrated continuously.
- Screenshots may represent short-lived deployments.
- Local Spark cannot reproduce every Databricks-managed behavior.
- Performance claims must remain conservative.
- Infrastructure definitions may be validated without always being applied.

## Implementation Implications

The baseline toolchain will prioritize:

```text
GitHub
Git
VS Code
Python
uv
Ruff
mypy
pytest
pre-commit
Mermaid
Terraform Community Edition
Databricks CLI
Databricks Free Edition where supported
Apache Spark local mode
GitHub Actions within applicable free usage

pre-deployment checks
deployment steps
validation steps
evidence capture
cleanup steps
post-cleanup verification
