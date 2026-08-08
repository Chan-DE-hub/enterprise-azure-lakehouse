# Coding Standards

## Purpose

This document defines the coding standards for the Enterprise Azure Lakehouse repository.

The objective is to keep the codebase readable, maintainable, testable, and consistent as the project grows.

---

## General Principles

All implementation should prioritize:

- Readability over cleverness
- Explicit behavior over hidden behavior
- Small and focused components
- Clear separation of concerns
- Strong typing
- Testability
- Predictable error handling
- Minimal duplication
- Documentation for non-obvious decisions

---

## Python Version

The project should use the Python version declared in `pyproject.toml`.

Developers should use the same supported version locally to reduce environment inconsistencies.

---

## Code Formatting and Linting

Ruff is used for linting and formatting.

Run:

```powershell
ruff check .
ruff format --check .
```

To apply formatting:

```powershell
ruff format .
```

Code should not be committed while linting or formatting checks are failing.

---

## Type Safety

Public functions, methods, and important internal functions should use type annotations.

Example:

```python
from pathlib import Path


def load_configuration(path: Path) -> dict[str, object]:
    """Load and return configuration data from a file."""
    ...
```

Avoid using `Any` unless there is a clear technical reason.

Static type validation is performed with mypy:

```powershell
mypy src
```

---

## Function Design

Functions should:

- Perform one clear responsibility
- Use descriptive names
- Avoid excessive nesting
- Avoid hidden side effects
- Return predictable types
- Raise domain-specific exceptions when appropriate

Prefer:

```python
def validate_source_name(source_name: str) -> None:

```

Avoid:

```python
def process(data):

```

when the function performs multiple unrelated operations.

---

## Class Design

Classes should represent a clear responsibility or abstraction.

Use classes when they provide meaningful encapsulation, state management, or extensibility.

Avoid creating classes only to group unrelated utility functions.

---

## Configuration

Do not hardcode environment-specific values in application code.

Configuration should be supplied through:

- Typed settings
- YAML configuration
- Environment variables
- Secure secret-management services when introduced

Examples of values that should not be hardcoded:

- Storage paths
- Catalog names
- Schema names
- Connection strings
- Credentials
- Environment names
- Pipeline identifiers

---

## Exception Handling

Use the project exception hierarchy for expected application and domain failures.

Do not silently suppress exceptions.

Prefer:

```python
try:
    metadata = repository.get(source_id)
except MetadataNotFoundError:
    logger.exception("Metadata record was not found", extra={"source_id": source_id})
    raise
```

Avoid:

```python
try:
    metadata = repository.get(source_id)
except Exception:
    pass
```

Catch broad exceptions only at intentional application boundaries where logging, translation, or cleanup is required.

---

## Logging

Use structured logging rather than `print()` statements.

Log messages should describe the event clearly and include relevant context.

Prefer:

```python
logger.info(
    "Metadata configuration loaded",
    extra={
        "source_id": source_id,
        "repository_type": repository.__class__.__name__,
    },
)
```

Do not log:

- Passwords
- Access tokens
- Secret values
- Connection strings containing credentials
- Sensitive business data

---

## Documentation

Public modules, classes, functions, and methods should have concise docstrings when their purpose is not immediately obvious.

Comments should explain why a decision exists rather than restating what the code does.

Prefer:

```python
# Cache validated metadata to avoid repeated file reads during one pipeline run.
```

Avoid:

```python
# Get the metadata.
metadata = repository.get(source_id)
```

---

## Imports

Imports should be grouped in this order:

1. Python standard library
2. Third-party packages
3. Project modules

Example:

```python
from pathlib import Path

from pydantic import BaseModel

from enterprise_lakehouse.metadata.models import SourceMetadata
```

Avoid wildcard imports.

---

## Testing

New behavior should include tests when practical.

Tests should cover:

- Expected behavior
- Validation failures
- Boundary conditions
- Domain-specific exceptions
- Regression scenarios

Tests should be deterministic and independent of execution order.

Run:

```powershell
pytest
```

---

## File and Module Naming

Use lowercase snake case for Python modules:

```text
metadata_loader.py
configuration_service.py
validation_rules.py
```

Use descriptive names that represent the module's responsibility.

Avoid generic names such as:

```text
helpers.py
common.py
utils.py
```

unless the scope is narrow and clearly documented.

---

## Dependency Management

Dependencies should be declared in `pyproject.toml`.

Avoid adding a package when the standard library or an existing dependency can satisfy the requirement cleanly.

New dependencies should have:

- A clear project purpose
- Active maintenance
- Compatible licensing
- Acceptable security posture
- Reasonable operational cost

---

## Quality Gate

Before opening a pull request, run:

```powershell
pytest
ruff check .
ruff format --check .
mypy src
pre-commit run --all-files
```

All required checks should pass before the change is considered ready for review.
