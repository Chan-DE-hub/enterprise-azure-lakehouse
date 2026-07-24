# Enterprise Azure Lakehouse

A production-oriented Data Engineering portfolio project demonstrating modern Azure and Databricks architecture using metadata-driven ingestion, Medallion Architecture, Unity Catalog, Delta Lake, Lakeflow Declarative Pipelines, CI/CD, testing, governance, and observability.

> This project is a portfolio-based reference implementation. It simulates enterprise engineering practices and does not represent production deployment experience with every technology included.

---

## Project Status

**Current phase:** Repository Foundation

This project is being developed incrementally using architecture-first and production-oriented engineering principles.

---

## Business Scenario

A retail organization receives customer, product, order, payment, shipment, and return data from multiple operational systems.

The objective is to build a secure, scalable, governed, and observable Lakehouse platform that supports:

- Batch file ingestion
- Incremental processing
- Change Data Capture
- Streaming events
- Data quality and quarantine
- Dimensional modeling
- Business reporting
- Operational monitoring
- Replay and backfill
- Automated deployment

---

## Target Architecture

```text
Source Systems
    ↓
ADLS Gen2 Landing Zone / Event Broker
    ↓
Unity Catalog External Volumes
    ↓
Bronze Raw Data
    ↓
Data Quality and Quarantine
    ↓
Silver Conformed Data
    ↓
Gold Data Products
    ↓
Databricks SQL / BI / Analytics


**Supporting platform Capabilities:**

GitHub
    ↓
GitHub Actions
    ↓
Databricks Declarative Automation Bundles
    ↓
Azure Databricks

Azure Key Vault
Unity Catalog
Terraform
Databricks Workflows
Monitoring and Audit Framework

## Technology Stack

**Core Platform**
- Microsoft Azure
- Azure Data Lake Storage Gen2
- Azure Databricks
- Unity Catalog
- Delta Lake
- Lakeflow Spark Declarative Pipelines

**Data Engineering**
- Python
- PySpark
- SQL
- Apache Spark Structured Streaming
- Auto Loader
- Metadata-driven ingestion
- CDC and incremental processing

**DevOps and Infrastructure**
- Git
- GitHub
- GitHub Actions
- Declarative Automation Bundles
- Terraform
- YAML

**Supporting Technologies**
- Azure Event Hubs
- Apache Kafka
- dbt
- Apache Airflow
- Snowflake

## Engineering Principles

**This project follows the following principles:**
- Source fidelity
- Separation of concerns
- Metadata-driven technical behavior
- Explicit business logic
- Idempotent processing
- Incremental processing
- Schema enforcement
- Data contracts
- Least-privilege access
- Environment isolation
- Observability by design
- Replayability
- Testability
- Auditability
- Cost awareness
- Documentation as code
- Simplicity before abstraction

**Planned Project Phases**
1. Repository foundation
2. Azure and Databricks platform blueprint
3. Unity Catalog bootstrap
4. Declarative Automation Bundle foundation
5. Configuration, control, and audit models
6. File-ingestion Bronze layer
7. Data quality and quarantine
8. Silver processing
9. Gold data products
10. Observability and alerting
11. Testing and CI/CD
12. Backfill, replay, and operational runbooks
13. Kafka streaming
14. Azure Event Hubs streaming
15. Direct source-system ingestion
16. Final architecture and hiring-manager review

**Planned Data Domains**
- Customers
- Products
- Orders
- Order items
- Payments
- Shipments
- Returns

**Repository Structure**

enterprise-azure-lakehouse/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── src/
├── config/
├── resources/
├── sql/
├── tests/
├── scripts/
├── infrastructure/
├── docs/
└── sample_data/

The repository structure will be expanded incrementally as each phase is implemented.

## Portfolio Scope

**Implemented directly**
- Architecture and repository design
- Metadata models
- PySpark and SQL transformations
- Data-quality patterns
- Pipeline configuration
- Testing
- Documentation
- CI/CD definitions
- Sample data and failure scenarios

**Simulated enterprise capabilities**
- Multi-environment deployment
- Group-based security
- Production approval workflows
- Operational support procedures
- Disaster recovery
- Cost and SLA monitoring

**Normally owned by a platform team**
- Azure subscription governance
- Network architecture
- Enterprise identity federation
- Production secret rotation
- Central monitoring infrastructure
- Organization-wide policy enforcement

**Current Limitations**
- Designed for a cost-conscious portfolio environment
- Uses synthetic and non-sensitive sample data
- Some Azure and Databricks components may be represented through code and documentation when live resources are unavailable
- Enterprise-scale throughput is demonstrated through architecture and test strategy rather than real production volume

**Author**
Christian Evangelista
