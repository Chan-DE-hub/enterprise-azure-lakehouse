# ADR-0003: Limit Metadata-Driven Design to Repeatable Technical Behavior

- **Status:** Accepted
- **Date:** 2026-07-24
- **Decision owners:** Data Engineering
- **Related documents:** [Architecture Overview](../architecture-overview.md)

## Context

Enterprise ingestion platforms often repeat the same technical behavior across many sources. Configuration-driven processing can reduce duplication and make onboarding more consistent.

However, overly generic frameworks frequently move complex business behavior into configuration tables, dynamic expressions, or large universal engines. This makes systems difficult to understand, test, debug, and operate.

The portfolio requires a metadata-driven architecture without turning every pipeline into an opaque abstraction.

## Decision

Metadata will control repeatable technical behavior.

Explicit, version-controlled code will implement complex business logic.

Configuration may define:

- source identifiers
- source connection references
- file formats
- source and target paths
- target object names
- ingestion modes
- load frequencies
- watermark columns
- primary keys
- CDC operation columns
- CDC sequence columns
- schema contract references
- checkpoint locations
- retry policies
- data-quality rule references
- notification routes
- enabled or disabled status

Configuration will not be used to hide:

- complex joins
- business calculations
- dimensional modeling
- financial logic
- survivorship rules
- cross-domain transformations
- source-specific parsing that cannot be expressed safely
- consumer-specific semantic logic

Separate ingestion adapters will be used when source technologies have meaningfully different operational behavior.

## Decision Drivers

- Reuse without opacity
- Maintainability
- Testability
- Code-review clarity
- Source-specific reliability
- Faster onboarding of similar sources
- Controlled configuration
- Reduced framework complexity

## Alternatives Considered

### Fully Hardcoded Pipelines

**Advantages**

- Explicit behavior
- Easy to understand for small numbers of pipelines
- Straightforward debugging

**Disadvantages**

- High duplication
- Inconsistent onboarding
- Repeated operational logic
- Difficult bulk changes

### Universal Configuration-Only Engine

**Advantages**

- Maximum apparent reuse
- New sources may require little code

**Disadvantages**

- Configuration becomes a programming language
- Weak static analysis
- Difficult debugging
- Complex conditional behavior
- Business logic becomes hidden
- High blast radius from framework defects

### One Universal Ingestion Adapter

**Advantages**

- Single entry point
- Simplified surface area

**Disadvantages**

- Ignores differences among files, APIs, JDBC, CDC, Kafka, and Event Hubs
- Encourages deeply nested conditional logic
- Weak source-specific observability and recovery behavior

## Consequences

### Positive Consequences

- Repeated technical behavior is standardized.
- Business logic remains visible and reviewable.
- Different source types can use appropriate ingestion adapters.
- Configuration changes can be validated before execution.
- Framework scope remains understandable.
- Unit tests can target both configuration validation and explicit transformation logic.

### Negative Consequences and Trade-offs

- Some code duplication is accepted when it preserves clarity.
- New source categories may require new adapters.
- Configuration schemas require governance and validation.
- Engineers must decide carefully whether behavior belongs in metadata or code.

## Implementation Implications

The repository will separate:

```text
configuration
    ↓
validated technical metadata
    ↓
source-specific ingestion adapter
    ↓
explicit transformation code


config_loader.py
config_models.py
config_validator.py
file_ingestion.py
api_ingestion.py
jdbc_ingestion.py
event_stream_ingestion.py
