# 🟡 Serving — Gold Layer

## Purpose

The Gold layer delivers **analytics-ready trend and signal datasets** optimized for **BI, analytics, and machine learning workloads**.

It represents the primary consumption layer of the market data platform.

---

## Responsibilities

- Generate deterministic trend and regime datasets
- Apply business-level aggregations
- Version signal logic for reproducibility
- Optimize data for analytical access patterns

---

## Gold Datasets

- `gold_market_trends`
- `gold_market_signals`
- `gold_market_regimes` (optional)

These datasets are **read-only**, curated, and optimized for downstream consumption.

---

## Design Principles

- Clear separation between raw data and signals
- Deterministic and reproducible logic
- Asset-agnostic signal definitions
- Separation of analytics and execution concerns

---

## Downstream Consumers

- BI and reporting tools
- Exploratory analytics
- Data science and ML pipelines