# ADR-0001: Use Unity Catalog as the Governance Foundation

- **Status:** Accepted
- **Date:** 2026-07-24
- **Decision owners:** Data Engineering
- **Related documents:** [Architecture Overview](../architecture-overview.md)

## Context

The Lakehouse platform requires consistent governance for data assets, files, tables, views, permissions, ownership, discovery, and lineage.

Legacy workspace-local metastore patterns create fragmented governance and make it more difficult to apply consistent access controls across environments and workspaces.

The portfolio must represent an enterprise-oriented governance model while remaining executable in a limited-cost environment.

## Decision

Unity Catalog will be the governance foundation for all Databricks-managed data assets represented by this repository.

The target hierarchy will follow:

```text
Metastore
    ↓
Catalog
    ↓
Schema
    ↓
Table / View / Volume / Function / Model

Environment separation will primarily be represented through separate catalogs:

dev_<domain>
test_<domain>
prod_<domain>

Schemas will organize data by functional responsibility, including:

landing
bronze
quarantine
silver
gold
config
control
audit
monitoring
