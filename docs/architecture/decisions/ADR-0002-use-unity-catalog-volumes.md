# ADR-0002: Use Unity Catalog Volumes Instead of DBFS Mounts

- **Status:** Accepted
- **Date:** 2026-07-24
- **Decision owners:** Data Engineering
- **Related documents:** [ADR-0001](ADR-0001-use-unity-catalog-for-governance.md)

## Context

The platform requires governed access to landing files, schemas, configuration artifacts, test fixtures, and other non-tabular data.

Legacy Databricks implementations often use DBFS mounts to expose cloud storage through workspace-level paths. Mounts depend on older access patterns, are difficult to govern centrally, and can obscure the relationship between identities, storage locations, and permissions.

The repository requires a modern file-access pattern aligned with Unity Catalog.

## Decision

Unity Catalog volumes will be used as the primary governed interface for non-tabular files accessed by Databricks workloads.

Target paths will follow:

```text
/Volumes/<catalog>/<schema>/<volume>/<relative-path>

/Volumes/dev_sales/landing/source_system/orders/
/Volumes/dev_sales/config/contracts/orders/
/Volumes/dev_sales/quarantine_payloads/orders/
/Volumes/dev_sales/test_data/fixtures/

abfss://container@account.dfs.core.windows.net/path
