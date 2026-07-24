# Architecture Decision Records

Architecture Decision Records document the significant technical and architectural decisions made for the Enterprise Azure Lakehouse portfolio.

Each ADR explains:

- the context that required a decision
- the selected approach
- the alternatives considered
- the consequences and trade-offs
- the implementation implications

ADRs are immutable historical records. When a decision changes, the original ADR is not deleted or rewritten to hide the previous decision. A new ADR supersedes it and links back to the earlier record.

---

## ADR Statuses

| Status | Meaning |
|---|---|
| Proposed | Under evaluation and not yet approved |
| Accepted | Approved and currently applicable |
| Superseded | Replaced by a newer ADR |
| Deprecated | No longer recommended but retained for historical context |
| Rejected | Considered but intentionally not selected |

---

## Decision Index

| ADR | Decision | Status |
|---|---|---|
| [ADR-0001](ADR-0001-use-unity-catalog-for-governance.md) | Use Unity Catalog as the governance foundation | Accepted |
| [ADR-0002](ADR-0002-use-unity-catalog-volumes.md) | Use Unity Catalog volumes instead of DBFS mounts | Accepted |
| [ADR-0003](ADR-0003-limit-metadata-driven-design.md) | Limit metadata-driven design to repeatable technical behavior | Accepted |
| [ADR-0004](ADR-0004-separate-landing-bronze-and-quarantine.md) | Separate Landing, Bronze, and Quarantine responsibilities | Accepted |
| [ADR-0005](ADR-0005-use-databricks-native-orchestration.md) | Prefer Databricks-native orchestration for Databricks workloads | Accepted |
| [ADR-0006](ADR-0006-adopt-free-first-operating-model.md) | Adopt a free-first and cost-conscious portfolio operating model | Accepted |

---

## Naming Convention

ADR files use the following format:

```text
ADR-NNNN-short-decision-title.md
