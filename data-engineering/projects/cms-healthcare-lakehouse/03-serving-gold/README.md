# 🟡 Serving — Gold Layer

## Purpose

The Gold layer delivers **business-ready, analytics-optimized datasets** using **dimensional modeling** techniques.

It is the primary consumption layer for BI, reporting, and advanced analytics workloads.

---

## Responsibilities

- Implement star-schema dimensional models
- Generate fact and dimension tables
- Apply business aggregations and metrics
- Optimize data for analytical access patterns

---

## Dimensional Model

### Dimensions
- `dim_provider` (NPI-based)
- `dim_hospital` (CCN-based)
- `dim_procedure` (HCPCS)
- `dim_geography`
- `dim_date`

### Facts
- `fact_provider_utilization`
- `fact_hospital_quality`

Surrogate keys are used consistently to support scalable joins and historical analysis.

---

## Design Principles

- Clear separation of facts and dimensions
- Consistent grain definition
- Reusable dimensions across facts
- BI- and AI-ready modeling patterns

---

## Downstream Consumers

- BI tools (Power BI)
- SQL-based analytics
- Data science and ML workloads