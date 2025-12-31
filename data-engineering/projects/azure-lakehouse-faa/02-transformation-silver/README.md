# ⚪ Silver Layer — FAA Flight Data Transformation & Quality

## Objective

The Silver layer is responsible for **transforming raw FAA flight data into clean, standardized, and trustworthy datasets** that are ready for analytical consumption.

This layer applies **ETL transformations focused on data correctness and quality**, not business metrics.  
It represents the **final engineering boundary** before analytics-oriented layers (Gold and Warehouse).

---

## Input Data

- **Source:** Bronze Delta tables (raw FAA / BTS flight data)
- **Granularity:** Flight-level records
- **Characteristics:** Append-only, schema-evolving, replayable

The Silver layer never reads directly from external sources; it depends exclusively on the Bronze layer.

---

## Responsibilities of the Silver Layer

The Silver layer is intentionally responsible for:

- Data cleansing and normalization
- Deduplication of flight records
- Standardization of formats and codes
- Conformance across related datasets
- Enforcement of data quality (DQ) rules
- Incremental and idempotent processing

Anything related to **business logic, KPIs, or analytics semantics** is deferred to downstream layers.

---

## Transformation Pattern (ETL)

The Silver layer follows a strict **ETL pattern**, executed in distributed processing engines.

### Extract
- Read incremental data from Bronze Delta tables
- Identify new or changed records using ingestion metadata

### Transform
- Normalize data types (dates, timestamps, numeric fields)
- Standardize categorical values (airports, carriers, delay codes)
- Apply deduplication logic
- Enforce data quality rules

### Load
- Write curated Delta tables to the Silver layer
- Use MERGE patterns to ensure idempotency
- Maintain stable, analytics-friendly schemas

---

## Incremental Processing Strategy

Silver transformations are executed **incrementally** to ensure scalability and reliability.

**Key principles:**
- Process only new or updated Bronze records
- Safe reprocessing without data duplication
- Deterministic results across re-runs

**Typical strategy:**
- Track maximum processed ingestion timestamp or partition
- Use Delta Lake MERGE for upserts
- Maintain processing checkpoints

---

## Data Quality Rules

Data quality is **explicitly enforced** in the Silver layer.

### Examples of enforced rules:
- Mandatory fields must not be null (e.g., flight date, origin, destination)
- Primary identifiers must be unique within defined keys
- Referential integrity between flights, airports, and carriers
- Valid ranges for numeric fields (e.g., delays, distances)

### Quality behavior:
- Records failing critical rules are rejected or quarantined
- Pipelines fail when thresholds are exceeded
- Quality metrics are logged for observability

---

## Schema Standardization

- Column naming is standardized and documented
- Data types are normalized across datasets
- Units of measure are aligned (e.g., time, distance)
- No business-driven renaming or aggregation is performed

Schemas produced in Silver are **stable and reusable** by downstream layers.

---

## Storage Strategy

- Storage layer: Azure Data Lake Gen2
- File format: Delta Lake
- Write mode: Incremental MERGE
- Partitioning: Business-agnostic (e.g., date-based)

---

## Audit & Observability

Each Silver run records:

- Number of records read from Bronze
- Number of records written to Silver
- Number of rejected or quarantined records
- Data quality rule violations
- Processing duration

These metrics enable:
- Monitoring and alerting
- Root-cause analysis
- Controlled reprocessing

---

## What Is Explicitly Out of Scope

The following actions are **not allowed** in the Silver layer:

- Business KPIs or metrics
- Aggregations for reporting
- Analytics-specific joins
- Star schema creation

These responsibilities belong to the **Gold and Warehouse layers**.

---

## Technologies Used

- Azure Databricks (PySpark)
- Delta Lake
- Azure Data Lake Gen2
- SQL (data quality checks and audit metadata)

---

## Outcome

The Silver layer produces **high-quality, standardized, and trustworthy datasets** that serve as the **single source of truth** for downstream analytics, BI, and AI workloads.

By enforcing data quality and consistency here, the architecture ensures **reliable analytics without reapplying engineering logic downstream**.

---

## Disclaimer

This layer processes **public, historical, non-sensitive aviation data** exclusively for educational and portfolio purposes.
