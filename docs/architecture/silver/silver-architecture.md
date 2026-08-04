# Silver Layer Architecture

## Purpose

The Silver layer is responsible for transforming raw Bronze datasets into trusted,
typed, validated, standardized, and reusable enterprise datasets.

Silver is the canonical integration layer.

Business aggregations do not belong in Silver.

---

## Responsibilities

- Standardize schemas
- Normalize column names
- Cast data types
- Handle null values
- Validate business rules
- Validate technical rules
- Deduplicate records
- Apply CDC
- Route invalid records to Quarantine
- Produce reusable conformed datasets

---

## Non Responsibilities

- KPI calculations
- Reporting
- Dashboard metrics
- Star schema
- Fact tables
- Dimension tables

Those belong to Gold.

---

## Processing Flow

Bronze

↓

Standardization Processor

↓

Quality Processor

↓

Expectation Engine

↓

Deduplication Processor

↓

CDC Processor

↓

Quarantine Router

↓

Silver Writer

↓

Silver

---

## Design Principles

- Metadata Driven
- Idempotent
- Incremental
- Streaming-first
- Declarative
- Testable
- Observable
- Reusable
- Stateless processors
- Configuration over code
