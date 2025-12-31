# 🏢 Synapse Warehouse — FAA Analytics Warehouse (ELT)

## Objective

The Synapse Warehouse layer provides a **relational, analytics-optimized data warehouse** built on top of the Gold layer.

This layer is responsible for **pure ELT transformations**, where data is first loaded from the lakehouse and then transformed **inside the SQL engine** to support enterprise BI, analytics, and semantic modeling.

It represents the **final analytical serving layer** of the Azure Lakehouse architecture.

---

## Input Data

- **Source:** Gold Delta tables (analytics-ready FAA datasets)
- **Granularity:** Curated analytical grains (flight-level and aggregated)
- **Characteristics:** Clean, stable schema, business-oriented

The warehouse never reads from Bronze or Silver layers directly.

---

## Responsibilities of the Warehouse Layer

The Synapse Warehouse is responsible for:

- Loading Gold datasets into relational tables
- Applying ELT transformations using SQL
- Designing and maintaining dimensional models
- Implementing Slowly Changing Dimensions (SCD)
- Exposing analytics-friendly schemas for BI tools
- Optimizing performance for analytical workloads

This layer is the **system of record for analytics consumption**.

---

## Transformation Strategy (Pure ELT)

This layer follows a **pure ELT approach**.

### Extract
- Read curated datasets from the Gold layer

### Load
- Load data into Synapse tables with minimal transformation

### Transform (SQL)
- Apply all business and analytics logic using SQL
- Create Fact and Dimension tables
- Implement SCD Type 1 and Type 2 logic
- Build star schemas and semantic structures

All transformations occur **inside the Synapse SQL engine**.

---

## Dimensional Modeling

The warehouse follows **dimensional modeling best practices**.

### Fact Tables
Examples:
- FactFlights
- FactDelays
- FactCancellations

Characteristics:
- Clearly defined grain
- Surrogate keys
- Additive and semi-additive measures

---

### Dimension Tables
Examples:
- DimDate
- DimAirport
- DimCarrier
- DimAircraft (if applicable)

Characteristics:
- Stable business keys
- Surrogate key management
- SCD Type 1 and/or Type 2 handling

---

## Slowly Changing Dimensions (SCD)

SCD strategies are applied based on analytical needs:

- **SCD Type 1:** Corrections or non-historical attributes
- **SCD Type 2:** Historical tracking of changes (e.g., carrier attributes)

SCD logic is implemented entirely in SQL using MERGE patterns.

---

## Performance & Optimization

The warehouse design considers:

- Table distribution strategies
- Partitioning by date or relevant dimensions
- Indexing for analytical queries
- Separation of staging and presentation schemas

Performance considerations are documented and revisited as data volume grows.

---

## BI & Semantic Consumption

The Synapse Warehouse is designed to be consumed by:

- BI tools (Looker, Power BI, Tableau)
- Ad-hoc SQL queries
- Analytics engineers defining semantic layers

The star schema ensures:
- Predictable query performance
- Simple metric definitions
- Tool-agnostic analytics access

---

## Audit & Observability

The warehouse layer tracks:

- Load timestamps
- Row counts per table
- ELT execution status
- Data freshness indicators

These metrics support:
- Data validation
- SLA monitoring
- Troubleshooting and reprocessing

---

## What Is Explicitly Out of Scope

The following actions are **not allowed** in the Warehouse layer:

- Raw data ingestion
- Low-level data cleansing
- Non-SQL transformations
- Tool-specific logic

These responsibilities belong to **upstream layers**.

---

## Technologies Used

- Azure Synapse Analytics
- SQL
- Azure Data Lake Gen2 (as source)
- Delta Lake (upstream storage)

---

## Outcome

The Synapse Warehouse delivers a **high-performance, analytics-optimized data model** that supports enterprise BI, analytics engineering, and advanced reporting.

By enforcing a **pure ELT approach**, this layer ensures clarity, flexibility, and maintainability for analytical workloads.

---

## Disclaimer

This warehouse processes **public, historical, non-sensitive aviation data** exclusively for educational and portfolio purposes.
