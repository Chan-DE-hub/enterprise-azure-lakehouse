# Branching Strategy

## Purpose

This document defines the branching strategy used by the Enterprise Azure Lakehouse repository.

The objective is to keep development isolated, reviewable, traceable, and safe while maintaining a stable `main` branch.

---

## Primary Branch

The `main` branch represents the latest reviewed and approved state of the repository.

Direct development on `main` is not allowed.

All changes must be introduced through a dedicated branch and merged through a pull request.

---

## Branch Types

Use the following branch prefixes.

| Prefix | Purpose | Example |
|---|---|---|
| `feature/` | New functionality | `feature/bronze-autoloader` |
| `fix/` | Defect correction | `fix/metadata-validation` |
| `docs/` | Documentation-only changes | `docs/architecture-overview` |
| `refactor/` | Internal code improvement without changing expected behavior | `refactor/config-loader` |
| `test/` | Test additions or improvements | `test/metadata-rules` |
| `chore/` | Maintenance, tooling, or dependency updates | `chore/update-dependencies` |
| `release/` | Release preparation | `release/v0.2.0` |

---

## Branch Naming Rules

Branch names should:

- Use lowercase letters
- Use hyphens between words
- Be short but descriptive
- Represent one clear scope
- Avoid personal names
- Avoid vague names such as `update`, `changes`, or `work`

Prefer:

```text
feature/bronze-ingestion
docs/repository-foundation
fix/missing-config-file
refactor/metadata-cache
```

Avoid:

```text
new-work
christian-branch
changes
final-update
test123
```

---

## Creating a Branch

Before creating a new branch, update the local `main` branch.

```powershell
git checkout main
git pull origin main
```

Then create the branch:

```powershell
git checkout -b docs/repository-foundation
```

Confirm the active branch:

```powershell
git branch --show-current
```

---

## Branch Scope

Each branch should address one logical concern.

A documentation branch should not also introduce unrelated application features.

A defect-fix branch should not include broad refactoring unless the refactoring is necessary to resolve the defect safely.

Keeping branches focused makes pull requests easier to review and reduces merge risk.

---

## Keeping a Branch Updated

For short-lived branches, pull the latest `main` changes when necessary before opening or merging a pull request.

```powershell
git fetch origin
git merge origin/main
```

Resolve conflicts locally, rerun the quality checks, and push the updated branch.

The repository may adopt a rebase-based strategy later, but merge-based synchronization is acceptable for the current portfolio workflow because it is explicit and beginner-safe.

---

## Commit Expectations

Commits within a branch should be:

- Focused
- Meaningful
- Written using Conventional Commit style
- Free from unrelated generated or temporary files

Examples:

```text
docs: add branching strategy
feat: implement bronze ingestion configuration
fix: reject duplicate source identifiers
test: add metadata repository regression tests
```

---

## Pull Request Requirement

Every branch intended for `main` must use a pull request.

The pull request should clearly describe:

- Why the change is needed
- What was changed
- What was intentionally excluded
- How the change was validated
- Any known limitations

---

## Merge Strategy

Use **Squash and merge** for focused feature and documentation branches unless preserving individual commits provides meaningful value.

A squash merge keeps the `main` branch history concise while retaining the pull request as the detailed review record.

The final squash commit message should follow Conventional Commit style.

Example:

```text
docs: establish documentation foundation
```

---

## Branch Cleanup

After the pull request is merged:

```powershell
git checkout main
git pull origin main
git branch -d docs/repository-foundation
```

Delete the remote branch through GitHub or with:

```powershell
git push origin --delete docs/repository-foundation
```

Do not delete a branch before confirming that its pull request has been merged successfully.

---

## Protected Branch Direction

As the repository matures, the `main` branch should use branch protection rules such as:

- Require a pull request before merging
- Require passing status checks
- Require the branch to be up to date
- Prevent force pushes
- Prevent deletion
- Require conversation resolution

These controls are planned until GitHub Actions and automated checks are added.

---

## Summary

The branching strategy follows a simple principle:

> One branch, one clear purpose, one reviewed pull request.

This approach supports incremental delivery, cleaner history, safer changes, and easier technical review.
