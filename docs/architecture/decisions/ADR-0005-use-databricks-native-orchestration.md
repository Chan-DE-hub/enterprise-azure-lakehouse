# ADR-0005: Prefer Databricks-Native Orchestration for Databricks Workloads

- **Status:** Accepted
- **Date:** 2026-07-24
- **Decision owners:** Data Engineering
- **Related documents:** [Architecture Overview](../architecture-overview.md)

## Context

The platform requires scheduling, dependency management, parameter passing, retries, deployment, monitoring, and operational control.

Multiple orchestration tools could be introduced, including Databricks Workflows, Azure Data Factory, and Apache Airflow.

Using several orchestrators for the same responsibility increases operational complexity and makes failure ownership unclear.

## Decision

Databricks Workflows will be the default orchestrator for workloads whose execution remains primarily within Databricks.

Lakeflow Spark Declarative Pipelines will manage table-level data dependencies where their declarative model is appropriate.

Declarative Automation Bundles will define and deploy Databricks jobs, pipelines, parameters, permissions, and environment targets.

Apache Airflow will be used only in a separate cross-platform orchestration demonstration where workflow ownership spans multiple independent systems.

Azure Data Factory will be represented separately for Azure-native ingestion and integration scenarios rather than being inserted into every Databricks-only workflow.

## Decision Drivers

- Native operational visibility
- Reduced tool sprawl
- Clear failure ownership
- Environment-aware deployment
- Lower portfolio operating cost
- Simpler authentication
- Appropriate use of each orchestration layer
- Interview-relevant cross-platform understanding without unnecessary complexity

## Alternatives Considered

### Use Airflow for All Workloads

**Advantages**

- Vendor-neutral orchestration
- Strong cross-platform scheduling
- Broad operator ecosystem

**Disadvantages**

- Additional infrastructure
- Additional authentication and monitoring
- Duplicates Databricks-native capabilities
- Higher operational burden for Databricks-only workflows

### Use Azure Data Factory for All Workloads

**Advantages**

- Strong Azure integration
- Visual orchestration
- Suitable for many ingestion scenarios

**Disadvantages**

- Adds an external control layer to Databricks-native dependencies
- Can create split monitoring and retry behavior
- Requires Azure resources that may generate cost
- Not necessary for every Lakehouse transformation

### Mix Multiple Orchestrators Within One Pipeline

**Advantages**

- Each task can use a specialized tool

**Disadvantages**

- Fragmented lineage and monitoring
- Complex retry and recovery behavior
- Ambiguous ownership
- Harder end-to-end deployment

## Consequences

### Positive Consequences

- Databricks workloads use native scheduling and observability.
- Deployment definitions remain version controlled.
- Authentication boundaries are simpler.
- Airflow and ADF are demonstrated only where they add architectural value.
- The flagship repository remains coherent.

### Negative Consequences and Trade-offs

- Databricks Workflows introduces platform coupling.
- Enterprise processes spanning many systems may still require external orchestration.
- Cross-platform monitoring may require additional integration.
- Some orchestration scenarios must be documented separately.

## Implementation Implications

The flagship repository will include:

```text
resources/
    jobs/
    pipelines/

databricks.yml
