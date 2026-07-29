# Development Workflow

## Purpose

This document defines the standard development workflow for the Enterprise Azure Lakehouse repository.

The objective is to keep changes small, reviewable, testable, and traceable throughout the project lifecycle.

---

## Standard Workflow

Every change should follow this sequence:

```text
Issue or Requirement
        │
        ▼
Create Feature Branch
        │
        ▼
Implement the Change
        │
        ▼
Add or Update Tests
        │
        ▼
Run Quality Checks
        │
        ▼
Update Documentation
        │
        ▼
Commit Changes
        │
        ▼
Push Branch
        │
        ▼
Open Pull Request
        │
        ▼
Review and Validation
        │
        ▼
Merge into Main
        │
        ▼
Delete Feature Branch
```

---

## Branching

Development should not be performed directly on the `main` branch.

Each change must use a dedicated branch based on its purpose.

Examples:

```text
feature/bronze-ingestion
fix/metadata-validation
docs/architecture-overview
refactor/config-loader
test/metadata-rules
chore/update-dependencies
```

---

## Local Validation

Before committing changes, run the required quality checks.

```powershell
pytest
ruff check .
ruff format --check .
mypy src
pre-commit run --all-files
```

A change should not be committed when required checks are failing.

---

## Commit Guidelines

Commits should be focused and describe one logical change.

Examples:

```text
feat: implement metadata repository cache
fix: handle missing source configuration
docs: add development workflow
refactor: simplify validation rules
test: add metadata loader tests
chore: update project dependencies
```

---

## Pull Request Expectations

Each pull request should include:

- Purpose of the change
- Scope of the implementation
- Important design decisions
- Tests performed
- Documentation updated
- Known limitations
- Future considerations

Pull requests should remain small enough to review confidently.

---

## Merge Requirements

A pull request should only be merged when:

- The implementation matches the stated scope
- Tests pass
- Linting passes
- Static type checks pass
- Pre-commit checks pass
- Documentation is updated when required
- The branch is up to date with `main`

---

## Post-Merge Cleanup

After a successful merge:

1. Switch to `main`.
2. Pull the latest changes.
3. Delete the local feature branch.
4. Delete the remote feature branch when it is no longer needed.
5. Create a new branch for the next change.

Example:

```powershell
git checkout main
git pull origin main
git branch -d docs/repository-polish
```
