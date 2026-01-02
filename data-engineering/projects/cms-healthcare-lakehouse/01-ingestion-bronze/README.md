# ⚪ Transformation — Silver Layer

## Purpose

The Silver layer is responsible for **cleansing, standardizing, and conforming** raw CMS data into **analysis-ready entities** with enforced data quality rules.

This layer bridges raw ingestion and analytical modeling.

---

## Responsibilities

- Clean and normalize CMS datasets
- Enforce data types and constraints
- Standardize healthcare identifiers (NPI, CCN, HCPCS)
- Apply deduplication logic
- Validate data quality and integrity

---

## Key Transformations

- Identifier normalization (NPI, CCN)
- Monetary and numeric field standardization
- Null and range validation
- Referential integrity checks
- Procedure code conformance

---

## Core Silver Tables

- `silver_provider`
- `silver_hospital`
- `silver_procedure`
- `silver_provider_utilization`
- `silver_quality_measure`

Each table represents a **clean, conformed entity** ready for dimensional modeling.

---

## Data Quality Checks

Implemented checks include:
- Uniqueness of business keys
- Mandatory field completeness
- Referential integrity between entities
- Record count and anomaly detection

Quality results are surfaced to the **Observability layer**.

---

## Downstream Dependencies

Silver tables are consumed by the **Gold serving layer** to build fact and dimension models for analytics and BI.