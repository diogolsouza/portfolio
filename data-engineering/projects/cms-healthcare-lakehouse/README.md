# 🏥 Azure Lakehouse - CMS Healthcare Analytics

## Project Overview

This project implements an **end-to-end Azure Lakehouse architecture** using **publicly available U.S. Medicare data** published by the Centers for Medicare & Medicaid Services (CMS) to demonstrate **production-grade data engineering practices**.

The objective is to design and implement a scalable healthcare data platform that supports **analytics, BI, and AI workloads**, following modern **ETL and ELT patterns** and the **Medallion architecture (Bronze → Silver → Gold)**.

This project is part of a broader **Data Engineering portfolio** and is intentionally designed as a **realistic, enterprise-style case study**, not a tutorial.

---

## Business Context

Healthcare analytics is a highly regulated, data-intensive domain involving large volumes of financial, operational, and quality-related data.  
Public and private stakeholders rely on this data to understand:

- Medicare cost and utilization patterns  
- Provider and hospital performance  
- Regional disparities in healthcare spending  
- Relationships between cost and quality of care  

This project focuses on **historical, aggregated healthcare analytics**, not real-time clinical decision-making.

---

## Data Source

This project uses **publicly available Medicare datasets** published by the **U.S. Centers for Medicare & Medicaid Services (CMS)**.

**Key characteristics:**
- Domain: Healthcare cost, utilization, and quality analytics
- Data type: Historical batch files (CSV)
- Update frequency: Periodic (annual / quarterly, depending on dataset)
- Usage: Educational and analytical purposes only

No protected health information (PHI), personally identifiable data, or restricted datasets are used.

---

## Architecture Overview

The solution follows a **Lakehouse-first design**, combining scalable cloud storage, distributed processing, and analytical SQL engines.

```
Source Data (CMS Open Data)
        │
        ▼
Azure Data Factory (Orchestration)
        │
        ▼
Azure Data Lake Gen2 (Delta Lake)
  ┌────────────────────────────┐
  │ Bronze → Silver → Gold     │  ← Databricks (ETL)
  └────────────────────────────┘
                │
                ▼
Azure Synapse Analytics
(Data Warehouse & SQL ELT)
```

---

## ETL and ELT Strategy

This project intentionally applies **both ETL and ELT patterns**, based on data layer responsibility.

### ETL (Ingestion & Curation)

ETL is used to ensure **data correctness, standardization, and quality** before analytics consumption.

- Raw ingestion into Bronze (append-only)
- Data cleansing and conformance in Silver
- Incremental and idempotent processing
- Healthcare-specific data quality validation (keys, ranges, null checks)

**Technologies:** Azure Data Factory, Azure Databricks (PySpark, Delta Lake)

---

### ELT (Analytics & Serving)

ELT is used to apply **business logic and analytics transformations** inside SQL-based analytical engines.

- Fact and Dimension table creation
- SCD Type 1 and Type 2 logic
- Metric calculations and aggregations
- Star schema modeling for BI and analytics

**Technologies:** Azure Synapse Analytics, SQL

---

## Project Structure

```
cms-healthcare-lakehouse/
│
├─ 01-ingestion-bronze/
│   └─ Raw ingestion, schema handling, replayability
│
├─ 02-transformation-silver/
│   └─ Cleansing, conformance, data quality gates
│
├─ 03-serving-gold/
│   └─ Business-ready fact and dimension datasets
│
├─ 04-synapse-warehouse/
│   └─ Dimensional modeling and SQL analytics
│
├─ 05-orchestration-ci-cd/
│   └─ Orchestration, pipelines, deployment considerations
│
├─ 06-observability/
│   └─ Logging, monitoring, alerting, runbooks
│
└─ 07-documentation/
    └─ Data dictionary, lineage, governance notes
```

### 📂 Layer Navigation

- 🟤 **01 – Ingestion (Bronze)**  
  Raw ingestion, schema handling, replayability

- ⚪ **02 – Transformation (Silver)**  
  Cleansing, conformance, data quality gates

- 🟡 **03 – Serving (Gold)**  
  Business-ready datasets and aggregates

- 🏢 **04 – Synapse Warehouse**  
  Dimensional modeling and SQL analytics

- 🔁 **05 – Orchestration & CI/CD**  
  Orchestration, pipelines, deployment considerations

- 📊 **06 – Observability**  
  Logging, monitoring, alerting, runbooks

- 📚 **07 – Documentation**  
  Data dictionary, lineage, governance

Each folder contains its own README describing design decisions and responsibilities.

---

## Key Engineering Concepts Demonstrated

- Medallion architecture with clear layer boundaries
- Incremental ingestion and reprocessing strategies
- Schema enforcement and evolution handling
- Healthcare-focused data quality validation
- Dimensional modeling (Fact / Dimension)
- Separation of ETL and ELT concerns
- Analytics- and AI-ready healthcare data design

---

## Intended Audience

This project is intended for:

- Data Engineers
- Analytics Engineers
- BI Engineers
- Data Architects
- Technical recruiters and hiring managers

It demonstrates **engineering maturity, architectural reasoning, and real-world applicability** in a healthcare analytics context using Azure-native technologies.

---

## Disclaimer

This project is for **educational and portfolio purposes only**.  
All data used is publicly available, historical, and non-sensitive.
