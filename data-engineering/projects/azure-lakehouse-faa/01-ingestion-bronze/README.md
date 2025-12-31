# 🟤 Bronze Layer — FAA Flight Data Ingestion

## Objective

The Bronze layer is responsible for **ingesting raw FAA flight performance data into the Azure Data Lake** in a **safe, auditable, and replayable** manner.

This layer preserves data **as close as possible to the source**, applying only **technical transformations required for ingestion correctness**.  
No business logic, aggregations, or analytical transformations are applied at this stage.

---

## Data Source

This project uses **publicly available U.S. FAA / BTS flight performance data**.

**Characteristics:**
- Domain: Commercial aviation analytics
- Data type: Historical batch files (CSV / Parquet)
- Update frequency: Periodic (monthly)
- Granularity: Flight-level records
- Usage: Educational and analytical purposes only

No restricted, real-time, sensitive, or personally identifiable data is ingested.

---

## Responsibilities of the Bronze Layer

The Bronze layer is intentionally limited to the following responsibilities:

- Raw ingestion from public FAA/BTS sources
- Append-only storage using Delta Lake
- Incremental and idempotent ingestion
- Schema capture and evolution handling
- Technical metadata enrichment
- Audit and observability tracking

Anything related to **business rules or analytics** is explicitly deferred to downstream layers.

---

## Ingestion Architecture

```
Public FAA / BTS Data
        │
        ▼
Azure Data Factory (Orchestration)
        │
        ▼
Azure Databricks (PySpark Ingestion)
        │
        ▼
Azure Data Lake Gen2
(Bronze Delta Tables)
```

Azure Data Factory is responsible for **orchestration and scheduling**, while Databricks performs **scalable ingestion and Delta Lake writes**.

---

## Ingestion Pattern (ETL)

This layer follows an **ETL pattern** focused on technical correctness.

### Extract
- Source files are downloaded or referenced from public FAA/BTS repositories
- Files are ingested as-is without modification

### Transform (Technical Only)
- Column type casting (as required for ingestion)
- Addition of technical metadata columns
- No deduplication or business transformation

### Load
- Data is written as **append-only Delta tables**
- Existing data is never overwritten
- Reprocessing the same window does not create duplicates

---

## Incremental Loading Strategy

FAA data is ingested using a **batch-incremental strategy**.

**Approach:**
- Data is ingested per delivery window (e.g., year/month)
- Previously ingested partitions are tracked via metadata
- Re-runs are idempotent and safe

**Partitioning strategy:**
- Partitioned by `ingestion_year` and `ingestion_month`
- Enables efficient reprocessing and downstream filtering

---

## Schema Handling

- Schemas are explicitly captured at ingestion time
- Schema evolution is supported using Delta Lake features
- New or unexpected columns are accepted without pipeline failure

No schema normalization or renaming is performed in Bronze.

---

## Storage Strategy

- Storage layer: Azure Data Lake Gen2
- File format: Delta Lake
- Write mode: Append-only
- Table naming: Source-oriented (not business-oriented)

---

## Audit & Observability

Each ingestion run records audit metadata including:

- Source dataset identifier
- Ingestion timestamp
- Record counts (read vs written)
- Pipeline execution status
- Processing duration

This information supports:
- Monitoring and alerting
- Data reconciliation
- Debugging failed runs
- Controlled reprocessing

---

## What Is Explicitly Out of Scope

The following actions are **not allowed** in the Bronze layer:

- Deduplication
- Joins across datasets
- Business rules or metrics
- Aggregations
- Data quality filtering beyond technical validation

These responsibilities belong to the **Silver and Gold layers**.

---

## Technologies Used

- Azure Data Factory
- Azure Databricks (PySpark)
- Azure Data Lake Gen2
- Delta Lake
- SQL (audit metadata)

---

## Outcome

The Bronze layer provides a **trusted, immutable raw data foundation** that enables reliable downstream transformations, analytics, and AI workloads.

By enforcing strict boundaries at ingestion time, this layer ensures **replayability, traceability, and operational stability** across the entire Lakehouse architecture.

---

## Disclaimer

This layer ingests **public, historical, non-sensitive aviation data** for educational and portfolio purposes only.
