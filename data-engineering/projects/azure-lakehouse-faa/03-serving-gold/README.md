# 🟡 Gold Layer — FAA Flight Analytics & Business Serving

## Objective

The Gold layer is responsible for delivering **analytics-ready, business-oriented datasets** derived from the curated Silver layer.

This layer introduces **analytics semantics and business logic**, making data consumable by BI tools, analytical SQL engines, and downstream AI use cases.

The Gold layer represents the **first intentional use of ELT** in this project.

---

## Input Data

- **Source:** Silver Delta tables (cleaned and standardized FAA flight data)
- **Granularity:** Flight-level and derived analytical grains
- **Characteristics:** High-quality, stable schema, analytics-ready

The Gold layer never reads directly from Bronze or external sources.

---

## Responsibilities of the Gold Layer

The Gold layer is responsible for:

- Translating curated data into business-oriented datasets
- Defining analytical grains and aggregates
- Applying analytics semantics and metric logic
- Providing stable schemas for BI and SQL consumers
- Supporting both BI dashboards and exploratory analytics

This layer acts as the **contract between data engineering and analytics**.

---

## Transformation Strategy (Hybrid ETL + ELT)

The Gold layer intentionally applies a **hybrid transformation approach**.

### ETL in Gold (Limited & Intentional)
Used when transformations are:
- Computationally expensive
- Reused across multiple consumers
- Required to be materialized for performance

**Examples:**
- Daily or monthly flight performance aggregates
- Pre-calculated delay buckets
- Conformed analytical datasets

These transformations are executed in **Databricks (PySpark)** and stored as Delta tables.

---

### ELT in Gold (Primary Analytics Interface)
Used to expose analytics logic **inside SQL engines**.

**Examples:**
- SQL views over curated Delta tables
- Metric definitions (delay rates, cancellation rates)
- Filtered or reshaped analytical views

ELT enables:
- Flexible analytics
- Easier metric evolution
- Direct BI tool integration

---

## Analytical Datasets Produced

Typical Gold outputs include:

- Flight performance aggregates (by day, airport, carrier)
- Delay and cancellation metrics
- On-time performance indicators
- Time-based analytical views (daily, monthly, seasonal)

All datasets are:
- Documented
- Versioned
- Stable in schema

---

## Storage Strategy

- Storage layer: Azure Data Lake Gen2
- File format: Delta Lake
- Write mode: Overwrite or incremental (depending on dataset)
- Partitioning: Aligned with analytical access patterns

---

## BI & Analytics Consumption

The Gold layer is designed to be consumed by:

- Azure Synapse SQL
- BI tools (Looker, Power BI, Tableau)
- Ad-hoc SQL analytics
- Feature preparation for ML models

Gold datasets are **tool-agnostic** and not tied to a specific BI platform.

---

## Audit & Observability

Each Gold transformation records:

- Source Silver tables used
- Record counts and aggregation levels
- Transformation execution status
- Processing duration

This ensures:
- Traceability of business datasets
- Safe reprocessing
- Confidence for analytics users

---

## What Is Explicitly Out of Scope

The following actions are **not allowed** in the Gold layer:

- Raw data cleansing
- Schema normalization
- Low-level data quality enforcement
- Source-specific ingestion logic

These responsibilities belong to **Bronze and Silver layers**.

---

## Technologies Used

- Azure Databricks (PySpark)
- Delta Lake
- Azure Data Lake Gen2
- SQL (views and analytical logic)

---

## Outcome

The Gold layer delivers **trusted, analytics-ready datasets** that serve as the foundation for BI dashboards, SQL analytics, and AI experimentation.

By introducing ELT at this stage, the architecture ensures **flexibility, performance, and clear ownership boundaries** between engineering and analytics.

---

## Disclaimer

This layer processes **public, historical, non-sensitive aviation data** exclusively for educational and portfolio purposes.
