# Contributing Guide

## Purpose

This repository demonstrates production-inspired Azure Data Engineering architecture and engineering practices.

Although this repository is maintained by a single developer, contributions should follow engineering standards similar to enterprise software projects.

---

# Branch Strategy

The default branch is:

```
main
```

Feature development should use short-lived feature branches.

Example

```
feature/bronze-autoloader
feature/metadata-framework
feature/data-quality
```

---

# Commit Convention

Follow Conventional Commits.

Examples

```
feat: implement bronze autoloader ingestion

fix: resolve schema evolution issue

docs: update architecture overview

refactor: simplify configuration loader

test: add parser unit tests

ci: validate Databricks bundle

build: update project dependencies
```

---

# Pull Requests

Each pull request should:

- explain the purpose
- describe the implementation
- explain architectural decisions
- explain trade-offs
- include testing evidence
- update documentation when necessary

---

# Engineering Principles

Every contribution should preserve:

- Source fidelity
- Separation of concerns
- Idempotency
- Incremental processing
- Metadata-driven technical behavior
- Testability
- Replayability
- Observability
- Security
- Cost awareness

---

# Coding Standards

Python

- type hints
- meaningful names
- avoid hardcoded values
- avoid global state
- avoid unnecessary classes
- unit-testable functions

SQL

- explicit columns
- deterministic logic
- incremental-friendly
- no unnecessary SELECT *

YAML

- no secrets
- reusable variables
- environment separation

---

# Documentation

Every architectural decision must be documented.

Every major implementation should include:

- purpose
- design decision
- deployment
- testing
- monitoring
- failure scenarios
